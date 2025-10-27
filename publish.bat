@echo off
REM Memegen Docker Hub Publisher
REM This script builds, tags, and pushes the memegen image to Docker Hub

echo ====================================
echo Memegen Docker Hub Publisher
echo ====================================
echo.

REM Prompt for Docker Hub username
set /p DOCKERHUB_USERNAME="Enter your Docker Hub username: "

if "%DOCKERHUB_USERNAME%"=="" (
    echo ERROR: Username cannot be empty!
    pause
    exit /b 1
)

echo.
echo Step 1/4: Building image...
call build.bat

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Build failed!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Step 2/4: Tagging image as %DOCKERHUB_USERNAME%/memegen:latest
docker tag memegen %DOCKERHUB_USERNAME%/memegen:latest

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
docker push %DOCKERHUB_USERNAME%/memegen:latest

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Push failed!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ====================================
echo SUCCESS! Image published to Docker Hub
echo Image: %DOCKERHUB_USERNAME%/memegen:latest
echo.
echo Others can now pull your image with:
echo   docker pull %DOCKERHUB_USERNAME%/memegen:latest
echo ====================================
pause

