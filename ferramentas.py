from langchain.tools import tool

from rag import buscar_base


# =========================
# CONSULTAR CATÁLOGO
# =========================

@tool
def consultar_base(pergunta: str) -> str:
    """
    Consulta a base de conhecimento da loja (FAQ, manuais, catálogos e PDFs anexados).
    Utilize esta ferramenta sempre que o usuário perguntar sobre produtos,
    preços, pagamento, especificações ou qualquer dúvida presente nos documentos da loja.
    """

    return buscar_base(pergunta)


# =========================
# CRIAÇÃO DAS FERRAMENTAS
# =========================

def criar_ferramentas():

    return [
        consultar_base
    ]