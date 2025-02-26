from PIL import Image
import streamlit as st
from helper.services import ktp_extraction

azure_openai_api_version = st.secrets["AZURE_OPENAI_API_VERSION"]
azure_openai_key = st.secrets["AZURE_OPENAI_KEY"]
endpoint_4o_mini = st.secrets["GPT4O_MINI_ENDPOINT"] 

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
        model = st.sidebar.selectbox('Select Model', ['gpt-4o-mini'], label_visibility='visible')
        if model == 'gpt-4o-mini':
            st.header("KTP Extraction")
            st.divider()
            ktp_extraction(model, azure_openai_key, endpoint_4o_mini)

if __name__ == "__main__":
    main()