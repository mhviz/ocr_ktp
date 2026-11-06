# OCR KTP

A small Streamlit demo for extracting visible fields from an Indonesian KTP into JSON. It supports Apple's native on-device Foundation Models, an OpenAI-compatible local vision-model API (for example, Ollama on a Mac), and Azure OpenAI. Model output is unverified; always compare it with the original document.

## Overview

This project extracts text from a KTP image or PDF and converts it into structured JSON fields such as NIK, name, address, date of birth, and other visible identity properties.

It is designed as a proof-of-concept and local demo rather than a production-grade identity-verification system.

## Why this project is useful

- Quick local prototype for OCR on KTP documents
- Works with local Mac hardware and local model servers
- Good for demos, experiments, and portfolio work
- Easy to extend with another document type or stricter validation layer

## Local setup on Mac

### 1) Install Python and create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2) Copy environment template

```bash
cp .env.final.example .env
```

### 3) Use the local Ollama model route

Edit `.env` to set:

```env
LOCAL_OPENAI_BASE_URL=http://localhost:11434/v1
LOCAL_OPENAI_API_KEY=ollama
LOCAL_OPENAI_MODEL=qwen2.5vl:3b
```

### 4) Pull a vision-capable model

```bash
brew install ollama
ollama pull qwen2.5vl:3b
ollama list
```

### 5) Run the app

```bash
streamlit run app.py
```

Select the local OpenAI-compatible option in the UI.

## Native Apple option

If you are on macOS 26+ with Apple silicon, use the native Apple mode and choose:

- Apple Foundation Models (on this Mac)

This mode keeps OCR and model inference on-device and does not require a URL or API key.

## Azure option

The Azure path is optional and only for users who already have a valid Azure OpenAI deployment.

```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_API_VERSION=2025-01-01-preview
AZURE_OPENAI_DEPLOYMENT=gpt-4.1-mini
```

## Privacy note

KTP data is sensitive personal data. Use this project only for documents you are authorized to process. Always review the extracted results manually before using them for any decision-making.

## Validation

```bash
python -m unittest discover -s tests -v
./scripts/validate_local_ocr.sh
```

## Stack

- Python
- Streamlit
- Pillow
- pypdfium2
- OpenAI-compatible local API / Ollama
- Azure OpenAI (optional)

## Typical use cases

- KTP OCR prototype
- Structured field extraction demo
- Local AI experimentation on Mac
- Portfolio project for AI + document processing

## Notes

This is a prototype and should not be treated as a production identity verification or compliance system.
