#!/usr/bin/env bash
set -euo pipefail

python3 --version >/dev/null 2>&1 || { echo "Python 3 is required."; exit 1; }

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env from .env.example"
fi

cat <<'EOF'

Setup complete.

Next steps:
1. Edit .env if you want Azure or a local OpenAI-compatible endpoint.
2. For local Ollama use:
   - LOCAL_OPENAI_BASE_URL=http://localhost:11434/v1
   - LOCAL_OPENAI_MODEL=<vision-capable model name>
3. Start the app:
   streamlit run app.py

For native Apple mode on macOS 26+:
- install Xcode Command Line Tools with: xcode-select --install
- then choose "Apple Foundation Models (on this Mac)" in the app
EOF
