@echo off
REM Run Memegen MCP Server in Docker (includes Memegen API)

echo Starting Memegen MCP Server in Docker...
echo This includes both Memegen API and MCP server
echo.
echo Memegen API will be accessible at: http://localhost:5000
echo Press Ctrl+C to stop
echo.

docker run -i --rm -p 5000:5000 memegen-mcp

