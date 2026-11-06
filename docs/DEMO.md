# Demo and screenshot guide

Use this checklist before adding a visual demo to README or a portfolio page.

## Capture a safe screenshot

1. Run the application locally with synthetic or fully redacted sample data.
2. Do not use a real KTP, NIK, name, address, birth date, face, or other personal data—even in a public portfolio screenshot.
3. Remove terminal output, environment variables, API keys, local file paths, and unrelated desktop notifications from the capture.
4. Capture the UI and example output only after confirming every displayed value is synthetic.
5. Save the image as `docs/images/app-demo.png` and review it at full size before committing.
6. Add it to `README.md` using:

   ```markdown
   ![OCR KTP demo using synthetic data](docs/images/app-demo.png)
   ```

## Short demo recording outline

- Introduce the app as a prototype for document-AI experimentation.
- Select a processing mode and state clearly where the data is processed.
- Use only a synthetic/redacted sample document.
- Show the extracted JSON and manually compare it with the synthetic source.
- End with the limitations: extraction may be wrong; this does not verify identity or authenticate KTPs.

Do not claim accuracy or privacy properties that have not been tested for the exact model, endpoint, and deployment configuration shown.
