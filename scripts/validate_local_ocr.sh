# Quick local OCR validation for Mac + Ollama
# Run this from the project root.

set -e

printf '\n[1/3] Checking local server...\n'
curl -sS http://localhost:11434/v1/models || {
  echo "Local Ollama server is not reachable on http://localhost:11434/v1";
  echo "Start it with: ollama serve";
  exit 1;
}

printf '\n[2/3] Checking installed models...\n'
ollama list

printf '\n[3/3] Suggested model for OCR KTP on M3 16GB...\n'
echo "Recommended first try: qwen2.5vl:3b"
echo "Heavier alternative: qwen2.5vl:7b"
echo "Native Apple option: use macOS 26+ + Apple Foundation Models"
printf '\nEdit .env to use:\n'
printf 'LOCAL_OPENAI_BASE_URL=http://localhost:11434/v1\n'
printf 'LOCAL_OPENAI_MODEL=qwen2.5vl:3b\n'
