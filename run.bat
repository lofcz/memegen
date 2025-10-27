@echo off
REM Memegen Docker Runner
REM This script builds and runs the memegen Docker container

call build.bat

if %ERRORLEVEL% NEQ 0 (
    exit /b %ERRORLEVEL%
)

call start.bat

