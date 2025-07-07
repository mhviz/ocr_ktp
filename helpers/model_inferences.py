import streamlit as st

def aoai_llm_inference(prompt, encoded_data, client, deployment):

    messages = [
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
    
    try:
        response = client.chat.completions.create(
            messages=messages,
            temperature=0,
            model=deployment)
        return response

    except:
        st.write("Failed to make the request. Please try again")
        raise SystemExit(f"Failed to make the request.")