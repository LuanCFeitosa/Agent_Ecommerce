from langchain.tools import tool

from rag import buscar_catalogo


# =========================
# CONSULTAR CATÁLOGO
# =========================

@tool
def consultar_catalogo(pergunta: str) -> str:
    """
    Consulta o FAQ da loja.

    Utilize esta ferramenta quando o vendedor perguntar sobre
    pagamento ou quando tiver dúvidas presente no índice do FAQ.
    """

    return buscar_catalogo(pergunta)


# =========================
# CRIAÇÃO DAS FERRAMENTAS
# =========================

def criar_ferramentas():

    return [
        consultar_catalogo
    ]