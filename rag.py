from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from llm import get_embeddings


# =========================
# CONFIGURAÇÃO
# =========================

CAMINHO_FAISS = "vectorstore"

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)


# =========================
# CARREGAR FAISS
# =========================

def carregar_vectorstore():

    embeddings = get_embeddings()

    vectorstore = FAISS.load_local(
        CAMINHO_FAISS,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore


vectorstore = carregar_vectorstore()


retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}
)


# =========================
# ADICIONAR NOVO PDF
# =========================

def processar_e_salvar_pdf(caminho_arquivo: str):

    loader = PyPDFLoader(caminho_arquivo)

    documentos = loader.load()

    novos_chunks = splitter.split_documents(documentos)

    print(f"Páginas adicionadas: {len(documentos)}")
    print(f"Chunks adicionados: {len(novos_chunks)}")

    vectorstore.add_documents(novos_chunks)

    vectorstore.save_local(CAMINHO_FAISS)


# =========================
# BUSCA
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