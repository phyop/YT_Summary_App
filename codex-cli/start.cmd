@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title YouTube Summary App - Codex CLI

where py >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python 3.11 or newer is required.
  echo Download it from https://www.python.org/downloads/
  pause
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo [1/3] Creating the private Python environment...
  py -3 -m venv .venv || goto :failed
)

echo [2/3] Installing or updating app dependencies...
".venv\Scripts\python.exe" -m pip install --disable-pip-version-check -q -r requirements.txt || goto :failed

set "CODEX_CLI_PATH="
if exist "%APPDATA%\npm\codex.cmd" set "CODEX_CLI_PATH=%APPDATA%\npm\codex.cmd"
if defined CODEX_CLI_PATH goto :check_login

codex --version >nul 2>nul
if not errorlevel 1 (
  set "CODEX_CLI_PATH=codex"
  goto :check_login
)

where npm >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Codex CLI is unavailable and Node.js/npm is not installed.
  echo Install Node.js LTS from https://nodejs.org/ then run this file again.
  pause
  exit /b 1
)

echo [3/3] Installing the official Codex CLI once...
call npm install -g @openai/codex || goto :failed
set "CODEX_CLI_PATH=%APPDATA%\npm\codex.cmd"

:check_login
call "%CODEX_CLI_PATH%" login status >nul 2>nul
if errorlevel 1 (
  echo.
  echo A browser window will open. Sign in with the ChatGPT account that has Codex access.
  call "%CODEX_CLI_PATH%" login || goto :failed
)

echo Starting the app at http://127.0.0.1:8765
".venv\Scripts\python.exe" app.py
exit /b %errorlevel%

:failed
echo.
echo Setup did not finish. Review the message above, then run start.cmd again.
pause
exit /b 1
