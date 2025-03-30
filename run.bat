@echo off
echo Running Keep Speaker On application...

REM Activate virtual environment
call %~dp0\venv\Scripts\activate.bat

REM Run the application
call python main.py

REM Keep the window open if there's an error
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo An error occurred. Press any key to exit.
    pause > nul
)

REM Deactivate virtual environment
deactivate
