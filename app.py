import os
import platform

import streamlit as st
from dotenv import load_dotenv
from openai import AzureOpenAI

from services.ocr import (
    MAX_UPLOAD_BYTES,
    DocumentError,
    apple_foundation_model_inference,
    azure_openai_inference,
    prepare_document_image,
    validate_extraction,
)

load_dotenv()

st.set_page_config(page_title="OCR KTP", layout="centered")
st.title("KTP data extraction")
st.warning(
    "KTP contains sensitive personal information. Only process documents you are "
    "authorized to use. The local option keeps processing on this Mac; Azure "
    "OpenAI sends the image to the Azure endpoint configured by you."
)

LOCAL_MODEL = "Apple Foundation Models (on this Mac)"
AZURE_MODEL = "Azure OpenAI"
backend = st.radio("Processing option", [LOCAL_MODEL, AZURE_MODEL], horizontal=True)

if backend == LOCAL_MODEL:
    st.caption(
        "Local mode uses Apple's Vision framework for OCR and Foundation Models "
        "to structure the recognized text. It requires Apple silicon, macOS 26 or "
        "later, and an available on-device model. The model receives OCR text, "
        "not the original image."
    )
else:
    st.caption("Azure mode sends the uploaded document image to your configured Azure OpenAI deployment.")

uploaded_file = st.file_uploader(
    "Upload one KTP image or PDF (maximum 10 MB; PDF first page only)",
    type=["jpg", "jpeg", "png", "pdf"],
)
authorized = st.checkbox("I am authorized to process this document")

if uploaded_file is not None:
    try:
        if uploaded_file.size > MAX_UPLOAD_BYTES:
            raise DocumentError("File exceeds the 10 MB limit.")
        image_bytes, preview = prepare_document_image(uploaded_file.name, uploaded_file.getvalue())
        st.image(preview, caption="Document preview", use_container_width=True)
    except DocumentError as exc:
        image_bytes = None
        st.error(str(exc))
else:
    image_bytes = None

if st.button("Extract fields", type="primary", disabled=(image_bytes is None or not authorized)):
    try:
        with st.spinner("Processing document…"):
            if backend == LOCAL_MODEL:
                if platform.system() != "Darwin":
                    raise DocumentError("Apple Foundation Models are available only on macOS.")
                raw_result = apple_foundation_model_inference(image_bytes)
                usage = None
            else:
                endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "").strip()
                api_key = os.getenv("AZURE_OPENAI_API_KEY", "").strip()
                if not endpoint or not api_key:
                    raise DocumentError(
                        "Set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY in your .env file."
                    )
                client = AzureOpenAI(
                    azure_endpoint=endpoint,
                    api_key=api_key,
                    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview").strip(),
                    timeout=60.0,
                    max_retries=1,
                )
                deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4.1-mini").strip()
                response = azure_openai_inference(image_bytes, client, deployment)
                raw_result = response.choices[0].message.content or ""
                usage = response.usage

        result = validate_extraction(raw_result)
        st.success("Extraction complete. Check every field against the original document.")
        st.subheader("Extracted data")
        st.json(result)
        st.table([{"Field": key, "Value": value} for key, value in result.items()])
        if usage is not None:
            st.caption(
                f"Azure token usage: {usage.total_tokens} total "
                f"({usage.prompt_tokens} input, {usage.completion_tokens} output). "
                "This is not a cost estimate."
            )
    except DocumentError as exc:
        st.error(str(exc))
    except Exception:
        # Avoid displaying provider exception details that may contain request metadata.
        st.error("Processing failed. Check your configuration and service availability, then try again.")
