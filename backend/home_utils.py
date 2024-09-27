import streamlit as st
import os

def save_api_key_to_env(api_key):
    with open(".env", "w") as f:
        f.write(f"API_KEY={api_key}\n")
        f.flush()
        f.close()
    # load_dotenv()
    os.environ["API_KEY"] = api_key

# Função para recuperar a API Key da variável de ambiente
def get_api_key():
    return os.getenv("API_KEY")

def alternateAPIToast():
    if st.session_state.apiToast:
        st.session_state.apiToast = False
    else:
        st.session_state.apiToast = True

def alternateVisible():
    if st.session_state.visible:
        st.session_state.visible = False
    else:
        st.session_state.visible = True