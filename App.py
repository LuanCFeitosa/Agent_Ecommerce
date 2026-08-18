import streamlit as st

from agente import orquestrador


st.set_page_config(
    page_title="Assistente de E-commerce",
    page_icon="🛒",
    layout="centered"
)


st.title("🛒 Assistente de E-commerce")

st.info("""
Este assistente utiliza inteligência artificial e RAG
para consultar o catálogo de produtos.

Você pode perguntar sobre:

📱 Produtos  
💰 Preços  
💾 Especificações  
🔎 Características  
📦 Informações disponíveis no catálogo
""")


# =========================
# HISTÓRICO
# =========================

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []


for mensagem in st.session_state.mensagens:

    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])


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

        with st.spinner("Consultando o catálogo..."):

            resposta = orquestrador.invoke({
                "input": pergunta
            })

            resposta_final = resposta["output"]

        st.markdown(resposta_final)


    st.session_state.mensagens.append({
        "role": "assistant",
        "content": resposta_final
    })