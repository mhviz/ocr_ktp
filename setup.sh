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
1. Configure Apple Foundation Models with LOCAL_MAC_* or configure an OpenAI-compatible endpoint with OPENAI_* in .env.
2. Start the app:
   streamlit run app.py

For native Apple Foundation Models:
- install Xcode Command Line Tools with: xcode-select --install
- leave LOCAL_MAC_URL blank and choose Apple Foundation Models in the app
EOF
