import os
import re
from openai import OpenAI
import json
import pandas as pd

client = OpenAI(
    api_key= os.getenv('API_KEY')
)


def get_assistant():
    assistants = client.beta.assistants.list()
    for assistant in assistants:
        if assistant.name == "Tech Analyst Assistant v3":
            # client.beta.assistants.delete(assistant.id)
            return assistant

    assistant = client.beta.assistants.create(
        name="Tech Analyst Assistant v3",
        description="You are a PDF extractor and retrieval assistant.\
            You will recieve an input message containing a PDF file of a model or series of equipment and a list of requirements.\
            The series of requirements that should be answered based on the PDF content are delimited by ####.\
            The start of each requirement asking for specific information or capability is delimited by $$$",
        instructions='1. Read the PDF content.\n\
                    2. Extract the relevant information \n\
                    3. Give a answer related to every requirement, based on the PDF content using the least amount of words possible and None if the specification do not say anything related to the requirement \n\
                    4. Assign a color to every answer, being green - requirement met, yellow - not enough information, red - requirement not met but has the information\n\
                    4. Format the answer according to the following JSON scheme:\n\
                    {\n\
"model": {Name of the Equipment Model},\n\
"answer":{\n\
	"QUESTION_1":{\n\
		"question": {Requirement being searched},\n\
		"answer" : {Answer to the question},\n\
		"source": {Section of the PDF that the Answer was based on}\n\
        "color" : {Color asssigned to the answer} \n\
		},\n\
	"QUESTION_2": {\n\
		"question": {Requirement being searched},\n\
		"answer" : {Answer to the question},\n\
		"source": {Section of the PDF that the Answer was based on}\n\
        "color" : {Color asssigned to the answer} \n\
		}\n\
	}\n\
}',
        model="gpt-4o-mini",
        tools=[{"type": "file_search"}],
    )
    return assistant


def create_vector_store_multiple(arquivos):
    for arq in arquivos:
        if not os.path.exists(arq):
            print("Erro: Arquivo não encontrado: " + arq)
            return None

    vector_store = client.beta.vector_stores.create(
        name="Multiplas_especificacoes",
        file=[open(arq, "rb") for arq in arquivos],
        purpose="assistants",
    )

    vector_stores = client.beta.vector_stores.list()
    for vector_store in vector_stores:
        if vector_store.name == "Multiplas_especificacoes":
            file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
                vector_store_id=vector_store.id,
                files=[open(arq, "rb") for arq in arquivos],
            )
            return vector_store

    print(vector_store.status)
    print(vector_store.file_counts)
    return vector_store


def create_vector_store_single(arq):
    vector_stores = client.beta.vector_stores.list()

    for vector_store in vector_stores:
        if vector_store.name == "Especificacao_unica":
            temporario = client.beta.vector_stores.files.list(vector_store.id)
            for file in temporario:
                client.files.delete(file.id)
            client.beta.vector_stores.delete(vector_store.id)

    if not os.path.exists(arq):
        print("Erro: Arquivo não encontrado: " + arq)
        return None

    vector_store = client.beta.vector_stores.create(name="Especificacao_unica")
    file_streams = [open(arq, "rb")]
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )

    print(file_batch.status)
    print(file_batch.file_counts)

    return vector_store


def create_thread(assistant, vector_store, questions):
    assistant = client.beta.assistants.update(
        assistant_id=assistant.id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )
    teste = "####\n " + questions

    thread = client.beta.threads.create(
        messages=[{"role": "user", "content": teste}],
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )

    print(thread.tool_resources.file_search)

    return assistant, thread


def create_run(assistant, thread):

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id, assistant_id=assistant.id
    )
    messages = list(
        client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id)
    )

    message_content = messages[0].content[0].text
    annotations = message_content.annotations
    citations = []
    for index, annotation in enumerate(annotations):
        message_content.value = message_content.value.replace(
            annotation.text, f"[{index}]"
        )
        if file_citation := getattr(annotation, "file_citation", None):
            cited_file = client.files.retrieve(file_citation.file_id)
            citations.append(f"[{index}] {cited_file.filename}")

    # print(message_content.value)
    # print("\n".join(citations))

    return message_content.value, citations, messages


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
    response = response.transpose()[["question", "answer", "color"]]
    response = response.rename(
        columns={
            "question": "Requisito",
            "answer": ("Resposta" + "_" + json_content["model"]),
            "color": ("Cor" + "_" + json_content["model"]),
        }
    )

    response["Requisito"] = response["Requisito"].str.replace("?", "")

    if ((response["Requisito"].values[0])[-1]) != ";":
        response["Requisito"] = response["Requisito"] + ";"

    # response.index = response.index.astype(str) + ';'
    # response["Requisito"] = response.index

    return response


def delete_vector_store(vector_store):
    client.beta.vector_stores.delete(vector_store.id)


def stop_assistant(assistant):
    client.beta.assistants.delete(assistant.id)


# Create a vector store caled "Financial Statements"
# vector_store = client.beta.vector_stores.create(name="Financial Statements")
# client.beta.vector_stores.delete(vector_store.id)

# You can print the status and the file counts of the batch to see the result of this operation.
# print(file_batch.status)
# print(file_batch.file_counts)

# The thread now has a vector store with that file in its tool resources.
# print(thread.tool_resources.file_search)

# Use the create and poll SDK helper to create a run and poll the status of
# the run until it's in a terminal state.
