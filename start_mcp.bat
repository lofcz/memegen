@echo off
REM Start the Memegen MCP Server

echo Starting Memegen MCP Server...
echo.
echo Make sure the Memegen application is running first!
echo If not, run 'start.bat' or 'start_app.bat' in another window.
echo.
echo Press Ctrl+C to stop the MCP server.
echo.

python mcp_server.py

