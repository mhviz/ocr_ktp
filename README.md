# OCR KTP

**A local-first document-AI app for extracting visible fields from Indonesian identity cards into structured JSON.** Choose Apple's on-device Foundation Model or an OpenAI-compatible API, review extracted fields, and see the total processing time.

> **Status: prototype.** Extraction is not guaranteed accurate, KTP authenticity is not checked, and this is not a production identity-verification system. Always verify results against the source document.

## Features

- Premium responsive web interface (FastAPI + HTML/CSS/JavaScript; no Streamlit)
- Apple Foundation Models or OpenAI-Compatible API, with model names loaded from `.env`
- Image/PDF upload, editable extracted fields, copy/download JSON, and elapsed-time display
- Input checks and local-first processing options

## Setup

Requires Python 3.10+. Apple processing additionally requires macOS and Swift/Xcode Command Line Tools. Native Apple Foundation Models require Apple silicon, macOS 26+, and an available on-device model.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

Configure the provider(s) you intend to use in `.env`:

```dotenv
LOCAL_MAC_URL=
LOCAL_MAC_API_KEY=
LOCAL_MAC_MODEL=

OPENAI_BASE_URL=
OPENAI_API_KEY=
OPENAI_MODEL=
```

For **Apple Foundation Models**, leave `LOCAL_MAC_URL` blank to use Apple's native on-device model. To use an Apple-compatible server instead, provide the `LOCAL_MAC_*` settings. In that mode, Vision OCR runs on the Mac and recognized text is sent to the configured endpoint.

For **OpenAI-Compatible API**, set `OPENAI_BASE_URL` and `OPENAI_MODEL`, and set `OPENAI_API_KEY` if required by the server. The uploaded document image is sent to this endpoint; verify its privacy and data handling before processing KTPs.

Start the app:

```bash
uvicorn app:app --reload
```

Then open <http://127.0.0.1:8000>. The provider cards show the model name loaded from `.env`. The result view displays total end-to-end time and server processing time, and lets you copy or download the edited JSON.

## Apple hardware acceleration

Vision OCR and Apple's Foundation Models use Apple's system frameworks, which choose and schedule available hardware acceleration automatically. This app does not force GPU-only execution: Apple does not expose a supported GPU-priority switch for these high-level Vision/Foundation Models APIs. On Apple silicon, the system may distribute work across the GPU, Neural Engine, and CPU depending on the operation, OS version, and runtime. If `LOCAL_MAC_URL` points to a separate OpenAI-compatible server, hardware selection for model inference is controlled by that server; this app only runs Vision OCR locally before sending recognized text to it.

## Privacy and responsible use

KTP data is sensitive personal information. Process only documents you are authorized to use. Prefer synthetic or redacted examples for development and demos. Review the selected provider's data handling and retention settings. Uploaded files are processed in memory and are not saved by this app. This repository is a prototype and does not provide production authentication, compliance controls, or identity verification. Do not expose it publicly without adding appropriate access controls.

## Development checks

```bash
python -m unittest discover -s tests -v
```

## Stack

Python · FastAPI · HTML/CSS/JavaScript · Pillow · pypdfium2 · Apple Vision/Foundation Models · OpenAI-compatible APIs

## Repository structure

```text
app.py                         FastAPI application and inference routes
services/                      Document processing and model integration
static/                         Premium browser UI
helpers/                        Shared helper functions
scripts/                        Local setup and endpoint checks
tests/                          Automated tests
.env.example                    Safe configuration template
SECURITY.md                     Security and privacy guidance
```

See [SECURITY.md](SECURITY.md) for security and privacy guidance.
