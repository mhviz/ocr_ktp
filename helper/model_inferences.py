import streamlit as st
import requests

def aoai_llm_inference(prompt, encoded_data, azure_openai_key, azure_openai_chat_endpoint):
    payload = {
        "temperature": 0,
        "messages": [
        {
        "role": "system",
        "content": [
            {
            "type": "text",
            "text": "You are an AI assistant that extracts data from documents and returns them as structured JSON objects. Do not return as a code block."
            }]},
        {
        "role": "user",
        "content": [
        {"type": "text","text": prompt},
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_data}"}}
        ]}]
    }

    try:
        response = requests.post(azure_openai_chat_endpoint,
                                headers={"Content-Type": "application/json",
                                        "api-key": azure_openai_key,},
                                json=payload)
        #response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        return response.json()
    except:
        st.write("Failed to make the request. Please try again")
        raise SystemExit(f"Failed to make the request.")