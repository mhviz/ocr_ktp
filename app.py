import os
from PIL import Image
from openai import AzureOpenAI
import streamlit as st
from services.ocr import ktp_extraction
from dotenv import load_dotenv
load_dotenv()

deployment = "gpt-4.1-mini"
if deployment == "gpt-4.1-mini":
    secrets_helpers = "gpt_41_mini"

api_version = os.getenv(f"MODEL_{secrets_helpers}_APIVERSION", "2025-01-01-preview")
subscription_key = os.getenv(f"MODEL_{secrets_helpers}_KEY")
endpoint = os.getenv(f"MODEL_{secrets_helpers}_ENDPOINT")

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key)

# Set page configuration
st.set_page_config(
    page_title="OCR KTP",
    # page_icon=icon,
    layout="centered",
    initial_sidebar_state="auto"
)

# Hide Streamlit menu
hide_menu = """ 
<style> 
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;};
</style> 
""" 
st.markdown(hide_menu, unsafe_allow_html=True)

def main():

    menu = st.sidebar.radio('MENU', ['KTP Extraction'], label_visibility='hidden')
    
    if menu == 'KTP Extraction':
        model = st.sidebar.selectbox('Select Model', ['gpt-4.1-mini'], label_visibility='visible')
        if model == 'gpt-4.1-mini':
            st.header("KTP Extraction")
            st.divider()
            ktp_extraction(model, client)

if __name__ == "__main__":
    main()