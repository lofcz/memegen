@echo off
REM Memegen Docker Build Script
REM This script builds the memegen Docker image

echo Building memegen Docker image...
docker build --tag memegen --file Containerfile .

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Docker build failed!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Build completed successfully!
echo Run 'start.bat' to start the container.
pause

