# OCR KTP

**A local-first document-AI prototype for extracting visible fields from Indonesian identity cards into structured JSON.** The project supports Apple's native on-device Foundation Model, a configurable Apple-compatible endpoint, and a general OpenAI-compatible API.

> **Status: prototype.** Extraction is not guaranteed accurate, KTP authenticity is not checked, and this is not a production identity-verification system. Always verify results against the source document.

## Demo

<!-- Add a screenshot only after capturing it with synthetic or fully redacted sample data. -->

_Add a sanitized screenshot here, for example `docs/images/app-demo.png`._

The app flow lets you choose Apple Foundation Models or OpenAI-Compatible API; the configured model name from `.env` is shown in the provider choices. Do not publish screenshots containing real names, NIKs, addresses, or other personal information.

## Project highlights

- Indonesian KTP field extraction into a structured format
- Apple Vision OCR and on-device Apple Foundation Models
- Configurable OpenAI-compatible chat-completions endpoint
- Streamlit interface for experimentation and manual result review

## Setup

Requires Python 3.10+. Apple processing additionally requires macOS and Swift/Xcode Command Line Tools. Native Apple Foundation Models require Apple silicon, macOS 26+, and an available on-device model.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

Configure only the provider you plan to use in `.env`:

```dotenv
LOCAL_MAC_URL=
LOCAL_MAC_API_KEY=
LOCAL_MAC_MODEL=

OPENAI_BASE_URL=
OPENAI_API_KEY=
OPENAI_MODEL=
```

For **Apple Foundation Models**, leave `LOCAL_MAC_URL` blank to run the native on-device Foundation Model. To use an Apple-compatible server instead, set all `LOCAL_MAC_*` values. In that endpoint mode, Vision OCR runs locally and only recognized text is sent to the configured endpoint. The app displays `LOCAL_MAC_MODEL` in the Apple provider choice.

For **OpenAI-Compatible API**, set `OPENAI_BASE_URL` and `OPENAI_MODEL`; set `OPENAI_API_KEY` if the server requires authentication. The app displays `OPENAI_MODEL` in the provider choice. This endpoint receives the uploaded document image, so verify its privacy and data handling before processing KTPs.

## Privacy and responsible use

KTP data is sensitive personal information. Process only documents you are authorized to use. Prefer synthetic or redacted examples for development and demos. Review the selected provider's data handling and retention settings. This repository is a prototype and does not provide production authentication, compliance controls, or identity verification.

## Development checks

```bash
python -m unittest discover -s tests -v
```

## Stack

Python · Streamlit · Pillow · pypdfium2 · Apple Vision/Foundation Models · OpenAI-compatible APIs

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

See [SECURITY.md](SECURITY.md) for security and privacy guidance.
