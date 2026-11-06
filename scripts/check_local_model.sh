#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${LOCAL_OPENAI_BASE_URL:-http://localhost:11434/v1}"

if command -v curl >/dev/null 2>&1; then
  echo "Checking local endpoint: $BASE_URL"
  curl -sS -m 10 "$BASE_URL/models" || true
else
  echo "curl not installed; skipping endpoint check."
fi

echo
printf '%s
' "If this is an Ollama server, run:"
printf '%s
' "  ollama list"
printf '%s
' "and use a model that supports image input, for example: llava, qwen2.5vl, or a similar vision-capable model installed on your machine."
printf '%s
' "Make sure LOCAL_OPENAI_MODEL matches the exact model name in your local server."
