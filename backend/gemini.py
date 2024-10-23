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
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
        system_instruction="You are a PDF extractor and retrieval assistant.\\\nYou will recieve an input message containing a PDF file of a model or series of equipment and a list of requirements.\\\nThe series of requirements that should be answered based on the PDF content are delimited by ####.\\\nThe start of each requirement asking for specific information or capability is delimited by $$$\nYour instructions are described bellow:\n1. Read the PDF content.\\n\\\n                    2. Extract the relevant information \\n\\\n                    3. Give a answer related to every requirement, based on the PDF content using the least amount of words possible and None if the specification do not say anything related to the requirement \\n\\\n                    4. Assign a color to every answer, being green - requirement met, yellow - not enough information, red - requirement not met but has the information\\n\\\n                    4. Format the answer according to the following JSON scheme:\\n\\\n                    {\\n\\\n\"model\": {Name of the Equipment Model},\\n\\\n\"answer\":{\\n\\\n\t\"QUESTION_1\":{\\n\\\n\t\t\"question\": {Requirement being searched},\\n\\\n\t\t\"answer\" : {Answer to the question},\\n\\\n\t\t\"source\": {Section of the PDF that the Answer was based on}\\n\\\n        \"color\" : {Color asssigned to the answer} \\n\\\n\t\t},\\n\\\n\t\"QUESTION_2\": {\\n\\\n\t\t\"question\": {Requirement being searched},\\n\\\n\t\t\"answer\" : {Answer to the question},\\n\\\n\t\t\"source\": {Section of the PDF that the Answer was based on}\\n\\\n        \"color\" : {Color asssigned to the answer} \\n\\\n\t\t}\\n\\\n\t}\\n\\\n}\n",
    )
    
    return model

# # TODO Make these files available on the local file system
# # You may need to update the file paths
# files = [
#   upload_to_gemini("HPE Aruba Networking CX 6200 switch series-a00097415enw.pdf", mime_type="application/pdf"),
# ]

# # Some files have a processing delay. Wait for them to be ready.
# wait_for_files_active(files)

