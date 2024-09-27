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
st.title("Página inicial")
    
if st.session_state.apiToast:
    st.toast("API Key configurada com sucesso!", icon='🎉')
    st.session_state.apiToast = False

if hu.get_api_key():

    with st.popover("Deseja alterar a API Key?"):
            st.write(f"Sua API Key Atual é: {os.getenv("API_KEY")}")

            api_key_input = st.text_input("Insira abaixo sua API Key", type="password")
            if st.button("Salvar a API Key"):
                hu.save_api_key_to_env(api_key_input)
                hu.alternateAPIToast()
                hu.alternateVisible()
                st.rerun()

    st.subheader("Selecione os arquivos para análise!")

    uploaded_file = st.file_uploader(
        "Escolha um arquivo com os equipamentos para analisar", type="csv"
    )
    
    if uploaded_file is not None:
        # Ler o arquivo CSV usando pandas
        df = pd.read_csv(uploaded_file)
        # Mostrar uma prévia do arquivo CSV
        st.write("Por favor verifique o conteúdo do arquivo:")
        st.dataframe(df)
    
    rfp_file = st.file_uploader("Escolha a RFP", type="csv")

    if uploaded_file is not None and rfp_file is not None:
        
        df_rfp = pd.read_csv(rfp_file)
        st.write("Por favor verifique o conteúdo do arquivo:")
        st.dataframe(df_rfp)

        # Botão de confirmação
        if st.button("Confirmar CSVs"):
            # Se o botão for clicado, processar o DataFrame
            st.write("Arquivos CSVs confirmados. Processando...")
            st.session_state.df = df
            st.session_state.df_rfp = df_rfp
            st.switch_page("pages/loading.py")

else:
    st.write("Olá! Parece que você ainda não configurou sua API Key.")
    st.write("Por favor, insira sua API Key abaixo para utilizar a ferramenta!")
    # Formulário para setar a API Key
    api_key_input = st.text_input("API Key", type="password")
    if st.button("Salvar a API Key"):
        hu.save_api_key_to_env(api_key_input)
        st.toast("API Key configurada com sucesso!", icon='🎉')
