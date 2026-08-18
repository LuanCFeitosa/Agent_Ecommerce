from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from llm import get_embeddings


# =========================
# CARREGAMENTO DO PDF
# =========================

loader = PyPDFLoader("dados/FAQ.pdf")

documentos = loader.load()

print(f"Quantidade de páginas: {len(documentos)}")


# =========================
# DIVISÃO DOS DOCUMENTOS
# =========================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)

chunks = splitter.split_documents(documentos)

print(f"Quantidade de chunks: {len(chunks)}")


# =========================
# BANCO VETORIAL
# =========================

vectorstore = FAISS.from_documents(
    chunks,
    get_embeddings()
)


# =========================
# RETRIEVER
# =========================

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}
)


# =========================
# BUSCA NO CATÁLOGO
# =========================

def buscar_catalogo(pergunta: str) -> str:

    documentos_relevantes = retriever.invoke(pergunta)

    if not documentos_relevantes:
        return "Nenhuma informação relevante encontrada."

    contexto = "\n\n".join(
        documento.page_content
        for documento in documentos_relevantes
    )

    return contexto