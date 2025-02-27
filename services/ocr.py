import streamlit as st
import json
import base64
import re
import pandas as pd
from datetime import datetime
from PIL import Image
import pypdfium2 as pdfium
from io import BytesIO
from helpers.cost_calculations import calculate_aoai_cost
from helpers.model_inferences import aoai_llm_inference

prompt = """Extract information from the document and convert it into a JSON-formatted dictionary with the following keys: provinsi, kabupaten_kota, nik, nama, tempat_tgl_lahir, jenis_kelamin, gol_darah, alamat, rt_rw, kel_desa, kecamatan, agama, status_perkawinan, pekerjaan, kewarganegaraan, berlaku_hingga, tanggal_aktif. Include the city or regency name in the kabupaten_kota value, e.g., "Kota Lhokseumawe" or "Kabupaten Tuban." For gol_darah, use values A, B, AB, O, or None if the value is '-' or other. The tanggal_aktif is the date below the photo on the ID, while berlaku_hingga is the date on the bottom left of the photo. Return the result as a JSON dictionary."""

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
                    encode_data = base64.b64encode(buffered.getvalue()).decode('ascii')

            elif file_type == 'pdf':
                pdf = pdfium.PdfDocument(uploaded_file)
                image = pdf[0].render(scale=7).to_pil()
                with BytesIO() as buffered:
                    image.save(buffered, format="PNG")
                    encode_data = base64.b64encode(buffered.getvalue()).decode('ascii')
        else:
            st.warning("Please upload a document.")

    with col2:
        if uploaded_file is not None:
            caption_text = "Uploaded Image" if file_type != 'pdf' else "Uploaded PDF"
            st.image(image, caption=caption_text, use_container_width=True)

    extract_button = st.button("Extract KTP", icon="🔎")
    
    if extract_button: 
        start_time = datetime.now()
        with st.spinner("Extracting ..."):
            try:
                results = aoai_llm_inference(prompt, encode_data, azure_openai_key, azure_openai_chat_endpoint)
                total_time = round((datetime.now() - start_time).total_seconds(),2)
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
                token = results['usage']
                completion_tokens = token['completion_tokens']
                prompt_tokens = token['prompt_tokens']
                total_tokens = token['total_tokens']
                total_cost = calculate_aoai_cost(model, prompt_tokens, completion_tokens) 
                
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
                st.success(f"Extraction successful in {total_time} seconds.")
                st.json(results["choices"][0]["message"]["content"])
            except:
                st.write("Failed to make the request. Please try again")

        st.divider()
        
        a, b = st.columns(2)
        c, d = st.columns(2)
        a.metric(label="Total Tokens", value=total_tokens, border=True)
        b.metric(label="Input Tokens", value=prompt_tokens, border=True)
        c.metric(label="Cost ($)", value=str(total_cost), border=True)
        d.metric(label="Output Tokens", value=completion_tokens, border=True)

        try:
            filename = 'results/ktp.csv'
            df_existing = pd.read_csv(filename)
            df_new = pd.DataFrame([[uploaded_file.name,model_version, total_cost, total_time, prompt_tokens, completion_tokens, total_tokens]], columns=df_existing.columns)
            pd.concat([df_existing, df_new], ignore_index=True).to_csv(filename, index=False)
        except:
            pass
