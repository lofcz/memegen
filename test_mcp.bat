@echo off
REM Test the Memegen MCP Server functionality

echo Testing Memegen MCP Server...
echo.
echo Make sure Memegen is running (start.bat or start_app.bat)
echo.

python test_mcp.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Tests failed!
    pause
    exit /b %ERRORLEVEL%
)

pause

