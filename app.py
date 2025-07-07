import os
from PIL import Image
import streamlit as st
from services.ocr import ktp_extraction
from dotenv import load_dotenv
load_dotenv()

azure_openai_api_version = os.getenv("MODEL_gpt_41_mini_APIVERSION")
azure_openai_key = os.getenv("MODEL_gpt_41_mini_KEY")
endpoint = os.getenv("MODEL_gpt_41_mini_APIVERSION")

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
            ktp_extraction(model, azure_openai_key, endpoint)

if __name__ == "__main__":
    main()