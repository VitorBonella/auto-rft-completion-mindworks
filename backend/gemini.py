"""
Install the Google AI Python SDK

$ pip install google-generativeai
"""

import json
import os
import random
import time
import google.generativeai as genai
import pandas as pd
import streamlit as st
import backend.gemini_prompt


def upload_to_gemini(path, mime_type=None):
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

def wait_for_files_active(files):
  print("Waiting for file processing...")
  for name in (file.name for file in files):
    file = genai.get_file(name)
    while file.state.name == "PROCESSING":
      print(".", end="", flush=True)
      time.sleep(10)
      file = genai.get_file(name)
    if file.state.name != "ACTIVE":
      raise Exception(f"File {file.name} failed to process")
  print("...all files ready")
  print()


def create_model():
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro-latest",
        generation_config=generation_config,
        system_instruction=backend.gemini_prompt.GEMINIPROMPT,
    )
    
    return model


def search_requirement(rfp, base):
    genai.configure(api_key=os.getenv('API_KEY'))

    questoes = ""

    for questao in rfp["Requisito"]:
        questoes += "$$$ " + questao + "\n"


    arquivos = base["Local"].unique()

    saidas = []
    total_arquivos = len(arquivos)
    qtd = 1 / arquivos.size

    progress_bar = st.progress(0, "0" + "/" + str(total_arquivos))

    for idx, arq in enumerate(arquivos):
        file = upload_to_gemini(arq, mime_type="application/pdf")
        wait_for_files_active([file])
        model = create_model()
        chat_session = model.start_chat()
        try:
            output = chat_session.send_message([file, questoes])
        except Exception as e:
            st.write("ERROR")
            st.write("Try to change your API KEY, or call the developers")
            st.exception(e)
            return None,None
        output = output.text
        saidas.append(output)
        output = format_output(output)
        id1 = "_" + str(random.randint(0, 100000000))
        id2 = "_" + str(random.randint(0, 100000000))
        rfp = rfp.merge(output, on="Item", how="left", suffixes=(id1, id2))
        
        progress_bar.progress((idx + 1) * qtd, str(idx+1) + "/" + str(total_arquivos))
        st.write(arq + "      ", "Completed")

        time.sleep(31)

    rfp = ajustar_cores(rfp)
    escondidos = []
    for col in rfp.columns:
        if col.startswith('Cor_'):
            escondidos.append(col)
    
    style = rfp.style.apply(aplicar_cor, axis=None)
    style = style.hide(subset=escondidos, axis=1)

    return rfp, style

def format_output(content):

    res_txt = content
    if res_txt.startswith("```json"):
        res_txt = res_txt[6:]
    if res_txt.endswith("```"):
        res_txt = res_txt[:-3]
    res_txt = res_txt[: res_txt.rfind("}") + 1]
    res_txt = res_txt[res_txt.find("{") :]
    res_txt.strip()

    # pattern = r"```[a-zA-Z]*\n|'''[a-zA-Z]*\n|```|'''"
    # res_txt = re.sub(pattern, '', content)

    json_content = json.loads(res_txt)
    response = pd.DataFrame(json_content["answer"])
    response = response.transpose()[["question", "answer", "color", "source"]]
    response = response.rename(
        columns={
            "question": "Requisito",
            "answer": ("Resposta" + "_" + json_content["model"]),
            "color": ("Cor" + "_" + json_content["model"]),
            "source": ("Fonte" + "_" + json_content["model"])
        }
    )

    # response["Requisito"] = response["Requisito"].str.replace("?", "")
    # response["Requisito"] = response["Requisito"].str.replace("$$$", "")
    # response["Requisito"] = response["Requisito"].str.replace("\n", "")
    # response["Requisito"] = response["Requisito"].str.replace(";;", ";")

    if ((response["Requisito"].values[0])[-1]) != ";":
        response["Requisito"] = response["Requisito"] + ";"
        
    response["Item"] = response.index.astype(str).str.replace("QUESTION_", "")        
    response["Item"] = response["Item"].astype("Int64")
    response.drop("Requisito", axis=1, inplace=True)

    # response.index = response.index.astype(str) + ';'
    # response["Requisito"] = response.index

    return response

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
