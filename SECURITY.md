# Security and privacy

## Sensitive identity data

This demo handles Indonesian identity-card data. Do not use real identity documents unless you are authorized and have assessed applicable privacy, legal, organizational, and provider requirements. Prefer synthetic or redacted test documents.

## Provider behavior

- **Apple Foundation Models, native mode:** Vision OCR and text structuring run on-device; the app does not send requests to a configurable API.
- **Apple Foundation Models, endpoint mode:** Vision OCR runs locally; recognized text is sent to `LOCAL_MAC_URL`. Verify the endpoint is local and trusted if you expect local-only processing.
- **OpenAI-Compatible API:** the uploaded document image is sent to `OPENAI_BASE_URL`. Verify the destination and its logging, retention, and privacy behavior before use.

The app has no authentication, authorization system beyond a user acknowledgement checkbox, production retention controls, or compliance certification. The checkbox is not access control. Do not expose this Streamlit demo publicly or treat it as a production identity-verification system.

## Secrets

Copy `.env.example` to `.env`; keep real API keys only in `.env` or a proper secret manager. `.env` is ignored by Git. Before pushing, check `git status` and ensure secrets, real KTP images, and extracted personal data are not included.

## Reporting a vulnerability

Please do not include API keys, KTP images, NIKs, or other personal data in a public issue. Report suspected security problems privately to the repository owner through GitHub's private vulnerability reporting feature.
