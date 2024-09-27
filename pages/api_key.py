from asyncio import wait
import os
import streamlit as st
from dotenv import load_dotenv
import dotenv
from streamlit_custom_notification_box import custom_notification_box
import backend.home_utils as hu

if "visible" not in st.session_state:
    st.session_state["visible"] = False
    
if "apiToast" not in st.session_state:
    st.session_state["apiToast"] = False
    
# Interface no Streamlit
st.title("Configuração de API Key")
styles = {
    "material-icons": {"color": "red"},
    "text-icon-link-close-container": {"box-shadow": "#3896de 0px 4px"},
    "notification-text": {"": ""},
    "close-button": {"": ""},
    "link": {"": ""},
}

if hu.get_api_key():
    st.write("Já existe uma API Key configurada.")
    st.write(
        "Caso não deseje mudar a sua API Key, clique no botão abaixo para voltar para a página principal."
    )
    st.write(
        "Caso deseje mudar a sua API Key, insira a nova API Key abaixo e clique no botão 'Salvar'"
    )
else:
    st.write("Olá! Parece que você ainda não configurou sua API Key.")
    st.write("Por favor, insira sua API Key abaixo para utilizar a ferramenta!")

# Formulário para setar a API Key
api_key_input = st.text_input("Insira abaixo sua API Key", type="password")

# if st.button("Configurar API Key"):
#     set_api_key(api_key_input)

if st.button("Salvar a API Key"):
    hu.save_api_key_to_env(api_key_input)
    #st.success("API Key configurada! Você será redirecionado para a página principal.")
    hu.alternateAPIToast()
    st.switch_page("pages/home.py")
    
if st.button("Voltar para página principal"):
    # Volta pra pagina inicial
    st.switch_page("pages/home.py")
