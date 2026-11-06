# OCR KTP

A small Streamlit demo for extracting visible fields from an Indonesian KTP into JSON. It supports Apple's native on-device Foundation Models, an OpenAI-compatible local vision-model API (for example, Ollama on a Mac), and Azure OpenAI. Model output is unverified; always compare it with the original document.

## Quick start

Requires Python 3.10+.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.final.example .env
streamlit run app.py
```

## Recommended Mac setup

### Option A: native Apple model (preferred if you have macOS 26+)

For Apple silicon with macOS 26+, use the native Apple mode. This keeps OCR and structuring local on the Mac. It does not require a URL or API key.

```bash
xcode-select --install
streamlit run app.py
```

Then select: "Apple Foundation Models (on this Mac)" in the app.

### Option B: local OpenAI-compatible server (Ollama)

Use your local Mac server if you prefer an OpenAI-compatible API route.

Example `.env`:

```env
LOCAL_OPENAI_BASE_URL=http://localhost:11434/v1
LOCAL_OPENAI_API_KEY=ollama
LOCAL_OPENAI_MODEL=qwen2.5vl:3b
```

Install Ollama and pull the model:

```bash
brew install ollama
ollama pull qwen2.5vl:3b
ollama list
```

Then confirm the server is up:

```bash
curl http://localhost:11434/v1/models
```

### Option C: Azure OpenAI

Only use Azure if you already have a resource and a valid deployment name.

```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_API_VERSION=2025-01-01-preview
AZURE_OPENAI_DEPLOYMENT=gpt-4.1-mini
```

## Privacy and safety

- KTP contains sensitive personal data. Use only documents you are authorized to process.
- Native Apple mode keeps the data on-device.
- Local API mode sends the image to `LOCAL_OPENAI_BASE_URL`; verify that server is private and trusted.
- Azure mode sends the image to your Azure endpoint and must follow your privacy, retention, and security policy.
- Always manually review the extracted result before using it for identity, compliance, or eligibility decisions.

## Run checks

```bash
python -m unittest discover -s tests -v
./scripts/validate_local_ocr.sh
```

## Layout

```text
app.py
services/
helpers/
scripts/
tests/
.env.final.example
```
