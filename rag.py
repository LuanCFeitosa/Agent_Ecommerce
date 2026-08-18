from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from llm import get_embeddings

# =========================
# CONFIGURAÇÃO DO SPLITTER
# =========================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)

# =========================
# BASE VETORIAL INICIAL (FAQ)
# =========================

loader = PyPDFLoader("dados/FAQ.pdf")
documentos = loader.load()
chunks = splitter.split_documents(documentos)

vectorstore = FAISS.from_documents(
    chunks,
    get_embeddings()
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}
)

# =========================
# ADICIONAR NOVOS PDFS (STREAMLIT)
# =========================

def processar_e_salvar_pdf(caminho_arquivo: str):
    """Carrega um novo PDF enviado e adiciona seus vetores ao FAISS existente."""
    loader_novo = PyPDFLoader(caminho_arquivo)
    novos_docs = loader_novo.load()
    novos_chunks = splitter.split_documents(novos_docs)
    
    # Adiciona os novos chunks na base FAISS em memória
    vectorstore.add_documents(novos_chunks)


# =========================
# BUSCA NO CATÁLOGO
# =========================

def buscar_base(pergunta: str) -> str:

    documentos_relevantes = retriever.invoke(pergunta)

    if not documentos_relevantes:
        return "Nenhuma informação relevante encontrada."

    contexto = "\n\n".join(
        documento.page_content
        for documento in documentos_relevantes
    )

    return contexto