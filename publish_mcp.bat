@echo off
REM Build and publish Memegen MCP Server Docker image

echo ====================================
echo Memegen MCP Server Docker Publisher
echo ====================================
echo.

set /p DOCKERHUB_USERNAME="Enter your Docker Hub username: "

if "%DOCKERHUB_USERNAME%"=="" (
    echo ERROR: Username cannot be empty!
    pause
    exit /b 1
)

echo.
echo Step 1/4: Building MCP server Docker image...
docker build --tag memegen-mcp --file Containerfile.mcp .

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Build failed!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Step 2/4: Tagging image as %DOCKERHUB_USERNAME%/memegen-mcp:latest
docker tag memegen-mcp %DOCKERHUB_USERNAME%/memegen-mcp:latest

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Tagging failed!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Step 3/4: Logging into Docker Hub...
docker login

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Login failed!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Step 4/4: Pushing to Docker Hub...
docker push %DOCKERHUB_USERNAME%/memegen-mcp:latest

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Push failed!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ====================================
echo SUCCESS! MCP Server published to Docker Hub
echo Image: %DOCKERHUB_USERNAME%/memegen-mcp:latest
echo.
echo Usage in C#:
echo   var server = new MCPServer("memegen",
echo       command: "docker",
echo       arguments: new[] { "run", "-i", "--rm", "%DOCKERHUB_USERNAME%/memegen-mcp:latest" });
echo.
echo Usage in CLI:
echo   docker run -i --rm %DOCKERHUB_USERNAME%/memegen-mcp:latest
echo.
echo Note: This image includes BOTH Memegen API and MCP server - no setup required!
echo ====================================
pause

