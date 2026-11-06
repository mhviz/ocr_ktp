# OCR KTP

**A local-first document-AI prototype for extracting visible fields from Indonesian identity cards into structured JSON.** The project explores on-device Apple Foundation Models, OpenAI-compatible local vision APIs, and optional Azure OpenAI.

> **Status: prototype.** Extraction is not guaranteed accurate, KTP authenticity is not checked, and this is not a production identity-verification system. Always verify results against the source document.

## Demo

<!-- Add a screenshot only after capturing it with synthetic or fully redacted sample data. -->

_Add a sanitized screenshot here, for example `docs/images/app-demo.png`._

The app flow is designed to let a user select a processing option, provide an image or PDF, and inspect structured field output. Do not publish screenshots containing real names, NIKs, addresses, faces, API keys, or other personal data.

## Project highlights

- Indonesian KTP field extraction into a structured format
- Exploration of local-first document AI on Apple silicon
- Optional OpenAI-compatible local model endpoint and Azure workflow
- Streamlit interface for experimentation and manual result review

## Mac setup

Requires Python 3.10+. Apple Foundation Models additionally require Apple silicon, macOS 26+, Swift/Xcode Command Line Tools, and an available on-device model.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

For native Apple processing, choose the Apple Foundation Models option in the app. It requires no API URL. For a local OpenAI-compatible server such as Ollama, configure `.env` with a vision-capable model and the server's URL, for example:

```dotenv
LOCAL_OPENAI_BASE_URL=http://localhost:11434/v1
LOCAL_OPENAI_API_KEY=ollama
LOCAL_OPENAI_MODEL=<installed-vision-model>
```

The local API must support image input. Verify the selected model and the current provider integration before processing documents; a local-looking URL alone does not guarantee local-only processing.

## Azure OpenAI (optional)

Configure the Azure endpoint, API key, API version, and deployment in `.env` only if you intend to use Azure. In that mode, the document image is sent to the configured endpoint. Do not commit credentials.

## Privacy and responsible use

KTP data is sensitive personal information. Process only documents you are authorized to use. Prefer synthetic or redacted examples for development and demos. Review the selected provider's data handling and retention settings. This repository is a prototype and does not provide production authentication, compliance controls, or identity verification.

## Development checks

```bash
python -m unittest discover -s tests -v
```

If using an OpenAI-compatible local server, check its model listing with:

```bash
./scripts/check_local_model.sh
```

## Stack

Python · Streamlit · Pillow · pypdfium2 · Apple Vision/Foundation Models · OpenAI-compatible APIs · Azure OpenAI (optional)

## Repository structure

```text
app.py                         Streamlit interface
services/                      Document processing and model integration
helpers/                        Shared helper functions
scripts/                        Local setup and endpoint checks
tests/                          Automated tests
.env.example                    Safe configuration template
SECURITY.md                     Security and privacy guidance
```

## Roadmap ideas

- Add a sanitized sample screenshot and short demo recording
- Expand tests for image/PDF input and provider-specific responses
- Evaluate extraction quality with consented, redacted or synthetic samples
- Add explicit field-level confidence and human correction workflow
- Document supported local model servers and their image-input requirements

See [SECURITY.md](SECURITY.md) for security and privacy guidance.
