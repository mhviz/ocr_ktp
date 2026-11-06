# OCR KTP

A small Streamlit demo that extracts visible fields from an Indonesian KTP into JSON. It supports a local Apple Silicon option and an optional Azure OpenAI option. Treat all extracted values as unverified and check them against the document.

## Processing options

### Apple Foundation Models (local)

On an Apple Silicon Mac with **macOS 26 or later**, select **Apple Foundation Models (on this Mac)**. The app uses Apple's Vision framework to OCR the document locally, then passes the recognized text to the on-device Foundation Model to structure it. The Foundation Model receives text, not the image. No Azure credentials or hosted-model request are used in this mode. The local model must be available on the Mac; availability is controlled by macOS and device settings.

Install Xcode Command Line Tools so the `swift` command is available:

```bash
xcode-select --install
```

### Azure OpenAI (optional)

Selecting **Azure OpenAI** sends the processed document image to the Azure endpoint you configure. Review your organization's privacy, retention, region, and access requirements before using real identity documents. Never commit API keys.

Copy `envExample.txt` to `.env` and set your Azure resource values. Azure is optional; the local mode does not need these variables.

## Setup

Requires Python 3.10 or later.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp envExample.txt .env   # optional; configure only for Azure mode
streamlit run app.py
```

## Input and privacy notes

- Accepts JPEG, PNG, and PDF uploads up to 10 MB. PDFs are limited to 20 pages and only the first page is processed.
- Images are resized before inference; no uploaded document or extraction result is intentionally written to the repository or application logs. Temporary files used by the local Swift process are removed when processing ends. Hosting infrastructure and the selected provider may have their own logs and retention behavior.
- Local mode uses on-device Vision OCR and Apple's Foundation Models. It requires compatible macOS and model availability; no cloud fallback is performed.
- Azure mode sends the image to the Azure endpoint configured by the operator. Azure usage and data handling are governed by that Azure resource's configuration and policies.
- The model can misread or invent values. This demo does not validate KTP authenticity, verify NIKs, or replace human review. Do not use it to make eligibility or identity decisions.
- Do not upload documents unless you are authorized to process them. Use synthetic or redacted examples for development and demos.

## Development notes

The Azure deployment name, endpoint, API key, and API version are configured through environment variables. Dependency ranges are in `requirements.txt`; run the app in a virtual environment and review dependency advisories before deployment. This repository does not include a production authentication, retention, or compliance layer.
