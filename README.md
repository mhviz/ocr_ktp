# OCR KTP

A small Streamlit demo for extracting visible fields from an Indonesian KTP into JSON. Choose Apple's native on-device Foundation Models, an OpenAI-compatible local vision-model API, or Azure OpenAI. Model output is unverified—always compare it with the original document.

## Quick start (Mac)

Requires Python 3.10+. For Apple's native model, also requires Apple silicon, macOS 26+, Swift/Xcode Command Line Tools, and an available on-device model.

```bash
xcode-select --install  # once; required for native Apple mode
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

For convenience, you can also run:

```bash
chmod +x setup.sh
./setup.sh
```

Open the local Streamlit URL shown in the terminal. The native Apple option needs no `.env` provider settings. It uses Vision for OCR and sends recognized text—not the image—to Apple's on-device Foundation Model; it does not fall back to a cloud service.

## Local API example (Ollama)

This repository is configured to work with:

```env
LOCAL_OPENAI_BASE_URL=http://localhost:11434/v1
```

In `.env`, set `LOCAL_OPENAI_MODEL` to the exact name of a model installed in your local server and known to support image input. For Ollama, first inspect models on the machine:

```bash
ollama list
```

Common examples of vision-capable local models include `llava`, `qwen2.5vl`, or other model names that explicitly support multimodal/image input. Use the exact model name shown by your server; do not guess a name that is not installed.

This mode sends the image to the configured endpoint. Confirm the local server does not forward requests elsewhere. A local-looking URL alone is not a privacy guarantee. The native Apple Foundation Models option is separate and does not use this URL.

## Other providers

- **Azure OpenAI:** set `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_API_VERSION`, and `AZURE_OPENAI_DEPLOYMENT` in `.env`. The document image is sent to that Azure endpoint.
- **Apple on-device:** no provider URL or API key required.

Only configure credentials for providers you use. Never commit `.env` or real secrets.

## Input, privacy, and limitations

- Accepts JPEG, PNG, and PDF up to 10 MB. PDFs are limited to 20 pages; only the first page is processed. Images are resized before inference.
- Use only documents you are authorized to process. KTP contains sensitive personal information; use synthetic or redacted examples for development.
- Apple native mode performs OCR and text structuring on-device. Local API mode sends the image to its configured server. Azure mode sends the image to the configured Azure resource.
- The app does not intentionally save uploads/results or print extraction results to logs, but hosting software, providers, and model servers may have their own logs or retention. Do not deploy this demo as a public service: it has no user authentication or production data-retention controls.
- OCR/LLM output can be wrong. This demo does not authenticate KTPs, verify NIKs, or replace human review. Do not use it to make identity or eligibility decisions.

## Suggested local model check

If you are using a local OpenAI-compatible server, verify the model and endpoint before running the app:

```bash
./scripts/check_local_model.sh
```

This script checks your local server and prints a reminder about vision-capable model names.

## Tests and layout

```bash
python -m unittest discover -s tests -v
```

```text
app.py                         Streamlit UI and provider selection
services/ocr.py                Upload validation, OCR/model calls, output validation
services/apple_foundation_model.swift  Native macOS Vision + Foundation Models runner
helpers/                        Compatibility/legacy helper modules
scripts/                        Setup and local-server helper scripts
tests/                          Unit tests
.env.example                    Safe configuration template
setup.sh                        One-click local setup for Python environment
```

See [SECURITY.md](SECURITY.md) for security and privacy reporting guidance.
