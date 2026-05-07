@echo off
REM Windows launcher for Soundscape Player.
REM Double-click in Explorer to start a local server and open the player.

cd /d "%~dp0"

set PORT=8765
set URL=http://localhost:%PORT%

echo Starting Soundscape Player at %URL%
echo Project folder: %CD%
echo.
echo Close this window to stop the server.
echo.

start "" "%URL%"

where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
  python -m http.server %PORT%
) else (
  where py >nul 2>&1
  if %ERRORLEVEL% EQU 0 (
    py -3 -m http.server %PORT%
  ) else (
    echo ERROR: Python is not installed. Get it from https://python.org and try again.
    pause
  )
)
