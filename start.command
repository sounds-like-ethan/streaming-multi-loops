#!/usr/bin/env bash
# Mac launcher for Soundscape Player.
# Double-click in Finder to start a local server and open the player in your browser.

set -e
cd "$(dirname "$0")"

PORT="${PORT:-8765}"
URL="http://localhost:$PORT"

echo "Starting Soundscape Player at $URL"
echo "Project folder: $(pwd)"
echo
echo "Close this Terminal window to stop the server."
echo

# Pick the first available Python.
if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  echo "ERROR: No python found. Install Python 3 from https://python.org and try again."
  read -n 1 -s -r -p "Press any key to close..."
  exit 1
fi

# Open browser shortly after server starts.
( sleep 1 && open "$URL" ) &

exec "$PY" -m http.server "$PORT"
