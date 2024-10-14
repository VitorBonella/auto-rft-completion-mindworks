import streamlit as st

st.title("Errors that occurred")

if ("erros" in st.session_state and st.session_state.erros is not None):
    erros = st.session_state.erros
    st.write(erros)

if ("links_falhos" in st.session_state and st.session_state.links_falhos is not None):
    links_falhos = st.session_state.links_falhos
    st.write(links_falhos)

if st.button('Return to main page'):
    #Volta pra pagina inicial
    st.switch_page("pages/home.py")