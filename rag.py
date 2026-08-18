import os
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from llm import get_embeddings

CAMINHO_FAISS = "vectorstore"

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)

# O Streamlit guarda esse banco na memória RAM após a 1ª execução
@st.cache_resource
def carregar_vectorstore():
    if not os.path.exists(CAMINHO_FAISS):
        return None
        
    embeddings = get_embeddings()
    return FAISS.load_local(
        CAMINHO_FAISS,
        embeddings,
        allow_dangerous_deserialization=True
    )

def buscar_base(pergunta: str) -> str:
    # Recupera o banco instantaneamente da memória do Streamlit
    vectorstore = carregar_vectorstore()

    if not vectorstore:
        return "A base de dados não foi encontrada."

    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    documentos_relevantes = retriever.invoke(pergunta)

    if not documentos_relevantes:
        return "Nenhuma informação relevante encontrada."

    return "\n\n".join(doc.page_content for doc in documentos_relevantes)

def processar_e_salvar_pdf(caminho_arquivo: str):
    loader = PyPDFLoader(caminho_arquivo)
    documentos = loader.load()
    novos_chunks = splitter.split_documents(documentos)

    vectorstore = carregar_vectorstore()
    
    if vectorstore is None:
        # Cria um novo se não existir
        vectorstore = FAISS.from_documents(novos_chunks, get_embeddings())
    else:
        # Adiciona aos existentes
        vectorstore.add_documents(novos_chunks)

    vectorstore.save_local(CAMINHO_FAISS)
    
    # Limpa o cache para o Streamlit reconhecer os novos PDFs adicionados
    st.cache_resource.clear()