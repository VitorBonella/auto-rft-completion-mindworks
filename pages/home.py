import os
import dotenv
import streamlit as st
import pandas as pd
import backend.home_utils as hu

if "visible" not in st.session_state:
    st.session_state["visible"] = False
    
if "apiToast" not in st.session_state:
    st.session_state["apiToast"] = False

# Interface no Streamlit
st.title("Home Page")
    
if st.session_state.apiToast:
    st.toast("API Key configured successfully!", icon='🎉')
    st.session_state.apiToast = False

if hu.get_api_key():

    with st.popover("Click here to configure your API Key"):
            st.write(f"Your current API Key is: {os.getenv("API_KEY")}")

            api_key_input = st.text_input("Insert your new API Key", type="password")
            if st.button("Save changes"):
                hu.save_api_key_to_env(api_key_input)
                hu.alternateAPIToast()
                hu.alternateVisible()
                st.rerun()

    st.subheader("Select files for analysis!")


    ## CSS para o file uploader, isso provavelmente irá quebrar ao longo do tempo, mas ainda não há solução melhor e/ou oficial para o problema das linguagens
    # css='''
    # <style>
    # [data-testid="stFileUploaderDropzone"] div div::before {color:white; content:"Arraste o arquivo aqui ou clique para selecionar";}
    # [data-testid="stFileUploaderDropzone"] div div span{display:none;}
    # [data-testid="stFileUploaderDropzone"] div div::after {color:white; font-size: .8em; content:"O limite de tamanho para o arquivo é de 200MB"}
    # [data-testid="stFileUploaderDropzone"] div div small{display:none;}
    # </style>
    # '''

    # st.markdown(css, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Choose a file with the equipment to be analyzed", type="csv"
    )
    
    if uploaded_file is not None:
        # Ler o arquivo CSV usando pandas
        df = pd.read_csv(uploaded_file)
        # Mostrar uma prévia do arquivo CSV
        st.write("Please check the file content:")
        st.dataframe(df)
    
    rfp_file = st.file_uploader("Escolha a RFP", type="csv")

    if uploaded_file is not None and rfp_file is not None:
        
        df_rfp = pd.read_csv(rfp_file)
        st.write("Please check the file content:")
        st.dataframe(df_rfp)

        # Botão de confirmação
        if st.button("Confirm files"):
            # Se o botão for clicado, processar o DataFrame
            st.write("CSV files confirmed. Processing...")
            st.session_state.df = df
            st.session_state.df_rfp = df_rfp
            st.switch_page("pages/loading.py")

else:
    st.write("Hello! It looks like you haven't configured your API Key yet.")
    st.write("Please enter your API Key below to use the tool!")
    # Formulário para setar a API Key
    api_key_input = st.text_input("API Key", type="password")
    if st.button("Save"):
        hu.save_api_key_to_env(api_key_input)
        st.toast("API Key configured successfully!", icon='🎉')
