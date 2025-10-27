#!/usr/bin/env python3
"""
Memegen MCP Server

A Model Context Protocol server that provides meme generation capabilities.
Allows AI assistants to list templates, get template details, and generate memes.
"""

import asyncio
import json
import logging
import os
from pathlib import Path
from typing import Any

import httpx
from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("memegen-mcp")

# MCP Server configuration
app = Server("memegen")

# Memegen API configuration
MEMEGEN_BASE_URL = os.environ.get("MEMEGEN_BASE_URL", "http://localhost:5000")
REQUEST_TIMEOUT = 30.0


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools for meme generation."""
    return [
        Tool(
            name="list_templates",
            description=(
                "List all available meme templates. "
                "Returns a list of templates with their IDs, names, and example URLs. "
                "Optionally filter by name/keyword or limit to animated templates only."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "filter": {
                        "type": "string",
                        "description": "Part of the name, keyword, or example to match",
                    },
                    "animated": {
                        "type": "boolean",
                        "description": "If true, only return templates that support animation",
                    },
                },
            },
        ),
        Tool(
            name="get_template",
            description=(
                "Get detailed information about a specific meme template by its ID. "
                "Returns template metadata including name, line count, styles, and example."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "template_id": {
                        "type": "string",
                        "description": "The ID of the meme template (e.g., 'fry', 'drake', 'buzz')",
                    },
                },
                "required": ["template_id"],
            },
        ),
        Tool(
            name="generate_meme",
            description=(
                "Generate a meme image using a template and custom text. "
                "Returns the URL of the generated meme image. "
                "Text lines can include special characters using tilde patterns "
                "(~n for newline, ~q for ?, ~a for &, etc.). "
                "Use underscores or dashes for spaces."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "template_id": {
                        "type": "string",
                        "description": "The ID of the meme template to use",
                    },
                    "text_lines": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Array of text lines for the meme (use _ or - for spaces)",
                    },
                    "extension": {
                        "type": "string",
                        "description": "Image format: png, jpg, gif, or webp (default: png)",
                    },
                    "style": {
                        "type": "string",
                        "description": "Template style variant (optional)",
                    },
                    "font": {
                        "type": "string",
                        "description": "Font name (e.g., 'thick', 'comic', 'impact')",
                    },
                    "layout": {
                        "type": "string",
                        "description": "Text layout position: default or top",
                    },
                },
                "required": ["template_id", "text_lines"],
            },
        ),
        Tool(
            name="generate_custom_meme",
            description=(
                "Generate a meme using a custom background image from a URL. "
                "Allows you to create memes with any image as the background."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "background_url": {
                        "type": "string",
                        "description": "URL of the custom background image",
                    },
                    "text_lines": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Array of text lines for the meme",
                    },
                    "extension": {
                        "type": "string",
                        "description": "Image format: png, jpg, gif, or webp (default: png)",
                    },
                    "font": {
                        "type": "string",
                        "description": "Font name (e.g., 'thick', 'comic', 'impact')",
                    },
                },
                "required": ["background_url", "text_lines"],
            },
        ),
        Tool(
            name="search_meme_examples",
            description=(
                "Search for example memes by filtering templates based on keywords. "
                "Useful for finding inspiration or specific meme formats."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query to filter meme examples",
                    },
                },
                "required": ["query"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool execution requests."""
    
    # Log ALL incoming requests with full details
    logger.error(f"=" * 80)
    logger.error(f"TOOL CALL: {name}")
    logger.error(f"ARGUMENTS: {json.dumps(arguments, indent=2)}")
    logger.error(f"ARGUMENTS TYPE: {type(arguments)}")
    logger.error(f"=" * 80)
    
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            
            if name == "list_templates":
                return await handle_list_templates(client, arguments)
            
            elif name == "get_template":
                return await handle_get_template(client, arguments)
            
            elif name == "generate_meme":
                return await handle_generate_meme(client, arguments)
            
            elif name == "generate_custom_meme":
                return await handle_generate_custom_meme(client, arguments)
            
            elif name == "search_meme_examples":
                return await handle_search_examples(client, arguments)
            
            else:
                logger.error(f"UNKNOWN TOOL: {name}")
                return [TextContent(type="text", text=f"Unknown tool: {name}")]
                
    except httpx.TimeoutException:
        logger.error("TIMEOUT ERROR")
        return [TextContent(
            type="text",
            text="Error: Request timed out. Make sure the Memegen server is running."
        )]
    except httpx.ConnectError:
        logger.error("CONNECTION ERROR")
        return [TextContent(
            type="text",
            text=f"Error: Cannot connect to Memegen server at {MEMEGEN_BASE_URL}. "
                 "Make sure it's running (use start.bat or start_app.bat)."
        )]
    except Exception as e:
        logger.exception("EXCEPTION IN TOOL HANDLER")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_list_templates(client: httpx.AsyncClient, args: dict) -> list[TextContent]:
    """Handle the list_templates tool."""
    params = {}
    if "filter" in args:
        params["filter"] = args["filter"]
    if "animated" in args:
        params["animated"] = "1" if args["animated"] else "0"
    
    response = await client.get(f"{MEMEGEN_BASE_URL}/templates/", params=params)
    response.raise_for_status()
    
    templates = response.json()
    
    # Format the response
    result = f"Found {len(templates)} template(s):\n\n"
    for template in templates[:50]:  # Limit to 50 to avoid overwhelming output
        result += f"• **{template['name']}** (ID: `{template['id']}`)\n"
        result += f"  Lines: {template['lines']}"
        if template.get('styles'):
            result += f" | Styles: {', '.join(template['styles'])}"
        result += f"\n  Example: {template['example']['url']}\n\n"
    
    if len(templates) > 50:
        result += f"... and {len(templates) - 50} more templates.\n"
        result += "Use the 'filter' parameter to narrow down results.\n"
    
    return [TextContent(type="text", text=result)]