# chat_session = model.start_chat(
#   history=[
#     {
#       "role": "user",
#       "parts": [
#         files[0],
#         "$$$ Deve possuir no mínimo 36 portas 10/100/1000BaseT Gigabit Ethernet BaseT\n$$$ Deve possuir no mínimo 12 portas SmartRate 1G/2.5G/5G BaseT Gigabit Ethernet BaseT\n$$$ Deve possuir 2 portas adicionais com velocidade de 1/10G SFP+ LRM;\n$$$ Deve possuir 2 portas adicionais com velocidade de 1/10G SFP+ LRM/MACSec 256;\n$$$ Deve possuir 1 interface RJ-45;\n$$$ Deve possuir USB-C ou serial para acesso console local;\n$$$ Deve possuir uma interface de gerenciamento out of band;\n$$$ Deve possuir memória RAM de no mínimo 8 Gbytes;\n$$$ Deve possuir memória Flash de no mínimo 16 Gbytes;\n$$$ Deve possuir buffer de pacotes de no mínimo 8 Mbytes;\n$$$ Deve possuir capacidade de encaminhamento de no mínimo 202 Mpps;\n$$$ Deve possuir capacidade de comutação de no mínimo 272 Gbps;\n$$$ Deve possui capacidade de empilhamento com até 8 elementos na pilha, sendo gerenciados atraves de um único IP.\n$$$ O switch deve ser do tipo standalone, com altura máxima de 1RU e instalação em rack (19\"). Deve acompanhar todos os componentes necessários para sua fixação no rack;\n$$$ O switch deve vir acompanhado do kit de instalação em rack.\n$$$ Deve suportar até 1440W PoE Classe 6;\n$$$ Deve possuir fonte de alimentação redundante, hot-swapple 100/240VAC;\n$$$ Deve possuir Certificado de Homologação na Anatel, de acordo com a Resolução nº 242;\n$$$ Deve possuir VLAN 802.1Q;\n$$$ Deve possuir 802.1V;\n$$$ Deve possuir BPDU;\n$$$ Deve realizar Jumbo Packets de no mínimo 9000 bytes;\n$$$ Deverá realizar Port Mirroring com no mínimo 4 grupos de espelhamento;\n$$$ Deve implementar funcionalidade que permita a detecção de links unidirecionais;\n$$$ Deve implementar 4094 VLAN Ids;\n$$$ Deve implementar MVRP (Multiple VLAN Registration Protocol);\n$$$ Deve implementar LLDP (IEEE 802.1ab);\n$$$ Deve implementar LLDP-MED;\n$$$ Deve implementar RPVST+ ou protocolo compatível;\n$$$ Deve implementar MSTP (IEEE 802.1s);\n$$$ Deve implementar MVRP;\n$$$ Deve implementar IGMP;\n$$$ Deve implementar túneis VxLAN (VTEP);\n$$$ Deve possuir capacidade mínima da tabela MAC de 16 mil entradas.\n$$$ Deve implementar roteamento estático;\n$$$ Deve implementar OSPF;\n$$$ Deve implementar OSPFv3;\n$$$ Deve implementar servidor DHCP;\n$$$ Deve suportar no mínimo 2 mil rotas IPV4 e 1 mil rotas IPv6.\n$$$ Deve implementar controle de broadcast e multicast;\n$$$ Deve implementar rate limiting para pacotes ICMP;\n$$$ Deve implementar Strict priority (SP) queuing e Deficit Weighted Round Robin (DWRR)\n$$$ Deve implementar priorização de trafego em tempo real\n$$$ Deve suportar IPSLA\n$$$ Deve implementar priorização de tráfego com no mínimo os seguintes parâmetros: endereço IP, Tipo de Serviço, Número da porta TCP/UDP, porta de origem e Diffserv.\n$$$ Deve suporta pelo no mínimo oito filas de priorização de tráfego\n$$$ Deve suportar ACL para IPv4 e IPv6\n$$$ Deve implementar Acl com base no IP de origem e destino, porta TCP e UDP de origem e destino baseada em VLAN ou por Porta.\n$$$ Deve suportar controle de acesso baseado em perfis (Role Based Access Control)\n$$$ Deve implementar 802.1x;\n$$$ Deve implementar autenticação baseada em web;\n$$$ Deve implementar autenticação baseada em endereço MAC;\n$$$ Deve permitir a utilização simultânea de autenticação 802.1x, WEB e MAC em uma mesma porta, com suporte a até 32 sessões simultâneas;\n$$$ Deve implementar TACACS+. Não serão aceitas soluções similares;\n$$$ Deve ter proteção contra-ataque na CPU do switch para prevenção de desligamento do appliance\n$$$ Deve implementar NTP;\n$$$ Deve suportar duas imagens de software no flash;\n$$$ Deve suportar múltiplos arquivos de configuração no flash;\n$$$ Deve suportar a autoconfiguração dos switches através de DHCP e software de gerenciamento, sem necessidade de nenhuma intervenção no switch (com configuração de fábrica);\n$$$ Deve suportar detecção de falha e link entre switches;\n$$$ Deve implementar sFlow;\n$$$ Deve possuir interface web para configuração;\n$$$ Deve implementar Syslog;\n$$$ Deve implementar Secure SFTP (SFTP);\n$$$ Deve implementar SNMP v1/v2/v3\n$$$ Deve implementar compatibilidade com o protocolo CDP para provisionamento de telefones IP;\n$$$ Deve possuir integração com App de gestão e configuração do mesmo fabricante.\n$$$ Deve suportar o encaminhamento de tráfego para gateway do mesmo fabricante para inspeção e controle de acesso;",
#       ],
#     }
#   ]
# )

# response = chat_session.send_message("INSERT_INPUT_HERE")

# print(response.text)



def search_requirement(rfp, base):
    genai.configure(api_key=os.getenv('API_KEY'))

    questoes = ""

    for questao in rfp["Requisito"]:
        questoes += "$$$ " + questao + "\n"


    arquivos = base["Local"].unique()

    saidas = []
    # total_arquivos = len(arquivos)
    # qtd = 1 / arquivos.size
    

    for idx, arq in enumerate(arquivos):
        file = upload_to_gemini(arq, mime_type="application/pdf")
        wait_for_files_active([file])
        model = create_model()
        chat_session = model.start_chat()
        output = chat_session.send_message([file, questoes])
        output = output.text
        saidas.append(output)
        output = format_output(output)
        id1 = "_" + str(random.randint(0, 100000000))
        id2 = "_" + str(random.randint(0, 100000000))
        rfp = rfp.merge(output, on="Item", how="left", suffixes=(id1, id2))
        if ((idx+1)%2 ==0): 
            print("Sleeping for 60 seconds - API key limit")
            time.sleep(60)

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