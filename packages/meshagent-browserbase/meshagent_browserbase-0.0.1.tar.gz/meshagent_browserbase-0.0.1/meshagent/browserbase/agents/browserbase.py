import logging
import aiohttp
from typing import Optional, Dict

from meshagent.api import RoomClient
from meshagent.agents import TaskRunner, AgentCallContext, ToolResponseAdapter
from meshagent.tools import Tool, Toolkit, JsonResponse, ToolContext
from meshagent.api import RoomException

from playwright.async_api import async_playwright, Playwright, PlaywrightContextManager
import os
import uuid

import asyncio

from browserbase import AsyncBrowserbase

from pydantic import BaseModel, Json, model_serializer
from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserConfig, Controller, ActionModel, SystemPrompt, ActionResult
from browser_use.controller.registry.views import RegisteredAction


from typing import Any


logger = logging.getLogger("browserbase")
logger.setLevel(logging.INFO)


class BrowserbaseContext:
    def __init__(self, *, project_id: str, api_key: str):
        self._project_id = project_id
        self._api_key = api_key
        self._client = AsyncBrowserbase(
            api_key=api_key,    
        )
        self._session = None
        self._http = aiohttp.ClientSession()
        self._playwrite_context = async_playwright() 
        self._playwright = None
        
    async def __aenter__(self):
        self._playwright = await self._playwrite_context.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self.client.close()
        await self._playwrite_context.__aexit__(*args)
         

    @property
    def project_id(self):
        return self._project_id
    
    @property
    def client(self):
        return self._client
    
    async def ensure_session(self):
        if self._session == None:
            self._session = asyncio.ensure_future(self._client.sessions.create(
                project_id=self._project_id,
            ))

        return await self._session
    

    async def create_browser(self):

        session = await self.ensure_session()

        chromium = self._playwright.chromium
        browser = await chromium.connect_over_cdp(session.connect_url, timeout=1)
        return browser
    

    async def get_live_url(self) -> str:
        """
        Get the URL to show the live view for the current browser session.

        :returns: URL
        """

        session = await self.ensure_session()

        session_url = f"https://api.browserbase.com/v1/sessions/{session.id}/debug"
        headers = {
            "Content-Type": "application/json",
            "x-bb-api-key": self._api_key,
        }
        response = await self._http.get(session_url, headers=headers)

        # Raise an exception if there wasn't a good response from the endpoint
        response.raise_for_status()
        live_view_data = (await response.json())
        pages = live_view_data["pages"]

        return pages[len(pages) - 1]["debuggerFullscreenUrl"]


_text_schema = {
    "type" : "object",
    "required" : [ "text" ],
    "additionalProperties" : False,
    "properties" : {
        "text" : {
            "type" : "string"
        }
    }
}





def get_registered_action(*, room: RoomClient, tool: Tool, response_adapter: ToolResponseAdapter) -> RegisteredAction:
     
    async def execute(**kwargs):
        response = await tool.execute(context=ToolContext(room=room, caller=room.local_participant), **(kwargs))
        try:
            result = await response_adapter.to_plain_text(room=room, response=response)
            return ActionResult(extracted_content=result, include_in_memory=True)
        except Exception as e:
            return ActionResult(error=str(e), include_in_memory=True)


    class _FakeModel(BaseModel):

        def __init__(self, **kwargs):
            super().__init__(json_obj=kwargs)  
       
        json_obj:dict

        def model_json_schema(**kwargs):
            return tool.input_schema
        
        def model_validate_json(**kwargs):
            return _FakeModel(json_obj=kwargs)
        
        
        @model_serializer
        def model_custom_serializer(self):
            return self.json_obj
        
        def model_dump(self, *, mode = 'python', include = None, exclude = None, context = None, by_alias = False, exclude_unset = False, exclude_defaults = False, exclude_none = False, round_trip = False, warnings = True, serialize_as_any = False):
            return self.json_obj
        
        def model_dump_json(self, *, indent = None, include = None, exclude = None, context = None, by_alias = False, exclude_unset = False, exclude_defaults = False, exclude_none = False, round_trip = False, warnings = True, serialize_as_any = False):
            return self.json_obj

    action = RegisteredAction(
        name=tool.name,
        description=tool.description,
        param_model=_FakeModel,
        function=execute
    )
     
    return action

def get_registered_actions_from_context(*, context: AgentCallContext, response_adapter: ToolResponseAdapter) -> list[RegisteredAction]:

    tools = list[RegisteredAction]()

    for toolkit in context.toolkits:
        for tool in toolkit.tools:
            tools.append(get_registered_action(room=context.room, tool=tool, response_adapter=response_adapter))

    return tools

class BrowserbaseTaskRunner(TaskRunner):

    def __init__(self, *, name, title=None, description=None, requires=None, supports_tools = None, response_adapter: Optional[ToolResponseAdapter] = None, toolkits: Optional[list[Toolkit]] = None, rules: Optional[list[str]] = None):
        super().__init__(name=name, title=title, description=description, requires=requires, supports_tools=supports_tools, input_schema=_text_schema, output_schema=_text_schema)

        if  supports_tools and response_adapter == None:
            raise RoomException("A response adapter must be provided to enable tools")
        
        self._response_adapter = response_adapter
        if toolkits == None:
            toolkits = []

        self._toolkits = toolkits
        if rules == None:
            rules = []
        self._rules = rules

    async def ask(self, *, context, arguments):

        await context.room.messaging.enable()
        context.toolkits.extend(self._toolkits)

        rules = self._rules

        class MySystemPrompt(SystemPrompt):
            def important_rules(self) -> str:
                # Get existing rules from parent class
                existing_rules = super().important_rules()

                # Add your custom rules
                new_rules = "\n".join(rules)+"n"

                # Make sure to use this pattern otherwise the exiting rules will be lost
                return f'{existing_rules}\n{new_rules}'
        
        async with BrowserbaseContext(
            api_key=os.getenv("BROWSERBASE_API_KEY"),
            project_id=os.getenv("BROWSERBASE_PROJECT_ID")
        ) as browser_context:

            controller = Controller()
            
            if self._response_adapter != None:
                actions = get_registered_actions_from_context(context=context,response_adapter=self._response_adapter)
                for action in actions:
                    controller.registry.registry.actions[action.name] = action

            agent = Agent(
                task = arguments["text"],
                controller=controller,
                system_prompt_class=MySystemPrompt,
                browser = Browser(config=BrowserConfig(
                    cdp_url=( await browser_context.ensure_session()).connect_url
                )),
                llm = ChatOpenAI(model="gpt-4o"),
            )

            # log connection info
            await context.room.developer.log(type="browserbase.started", data={ "live_view_url" : await browser_context.get_live_url() })

            result = await agent.run()
            text = result.final_result()
            if text == None:
                raise RoomException("The agent was unable to complete the task successfully")

            return {
                "text" :  text
            }