async def handle_get_template(client: httpx.AsyncClient, args: dict) -> list[TextContent]:
    """Handle the get_template tool."""
    template_id = args["template_id"]
    
    response = await client.get(f"{MEMEGEN_BASE_URL}/templates/{template_id}")
    
    if response.status_code == 404:
        return [TextContent(
            type="text",
            text=f"Template '{template_id}' not found. Use 'list_templates' to see available templates."
        )]
    
    response.raise_for_status()
    template = response.json()
    
    # Format detailed template info
    result = f"# {template['name']}\n\n"
    result += f"**ID:** `{template['id']}`\n"
    result += f"**Text Lines:** {template['lines']}\n"
    result += f"**Overlays:** {template.get('overlays', 0)}\n"
    
    if template.get('styles'):
        result += f"**Available Styles:** {', '.join(template['styles'])}\n"
    
    result += f"\n**Blank Template:** {template['blank']}\n"
    result += f"\n**Example:**\n"
    result += f"Text: {' / '.join(template['example']['text'])}\n"
    result += f"URL: {template['example']['url']}\n"
    
    if template.get('source'):
        result += f"\n**Source:** {template['source']}\n"
    
    if template.get('keywords'):
        result += f"**Keywords:** {', '.join(template['keywords'])}\n"
    
    return [TextContent(type="text", text=result)]


async def handle_generate_meme(client: httpx.AsyncClient, args: dict) -> list[TextContent]:
    """Handle the generate_meme tool."""
    template_id = args["template_id"]
    text_lines = args.get("text_lines", [])
    extension = args.get("extension", "png")
    
    # Validate text_lines is a list
    if not isinstance(text_lines, list):
        return [TextContent(
            type="text",
            text=f"Error: text_lines must be an array of strings, got {type(text_lines).__name__}"
        )]
    
    # Convert all text lines to strings and validate
    text_lines = [str(line).strip() for line in text_lines if line]
    
    if not text_lines:
        return [TextContent(
            type="text",
            text="Error: text_lines cannot be empty. Provide at least one non-empty line."
        )]
    
    # Build the URL path (Memegen will handle URL encoding)
    text_path = "/".join(text_lines)
    url_path = f"{MEMEGEN_BASE_URL}/images/{template_id}/{text_path}.{extension}"
    
    logger.info(f"Generating meme: {url_path}")
    
    # Add query parameters
    params = {}
    if "style" in args:
        params["style"] = args["style"]
    if "font" in args:
        params["font"] = args["font"]
    if "layout" in args:
        params["layout"] = args["layout"]
    
    # Make a HEAD request to check if the meme can be generated
    response = await client.head(url_path, params=params, follow_redirects=True)
    
    if response.status_code == 404:
        return [TextContent(
            type="text",
            text=f"Template '{template_id}' not found. Use 'list_templates' to see available templates."
        )]
    elif response.status_code >= 400:
        return [TextContent(
            type="text",
            text=f"Error generating meme (status {response.status_code}). Check your parameters."
        )]
    
    # Build the final URL with params
    final_url = str(response.url)
    
    # Make URL accessible from outside container
    # Replace internal localhost:5000 with external accessible URL
    if final_url.startswith("http://localhost:5000"):
        # Keep localhost:5000 - it will be accessible if port is published
        accessible_url = final_url
    else:
        accessible_url = final_url
    
    result = f"✅ Meme generated successfully!\n\n"
    result += f"**Template:** {template_id}\n"
    result += f"**Text:** {' / '.join(text_lines)}\n"
    result += f"**URL:** {accessible_url}\n\n"
    result += f"View your meme at: {accessible_url}"
    
    return [TextContent(type="text", text=result)]


