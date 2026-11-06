# Portfolio copy

Copy and adapt these descriptions for GitHub, LinkedIn, or a portfolio site. The wording intentionally presents OCR KTP as a prototype, not a production identity-verification service.

## GitHub repository description

Local-first Indonesian KTP OCR prototype exploring Apple on-device models, local vision APIs, and optional Azure OpenAI.

## Short tagline

Document AI for Indonesian KTPs, with a local-first Mac workflow.

## Portfolio summary

Built a Streamlit prototype that explores extracting visible fields from Indonesian identity cards into structured JSON. The project focuses on document preprocessing, multimodal model integration, and local-first experimentation on Apple silicon, with optional OpenAI-compatible local APIs and Azure OpenAI. Because identity-card data is sensitive and model output can be wrong, the project emphasizes privacy, manual review, and clear prototype limitations.

## LinkedIn post draft

I’ve been working on OCR KTP, a prototype for extracting visible fields from Indonesian identity cards into structured JSON.

The project explores document preprocessing and multimodal AI across on-device Apple Foundation Models, OpenAI-compatible local model APIs, and an optional Azure OpenAI workflow. A key design consideration is privacy: identity documents contain sensitive personal data, and model-generated fields must always be checked against the original.

This is an experimental portfolio project—not a production identity-verification system. I’m continuing to improve its test coverage, local setup, and extraction-quality evaluation.

## Portfolio website card

**OCR KTP — Local-first document AI prototype**  
A Streamlit application concept for extracting visible Indonesian KTP fields into structured JSON. Explores Apple on-device AI, local vision-model APIs, and optional Azure OpenAI. Built with Python; intended for experimentation and manual review.

## Technical interview talking points

- Why document extraction is more than OCR: field structure, ambiguity, and validation matter.
- Why offer local processing for sensitive identity documents, while being clear about endpoint trust and provider behavior.
- Why generated identity fields must remain unverified and require human review.
- Next engineering steps: provider integration tests, synthetic/redacted evaluation data, field-level confidence, and robust error handling.
