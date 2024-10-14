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
st.title("API Key Configuration")
styles = {
    "material-icons": {"color": "red"},
    "text-icon-link-close-container": {"box-shadow": "#3896de 0px 4px"},
    "notification-text": {"": ""},
    "close-button": {"": ""},
    "link": {"": ""},
}

if hu.get_api_key():
    st.write("There is already an API Key configured.")
    st.write(
        "If you do not wish to change your API Key, click the button below to return to the main page."
    )
    st.write(
        "If you wish to change your API Key, enter the new API Key below and click the 'Save' button"
    )
else:
    st.write("Hello! It looks like you haven't configured your API Key yet.")
    st.write("Please enter your API Key below to use the tool!")

# Formulário para setar a API Key
api_key_input = st.text_input("API Key", type="password")

# if st.button("Configurar API Key"):
#     set_api_key(api_key_input)

if st.button("Save"):
    hu.save_api_key_to_env(api_key_input)
    #st.success("API Key configurada! Você será redirecionado para a página principal.")
    hu.alternateAPIToast()
    st.switch_page("pages/home.py")
    
if st.button("Return to main page"):
    # Volta pra pagina inicial
    st.switch_page("pages/home.py")
