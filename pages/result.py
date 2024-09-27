import streamlit as st
import pandas as pd


@st.dialog("Deseja retornar para a página principal?")
def voltar_para_pagina_principal():
    st.warning(
        "Se você voltar para a página principal, seu progresso e resultado será perdido."
    )
    if st.button("Confirmar"):
        st.switch_page("pages/home.py")


st.title("Resultado da Consulta")
df = st.session_state.dfFinal
st.write("Primeiras linhas do arquivo CSV:")
st.dataframe(df)

uploaded_file_Final = df.to_excel("Resultados.xlsx", index=False)

st.download_button(
    label="Baixar Arquivo",
    data=open("Resultados.xlsx", "rb"),
    file_name="Resultados.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

if "links_falhos" in st.session_state and st.session_state.links_falhos is not None:
    links_falhos = st.session_state.links_falhos
    st.write(links_falhos)

if st.button("Voltar para página principal"):
    voltar_para_pagina_principal()