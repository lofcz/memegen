"""
Setup script for Memegen MCP Server
Allows distribution via PyPI (pip install memegen-mcp-server)
"""

from setuptools import setup

with open("MCP_README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="memegen-mcp-server",
    version="1.0.0",
    description="MCP server for Memegen API - Generate memes programmatically via AI assistants",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Memegen Contributors",
    author_email="support@maketested.com",
    url="https://github.com/jacebrowning/memegen",
    py_modules=["mcp_server"],
    install_requires=[
        "mcp>=1.0.0",
        "httpx>=0.27.0",
    ],
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "memegen-mcp-server=mcp_server:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    keywords="mcp model-context-protocol meme memegen ai assistant claude",
    project_urls={
        "Documentation": "https://github.com/jacebrowning/memegen/blob/main/MCP_README.md",
        "Source": "https://github.com/jacebrowning/memegen",
        "Tracker": "https://github.com/jacebrowning/memegen/issues",
    },
)

