@echo off
REM Build Memegen MCP Server Docker image

echo Building Memegen MCP Server Docker image...
docker build --tag memegen-mcp --file Containerfile.mcp .

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Docker build failed!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Build completed successfully!
echo.
echo To test locally:
echo   docker run -i --rm memegen-mcp
echo.
echo To publish:
echo   run publish_mcp.bat
pause

