# Memegen MCP Server - Quick Start Guide

## 🚀 5-Minute Setup

### Step 1: Install Dependencies
```bash
.\install_mcp.bat
```

### Step 2: Start Memegen
```bash
.\start.bat
```
Leave this terminal window open.

### Step 3: Test the MCP Server
Open a **new** terminal and run:
```bash
.\test_mcp.bat
```

If all tests pass ✅, you're ready!

### Step 4: Start the MCP Server
```bash
.\start_mcp.bat
```

---

## 📋 All Available Commands

### Memegen Application
- `build.bat` - Build the Docker image
- `start.bat` - Start Memegen (quick start, no rebuild)
- `start_app.bat` - Alternative start script
- `run.bat` - Build and start (all-in-one)
- `publish.bat` - Publish Docker image to Docker Hub

### MCP Server
- `install_mcp.bat` - Install MCP dependencies
- `test_mcp.bat` - Test MCP server functionality
- `start_mcp.bat` - Start the MCP server
- `publish_mcp.bat` - Publish MCP server to PyPI/npm

---

## 🔧 Using with Claude Desktop

1. **Find your config file:**
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`

2. **Add this configuration:**
   ```json
   {
     "mcpServers": {
       "memegen": {
         "command": "python",
         "args": ["C:\\Path\\To\\memegen\\mcp_server.py"]
       }
     }
   }
   ```
   
   Replace `C:\\Path\\To\\memegen\\` with your actual path.

3. **Restart Claude Desktop**

4. **Test it:**
   - Ask Claude: "List all meme templates"
   - Ask Claude: "Create a 'fry' meme that says 'Testing MCP' and 'It works!'"

---

## 💡 Example Prompts

Once configured with Claude Desktop, try these:

### List Templates
```
Show me all available meme templates
List memes related to "coding"
What animated meme templates are available?
```

### Generate Memes
```
Create a "drake" meme with "Manual work" and "Automation"
Make a "buzz" meme saying "Memes" and "Memes everywhere"
Generate a "fry" meme about being unsure if something is a bug or a feature
```

### Get Template Info
```
Tell me about the "doge" template
What styles are available for the "ds" template?
Show me details for the "oprah" template
```

### Custom Memes
```
Create a meme using https://example.com/image.jpg with text "Hello" and "World"
```

---

## 🐛 Troubleshooting

### "Cannot connect to Memegen server"
**Fix:** Make sure Memegen is running:
```bash
.\start.bat
```

### "Module 'mcp' not found"
**Fix:** Install dependencies:
```bash
.\install_mcp.bat
```

### Claude Desktop doesn't see the tools
**Fixes:**
1. Check the config file path is correct (use double backslashes `\\`)
2. Restart Claude Desktop completely
3. Check that Memegen is running (`.\start.bat`)
4. Verify MCP server works: `.\test_mcp.bat`

### Port 5000 already in use
**Fix:** Edit `start.bat` to use a different port, and update the MCP server configuration.

---

## 📚 More Information

- **Full Documentation:** See `MCP_README.md`
- **Main Memegen Docs:** See `README.md`
- **Contributing:** See `CONTRIBUTING.md`

---

## 🎯 What Can You Do?

With the MCP server, AI assistants can:
- ✅ List 500+ meme templates
- ✅ Generate memes with custom text
- ✅ Create custom memes from any image
- ✅ Search for meme examples
- ✅ Get template details and styles
- ✅ No watermarks (if configured)

All without leaving the chat interface!

---

## 📞 Need Help?

1. Check `MCP_README.md` for detailed documentation
2. Run `.\test_mcp.bat` to diagnose issues
3. Visit the [MCP Documentation](https://modelcontextprotocol.io/)
4. Check [Memegen GitHub Issues](https://github.com/jacebrowning/memegen/issues)

