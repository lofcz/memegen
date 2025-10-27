@echo off
REM Install MCP Server Dependencies

echo Installing Memegen MCP Server dependencies...
python -m pip install --upgrade pip
python -m pip install -r mcp_requirements.txt

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Failed to install dependencies!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ====================================
echo MCP Server dependencies installed!
echo ====================================
echo.
echo Next steps:
echo 1. Make sure Memegen is running: start.bat or start_app.bat
echo 2. Test the MCP server: python mcp_server.py
echo.
echo To use with Claude Desktop or other MCP clients,
echo add the configuration from mcp_server_config.json
echo to your MCP client's configuration file.
echo.
pause

