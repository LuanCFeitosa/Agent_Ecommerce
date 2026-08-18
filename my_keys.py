import os
from dotenv import load_dotenv

load_dotenv()

def GEMINI_API_KEY():
    return os.getenv("GOOGLE_API_KEY")
