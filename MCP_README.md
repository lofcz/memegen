# Memegen MCP Server

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that provides meme generation capabilities to AI assistants like Claude.

## 🎯 What is This?

This MCP server exposes the Memegen API as a set of tools that AI assistants can use to:
- List available meme templates
- Get details about specific templates
- Generate memes with custom text
- Create custom memes from any image URL
- Search for meme examples

## 🚀 Quick Start

### Prerequisites

1. **Python 3.13+** installed
2. **Memegen application running** on `http://localhost:5000`

### Installation

1. **Install MCP server dependencies:**
```bash
.\install_mcp.bat
```

Or manually:
```bash
pip install -r mcp_requirements.txt
```

2. **Start the Memegen application** (in a separate terminal):
```bash
.\start.bat
# or
.\start_app.bat
```

3. **Start the MCP server:**
```bash
.\start_mcp.bat
```

Or manually:
```bash
python mcp_server.py
```

## 🔧 Configuration

### Using with Claude Desktop

Add this to your Claude Desktop configuration file:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "memegen": {
      "command": "python",
      "args": ["C:\\Users\\YourUsername\\Documents\\GitHub\\memegen\\mcp_server.py"],
      "env": {
        "MEMEGEN_BASE_URL": "http://localhost:5000"
      }
    }
  }
}
```

**Important:** Replace `C:\\Users\\YourUsername\\Documents\\GitHub\\memegen\\` with the actual path to your memegen directory.

### Using with Other MCP Clients

The server uses standard MCP protocol over stdio. Configure your MCP client to run:

```bash
python mcp_server.py
```

## 🛠️ Available Tools

### 1. `list_templates`

List all available meme templates.

**Parameters:**
- `filter` (optional): Filter templates by name or keyword
- `animated` (optional): If true, only show templates that support animation

**Example:**
```
List all meme templates
List templates related to "drake"
Show animated meme templates
```

### 2. `get_template`

Get detailed information about a specific template.

**Parameters:**
- `template_id` (required): The template ID (e.g., "fry", "drake", "buzz")

**Example:**
```
Get details for the "fry" template
Show me information about the "drake" template
```

### 3. `generate_meme`

Generate a meme using a template and custom text.

**Parameters:**
- `template_id` (required): The template ID
- `text_lines` (required): Array of text lines for the meme
- `extension` (optional): Image format (png, jpg, gif, webp)
- `style` (optional): Template style variant
- `font` (optional): Font name (thick, comic, impact, etc.)
- `layout` (optional): Text layout (default, top)

**Example:**
```
Create a "fry" meme with "Not sure if AI" and "Or just really smart bot"
Generate a "drake" meme with "Writing code manually" and "Using AI assistance"
Make a "buzz" meme saying "Memes" and "Memes everywhere"
```

### 4. `generate_custom_meme`

Create a meme using any image from a URL.

**Parameters:**
- `background_url` (required): URL of the background image
- `text_lines` (required): Array of text lines
- `extension` (optional): Image format (png, jpg, gif, webp)
- `font` (optional): Font name

**Example:**
```
Create a custom meme using https://example.com/image.jpg with text "Hello" and "World"
```

### 5. `search_meme_examples`

Search for example memes by keyword.

**Parameters:**
- `query` (required): Search query

**Example:**
```
Search for meme examples about "coding"
Find examples matching "AI"
```

## 📝 Text Formatting

When generating memes, text formatting follows these rules:

- **Spaces:** Use `_` (underscore) or `-` (dash) for spaces
- **Special Characters:**
  - `~n` → newline
  - `~q` → question mark (?)
  - `~a` → ampersand (&)
  - `~p` → percentage (%)
  - `~h` → hashtag (#)
  - `~s` → slash (/)
  - `~b` → backslash (\\)
  - `__` → underscore (_)
  - `--` → dash (-)

**Example:**
```
Text: "Hello_World~nHow_are_you~q"
Result: "Hello World
         How are you?"
```

## 🧪 Testing the MCP Server

### Test with MCP Inspector

Use the MCP Inspector tool to test your server:

```bash
npx @modelcontextprotocol/inspector python mcp_server.py
```

### Test Manually

1. Start Memegen: `.\start.bat`
2. Start MCP server: `.\start_mcp.bat`
3. The server will communicate via stdio (standard input/output)

## 🐛 Troubleshooting

### "Cannot connect to Memegen server"

**Solution:** Make sure the Memegen application is running:
```bash
.\start.bat
# or
.\start_app.bat
```

### "Module not found: mcp"

**Solution:** Install dependencies:
```bash
.\install_mcp.bat
```

### "Template not found"

**Solution:** Use `list_templates` to see available templates:
```
Ask your AI assistant: "List all meme templates"
```

### Port Already in Use

If port 5000 is already in use, you can change the Memegen port and update the MCP configuration:

1. Edit `start.bat` or `start_app.bat` to use a different port
2. Update `MEMEGEN_BASE_URL` in the MCP configuration

## 📚 Examples

### Example 1: List Templates
```
User: "List all meme templates"
AI: Uses list_templates tool
Result: Shows all available templates with IDs and examples
```

### Example 2: Generate a Meme
```
User: "Create a 'fry' meme that says 'Not sure if Monday' and 'Or just really tired'"
AI: Uses generate_meme tool with template_id="fry" and text_lines=["Not_sure_if_Monday", "Or_just_really_tired"]
Result: Returns URL to generated meme image
```

### Example 3: Custom Meme
```
User: "Make a meme from this image: https://example.com/cat.jpg with text 'When you hear the treat bag'"
AI: Uses generate_custom_meme tool
Result: Returns URL to custom meme
```

## 🔒 Security Notes

- The MCP server runs locally and only communicates with your local Memegen instance
- No data is sent to external servers (unless you use custom background URLs)
- The server uses stdio for communication (standard MCP pattern)

## 📖 Learn More

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [Memegen API Documentation](http://localhost:5000/docs) (when running)
- [Memegen GitHub Repository](https://github.com/jacebrowning/memegen)

## 🤝 Contributing

This MCP server is part of the Memegen project. Feel free to contribute improvements!

## 📄 License

Same as Memegen - MIT License

