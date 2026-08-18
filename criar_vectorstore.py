from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from llm import get_embeddings


# =========================
# CARREGAR PDF
# =========================

loader = PyPDFLoader("dados/FAQ.pdf")

documentos = loader.load()

print(f"Páginas: {len(documentos)}")


# =========================
# CRIAR CHUNKS
# =========================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)

chunks = splitter.split_documents(documentos)

print(f"Chunks: {len(chunks)}")


# =========================
# CRIAR EMBEDDINGS
# =========================

print("Gerando embeddings...")

embeddings = get_embeddings()


# =========================
# CRIAR FAISS
# =========================

vectorstore = FAISS.from_documents(
    chunks,
    embeddings
)


# =========================
# SALVAR
# =========================

vectorstore.save_local("vectorstore")

print("FAISS criado com sucesso!")