import os
import re
import requests
import streamlit as st
from time import sleep
import random

import urllib.parse

from backend import gpt
import pandas as pd

def download_pdf(url, download_folder="downloads"):
    failed_links = set()
    # Cria a pasta de downloads se ela não existir
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Nome do arquivo baseado no link mas com formatação adequada...
    temp = urllib.parse.unquote(url)
    #temp = url
    file_name = os.path.join(download_folder, temp.split("/")[-1])
    match = re.search(r"\.pdf", file_name)
    if match:
        # Corta a string até a posição logo após o .pdf se achar
        file_name = file_name[:match.end()]
    

    # Verifica se o arquivo já foi baixado ou se já falhou anteriormente
    if os.path.isfile(file_name):
        # print(f"{file_name} já foi baixado.")
        return file_name
    if url in failed_links:
        # print(f"{url} já falhou anteriormente. Pulando...")
        return None

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": url,
    }

    try:
        # Utiliza uma sessão para gerenciar cookies e cabeçalhos
        with requests.Session() as session:
            session.headers.update(headers)
            response = session.get(url, timeout=5)
            response.raise_for_status()  # Levanta exceção para status HTTP 4xx/5xx
            with open(file_name, "wb") as file:
                file.write(response.content)
        # print(f"{file_name} baixado com sucesso.")
        return file_name
    except requests.RequestException as e:
        # print(f"Falha ao baixar {url}. Erro: {e}")
        failed_links.add(url)  # Adiciona o link ao conjunto de falhas
        return None

def ajustar_cores(df):
    for col in df.columns:
        if col.startswith("Resposta_"):
            cor_col = col.replace("Resposta_", "Cor_")
            # Verifica se a coluna de cor correspondente existe
            if cor_col in df.columns:

                def ajustar_cor(row):
                    resposta = row[col]
                    cor_atual = row[cor_col]

                    # Condições para RED
                    if (
                        pd.isna(resposta)
                        or resposta == ""
                        or resposta == "Não encontrado"
                        or resposta == "N/A"
                        or resposta == "Não mencionado"
                        or resposta == "Not enough information"
                        or resposta == "Not applicable"
                        or resposta == "Not mentioned"
                        or resposta == "Not found"
                        or resposta == "Not met"
                        or resposta == "Not stated"
                        or resposta == "None"
                        or resposta == "No"
                        or resposta == "Não"
                    ):
                        return "yellow"

                    # Ajusta para YELLOW se for uma string válida e a cor atual for red
                    if (
                        cor_atual == "yellow"
                        and isinstance(resposta, str)
                        and resposta not in ["Não encontrado", "", "N/A", "Não mencionado", "Not enough information", "Not applicable", "Not mentioned", "Not found", "Not met", "Not stated", "None", "No", "Não"]
                    ):
                        return "red"

                    return cor_atual

                # Aplicar ajuste de cor
                df[cor_col] = df.apply(ajustar_cor, axis=1)
    return df


def aplicar_cor(df):
    for col in df.columns:
        if col.startswith("Resposta_"):
            df[col] = df[df.columns[df.columns.get_loc(col) + 1]]
            df[col] = df[col].apply(
                lambda x: (
                    "background-color: green"
                    if x == "green"
                    else (
                        "background-color: yellow"
                        if x == "yellow"
                        else "background-color: red"
                    )
                )
            )
        else:
            df[col] = ""

    return df

def search_requirement(rfp, base):
    # Aqui entrará a integracao com o modelo de ML (ChatGPT)
    progress_bar = st.progress(0)
    questoes = ""

    for questao in rfp["Requisito"]:
        questoes += "$$$ " + questao + "\n"

    assitant = gpt.get_assistant()

    arquivos = base["Local"].unique()

    saidas = []
    total_arquivos = len(arquivos)
    qtd = 1 / arquivos.size

    for idx, arq in enumerate(arquivos):
        vector_store = gpt.create_vector_store_single(arq)
        assitant, thread = gpt.create_thread(assitant, vector_store, questoes)
        sleep(0.05)
        output, cit, messages = gpt.create_run(assitant, thread)
        saidas.append(output)
        # print(output)
        output = gpt.format_output(output)
        # print(output)
        id1 = "_" + str(random.randint(0, 100000000))
        id2 = "_" + str(random.randint(0, 100000000))
        rfp = rfp.merge(output, on="Requisito", how="left", suffixes=(id1, id2))
        progress_bar.progress((idx + 1) * qtd)
        sleep(5)
        
    rfp = ajustar_cores(rfp)
    escondidos = []
    for col in rfp.columns:
        if col.startswith('Cor_'):
            escondidos.append(col)
    
    style = rfp.style.apply(aplicar_cor, axis=None)
    style = style.hide(subset=escondidos, axis=1)

    return rfp, style