async def handle_generate_custom_meme(client: httpx.AsyncClient, args: dict) -> list[TextContent]:
    """Handle the generate_custom_meme tool."""
    background_url = args["background_url"]
    text_lines = args.get("text_lines", [])
    extension = args.get("extension", "png")
    
    # Validate text_lines is a list
    if not isinstance(text_lines, list):
        return [TextContent(
            type="text",
            text=f"Error: text_lines must be an array of strings, got {type(text_lines).__name__}"
        )]
    
    # Convert all text lines to strings and validate
    text_lines = [str(line).strip() for line in text_lines if line]
    
    if not text_lines:
        return [TextContent(
            type="text",
            text="Error: text_lines cannot be empty. Provide at least one non-empty line."
        )]
    
    # Build the URL path for custom template
    text_path = "/".join(text_lines)
    url_path = f"{MEMEGEN_BASE_URL}/images/custom/{text_path}.{extension}"
    
    logger.info(f"Generating custom meme: {url_path}")
    
    # Add query parameters
    params = {"background": background_url}
    if "font" in args:
        params["font"] = args["font"]
    
    # Make a HEAD request to check if the meme can be generated
    response = await client.head(url_path, params=params, follow_redirects=True)
    
    if response.status_code >= 400:
        return [TextContent(
            type="text",
            text=f"Error generating custom meme (status {response.status_code}). "
                 "Check that the background URL is valid and accessible."
        )]
    
    final_url = str(response.url)
    
    # Make URL accessible from outside container
    if final_url.startswith("http://localhost:5000"):
        # Keep localhost:5000 - it will be accessible if port is published
        accessible_url = final_url
    else:
        accessible_url = final_url
    
    result = f"✅ Custom meme generated successfully!\n\n"
    result += f"**Background:** {background_url}\n"
    result += f"**Text:** {' / '.join(text_lines)}\n"
    result += f"**URL:** {accessible_url}\n\n"
    result += f"View your meme at: {accessible_url}"
    
    return [TextContent(type="text", text=result)]


async def handle_search_examples(client: httpx.AsyncClient, args: dict) -> list[TextContent]:
    """Handle the search_meme_examples tool."""
    query = args["query"]
    
    response = await client.get(f"{MEMEGEN_BASE_URL}/images/", params={"filter": query})
    response.raise_for_status()
    
    examples = response.json()
    
    if not examples:
        return [TextContent(
            type="text",
            text=f"No examples found matching '{query}'. Try a different search term."
        )]
    
    result = f"Found {len(examples)} example(s) matching '{query}':\n\n"
    for example in examples[:20]:  # Limit to 20
        result += f"• **{example['template']}**\n"
        result += f"  {example['url']}\n\n"
    
    if len(examples) > 20:
        result += f"... and {len(examples) - 20} more examples.\n"
    
    return [TextContent(type="text", text=result)]


async def main():
    """Run the MCP server."""
    from mcp.server.stdio import stdio_server
    
    logger.info("Starting Memegen MCP Server...")
    logger.info(f"Memegen API: {MEMEGEN_BASE_URL}")
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

