# Security and privacy

## Sensitive identity data

This demo handles Indonesian identity-card data. Do not use real identity documents unless you are authorized and have assessed applicable privacy, legal, organizational, and provider requirements. Prefer synthetic or redacted test documents.

## Provider behavior

- **Apple Foundation Models:** the app uses local Vision OCR and on-device text structuring; it does not send requests to Azure or the configurable local API in this mode.
- **Local OpenAI-compatible API:** the image is sent to `LOCAL_OPENAI_BASE_URL`. Verify the server is actually local/trusted and does not proxy or log sensitive content.
- **Azure OpenAI:** the image is sent to the configured Azure endpoint. Review resource region, access, retention, and organizational settings.

The app has no authentication, authorization system beyond a user acknowledgement checkbox, production retention controls, or compliance certification. The checkbox is not access control. Do not expose this Streamlit demo publicly or treat it as a production identity-verification system.

## Secrets

Copy `.env.example` to `.env`; keep real API keys only in `.env` or a proper secret manager. `.env` is ignored by Git. Before pushing, check `git status` and ensure secrets, real KTP images, and extraction results are not staged. If a key was ever committed, revoke/rotate it; deleting it from the latest commit is not sufficient.

## Reporting a vulnerability

Please do not include API keys, KTP images, NIKs, or other personal data in a public issue. Report suspected security problems privately to the repository owner through GitHub's private vulnerability reporting feature if available, or contact the maintainer directly.
