# Codex CLI Version

This is the recommended version. It uses ChatGPT-authenticated Codex CLI and does not require an OpenAI API key.

## Use

1. Install Python 3.11+.
2. Install Node.js LTS if Codex CLI is not already installed.
3. Double-click `start.cmd`.
4. Complete `codex login` in the browser when prompted.
5. Paste a YouTube URL and press Enter.

The app supports individual videos, Shorts, playlists, and channel video pages. Channel pages process the latest four non-live uploads.

## Manual launch

```powershell
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
npm install -g @openai/codex
codex login
.venv\Scripts\python.exe app.py
```

Set `CODEX_CLI_PATH` only if automatic CLI discovery cannot find your executable.
