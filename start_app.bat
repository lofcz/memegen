@echo off
REM Memegen Docker Start Script
REM This script runs the memegen Docker container

echo Starting memegen container...
echo Access the application at: http://localhost:5000/
echo Press Ctrl+C to stop the server
echo.

docker run --publish 5000:5000 --env DOMAIN="localhost" memegen

