import os
import pathlib
from typing import Any, Dict

import setuptools  # type: ignore

here = pathlib.Path(__file__).parent.resolve()
about: Dict[Any, Any] = {}
with open(os.path.join(here, "version.py"), "r") as f:
    exec(f.read(), about)

setuptools.setup(
    name="meshagent-browserbase",
    version=about["__version__"],
    description="Browserbase support for Meshagent",
    long_description=(here / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="",
    classifiers=[       
    ],
    keywords=[],
    license="MIT",
    packages=setuptools.find_namespace_packages(include=[
        "meshagent.*",        
    ]),
    python_requires=">=3.9.0",
    install_requires=[
        "pytest>=8.3.4",
        "pytest-asyncio>=0.24.0",
        "meshagent-api>=0.0.1",
        "meshagent-tools>=0.0.1",
        "meshagent-agents>=0.0.1",
        "browserbase>=1.0.5",
        "playwright>=1.48.0",
        "browser-use>=0.1.36",
        "langchain-openai>=0.3.1",
    ],
    package_data={
        "meshagent.browserbase": ["py.typed", "*.pyi", "**/*.pyi",  "**/*.js"],
    },
    project_urls={
        "Documentation": "https://meshagent.com",
        "Website": "https://meshagent.com",
        "Source": "https://github.com/meshagent",
    },
)
