import streamlit as st
import pandas as pd
from time import sleep
import pandas as pd
import backend.loading_utils as lu
import backend.gemini as ge

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title("We are processing the files, please wait")

if st.button("If something goes wrong and you want to return, click here"):
    # Volta pra pagina inicial
    st.switch_page("pages/home.py")

if (
    "df" in st.session_state
    and st.session_state.df is not None
    and "df_rfp" in st.session_state
    and st.session_state.df_rfp is not None
):
    # Exibe o arquivo carregado
    st.write("Loading...")
    erros = ""
    base = st.session_state.df
    rfp = st.session_state.df_rfp
    # Processe os dados aqui:

    # region Baixar Dados/base

    # Conjunto para armazenar links que falharam ao baixar
    

    # Verifica se as colunas necessárias existem
    if "Equipment" not in base.columns:
        if "Equipamento" in base.columns:
            base.rename(columns={"Equipamento": "Equipment"}, inplace=True)
            # st.write(
            #     "Assumindo erro humano e renomeando coluna 'Equipamento' para 'Equipment'"
            # )
        else:
            erros = erros + "Error: 'Equipment' Column not found on CSV file.\n"

    if "Link" not in base.columns:
        erros = erros + "Error: 'Link' Column not found on CSV file.\n"

    if erros:
        st.session_state.erros = erros
        st.switch_page("pages/error.py")

    # Remove linhas com valores nulos, não serão uteis ao programa
    base.dropna(subset=["Link"], inplace=True)
    base.dropna(subset=["Equipment"], inplace=True)

    base["Local"] = base["Link"].apply(lu.download_pdf)

    linkErrado = base[base["Local"].isnull()][["Equipment", "Link"]]

    base.dropna(subset=["Local"], inplace=True)

    links_falhos = None
    flag = True
    for i in linkErrado.values:
        if flag:
            flag = False
            links_falhos = "Equipment whose link does not work:\n\n"
        links_falhos = links_falhos + i[0] + " - " + i[1] + "\n\n"

    # Verifica se as colunas necessárias existem
    if "Requisito" not in rfp.columns:
        erros = erros + "Error: 'Requisito' Column not found on CSV file.\n"

    if "Comprovação" in rfp.columns:
        rfp = rfp.drop(columns=["Comprovação"])
    
    if "Arquivo" in rfp.columns:
        rfp = rfp.drop(columns=["Arquivo"])

    if erros:
        st.session_state.erros = erros
        st.session_state.links_falhos = links_falhos
        st.switch_page("pages/error.py")

    new_info, new_info_colour = ge.search_requirement(rfp, base)
    if new_info_colour != None:
        dfFinal = new_info_colour

        if links_falhos:
            st.session_state.links_falhos = links_falhos
        # So colcoar o dfFinal como o que foi adquirido
        st.session_state.dfFinal = dfFinal
        st.switch_page("pages/result.py")

#st.switch_page("pages/home.py")
