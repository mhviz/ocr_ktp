import os
from PIL import Image
import base64
import pypdfium2 as pdfium
from io import BytesIO
import streamlit as st
import requests
import json
import pandas as pd
import re
from datetime import datetime
import pandas as pd

prompt = """Extract information from the document and convert it into a JSON-formatted dictionary with the following keys: provinsi, kabupaten_kota, nik, nama, tempat_tgl_lahir, jenis_kelamin, gol_darah, alamat, rt_rw, kel_desa, kecamatan, agama, status_perkawinan, pekerjaan, kewarganegaraan, berlaku_hingga, tanggal_aktif. Include the city or regency name in the kabupaten_kota value, e.g., "Kota Lhokseumawe" or "Kabupaten Tuban." For gol_darah, use values A, B, AB, O, or None if the value is '-' or other. The tanggal_aktif is the date below the photo on the ID, while berlaku_hingga is the date on the bottom left of the photo. Return the result as a JSON dictionary."""

def calculate_cost(model, prompt_tokens, completion_tokens):
    # Pricing per 1,000,000 tokens
    if model == 'gpt-4o':
        input_price_per_million = 2.5
        output_price_per_million = 10 
    elif model == 'gpt-4o-mini':
        input_price_per_million = 0.15
        output_price_per_million = 0.60

    # Convert pricing to per token
    input_price_per_token = input_price_per_million / 1_000_000
    output_price_per_token = output_price_per_million / 1_000_000

    # Calculate cost for each type of token
    prompt_cost = prompt_tokens * input_price_per_token
    completion_cost = completion_tokens * output_price_per_token

    # Total cost
    total_cost = prompt_cost + completion_cost

    return total_cost


def extract_data(prompt, encoded_data, azure_openai_key, azure_openai_chat_endpoint):
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

def ktp_extraction(model, azure_openai_key, azure_openai_chat_endpoint):
    
    col1, col2 = st.columns(2)
    with col1:
        uploaded_file = st.file_uploader("Choose a File", type=["jpg", "jpeg", "png", "pdf"])
        if uploaded_file is not None:
            file_type = uploaded_file.type.lower().split('/')[1]

            if file_type != 'pdf':
                image = Image.open(uploaded_file)
                with BytesIO() as buffered:
                    image.save(buffered, format="PNG")
                    # st.image(image, caption="Uploaded Image", use_column_width=True)
                    encode_data = base64.b64encode(buffered.getvalue()).decode('ascii')

            elif file_type == 'pdf':
                pdf = pdfium.PdfDocument(uploaded_file)
                image = pdf[0].render(scale=7).to_pil()
                with BytesIO() as buffered:
                    image.save(buffered, format="PNG")
                    # st.image(image, caption="Uploaded PDF", use_column_width=True)
                    encode_data = base64.b64encode(buffered.getvalue()).decode('ascii')
        else:
            st.warning("Please upload a document before clicking the button.")

    
    with col2:
        if uploaded_file is not None:
            caption_text = "Uploaded Image" if file_type != 'pdf' else "Uploaded PDF"
            st.image(image, caption=caption_text, use_column_width=True)
    extract_button = st.button("Recaption")
    
    if extract_button: 
    # if uploaded_file is not None: 
        start_time = datetime.now()
        with st.spinner("Proccessing Document..."):
            try:
                results = extract_data(prompt, encode_data, azure_openai_key, azure_openai_chat_endpoint)
                
            except:
                st.write("Failed to make the request. Please try again. Don't forget to upload a document")
                raise SystemExit(f"Failed to make the request.")

        st.subheader('Result')
        tab_json, tab_table = st.tabs(["JSON", "TABLE"])
        with tab_table:
            result_tab1 = results["choices"][0]["message"]["content"]
            print(result_tab1)           
            try:
                data_result = json.loads(result_tab1)
            except:
                try:
                    result_tab1 = re.search(r'{.*?}', result_tab1, re.DOTALL).group(0)
                    data_result = json.loads(result_tab1)
                except:
                    raise SystemExit(f"Failed to make the request.")
            
            try:
                df_result = pd.json_normalize(data_result).T.reset_index()
                df_result.columns = ["key","value"]
                st.table(df_result)
            except:
                st.write("Failed to make the request. Please try again")
        with tab_json:
            try:
                st.success("Extraction Success")
                st.json(results["choices"][0]["message"]["content"])
            except:
                st.write("Failed to make the request. Please try again")
        
        token = results['usage']
        model_version = results['model']
        completion_tokens = token['completion_tokens']
        prompt_tokens = token['prompt_tokens']
        total_tokens = token['total_tokens']
        total_cost = calculate_cost(model, prompt_tokens, completion_tokens) 
        total_time = datetime.now() - start_time

        st.divider()

        viz1, viz2 = st.columns(2)
        with viz1:
            st.metric(label=model_version, value="Model Version")
            st.metric(label='$'+str(total_cost), value="Estimated Cost")
            st.metric(label=str(total_time), value="Processing Time")
        
        with viz2:
            st.metric(label="Input Tokens", value=prompt_tokens)
            st.metric(label="Output Tokens", value=completion_tokens)
            st.metric(label="Total Tokens", value=total_tokens)

        # try:
        #     filename = 'result/ktp.csv'
        #     df_existing = pd.read_csv(filename)
        #     df_new = pd.DataFrame([[uploaded_file.name,model_version, total_cost, total_time, prompt_tokens, completion_tokens, total_tokens]], columns=df_existing.columns)
        #     pd.concat([df_existing, df_new], ignore_index=True).to_csv(filename, index=False)
        # except:
        #     pass

