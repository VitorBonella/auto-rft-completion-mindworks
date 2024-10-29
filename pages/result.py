import streamlit as st
import pandas as pd


@st.dialog("Do you want to return to the main page?")
def voltar_para_pagina_principal():
    st.warning(
        "If you go back to the main page, your progress and results will be lost."
    )
    if st.button("Confirm"):
        st.switch_page("pages/home.py")


st.title("Query Result")
df = st.session_state.dfFinal
st.write("First lines of the resulting file:")
st.dataframe(df)

uploaded_file_Final = df.to_excel("Resultados.xlsx", index=False)

st.download_button(
    label="Download file",
    data=open("Resultados.xlsx", "rb"),
    file_name="Resultados.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

if "links_falhos" in st.session_state and st.session_state.links_falhos is not None:
    links_falhos = st.session_state.links_falhos
    st.write(links_falhos)

if len(st.session_state.arquivos_falhos) > 0:
    st.warning("Failed to process some files " + str(st.session_state.arquivos_falhos), icon="⚠️")

if st.button("Return to main page"):
    voltar_para_pagina_principal()