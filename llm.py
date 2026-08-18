from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)

from my_keys import GEMINI_API_KEY
from my_models import GEMINI_FLASH


def get_llm():
    return ChatGoogleGenerativeAI(
        api_key=GEMINI_API_KEY(),
        model=GEMINI_FLASH()
    )


def get_embeddings():
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=GEMINI_API_KEY()
    )