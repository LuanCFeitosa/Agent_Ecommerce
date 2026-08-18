import streamlit as st


st.set_page_config(
    page_title="Assistente de E-commerce",
    page_icon="🛒",
    layout="centered"
)

import tempfile
from agente import orquestrador
import rag


@st.cache_resource
def obter_base_conhecimento():
    return rag.carregar_vectorstore()

vectorstore = obter_base_conhecimento()


st.title("🛒 Assistente de E-commerce")

st.info("""
Este assistente utiliza inteligência artificial 
para consultar documentos PDF e responder perguntas.

Você pode perguntar sobre:

- Devoluções 
- Afiliados 
- Prazos
- Garantias 
- Informações Gerais

Também é possível enviar novos PDFs para que o assistente aprenda sobre eles.

""")


# =========================
# HISTÓRICO
# =========================

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []


for mensagem in st.session_state.mensagens:

    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])

with st.sidebar:
    st.header("📄 Adicionar Conhecimento")
    pdf_enviado = st.file_uploader("Envie um arquivo PDF", type=["pdf"])

    if pdf_enviado is not None:
        if st.button("Indexar PDF"):
            with st.spinner("Processando e salvando na base vetorial..."):
                # Salva o arquivo temporariamente no disco para o loader do LangChain ler
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(pdf_enviado.read())
                    caminho_temp = tmp_file.name

                # Executa a função de ingestão que dividirá o PDF e salvará no banco vetorial
                rag.processar_e_salvar_pdf(caminho_temp)
                st.success("✅ Conteúdo do PDF adicionado com sucesso!")


# =========================
# CHAT
# =========================

pergunta = st.chat_input(
    "Pergunte algo sobre nossos produtos..."
)


if pergunta:

    st.chat_message("user").markdown(pergunta)

    st.session_state.mensagens.append({
        "role": "user",
        "content": pergunta
    })


    with st.chat_message("assistant"):

        with st.spinner("Consultando a base de conhecimento..."):

            resposta = orquestrador.invoke({
                "input": pergunta
            })

            resposta_final = resposta["output"]

        st.markdown(resposta_final)


    st.session_state.mensagens.append({
        "role": "assistant",
        "content": resposta_final
    })