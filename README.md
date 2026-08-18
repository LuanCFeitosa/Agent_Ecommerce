# 🛒 Assistente de E-commerce com RAG & Agente ReAct

Este projeto é um assistente virtual inteligente para e-commerce. Ele combina a técnica de **RAG (Retrieval-Augmented Generation)** com **Agentes do LangChain** (padrão ReAct) e modelos do **Google Gemini** para responder dúvidas sobre produtos, preços, especificações e políticas da loja com base em documentos PDF locais e dinâmicos.

---

## 📁 Estrutura do Projeto

```
projeto-ecommerce/
│
├── app.py
├── agente.py
├── ferramentas.py
├── rag.py
├── llm.py
├── my_keys.py
├── my_models.py
│
└── vectorstore/
│   └── index.faiss
│   └── index.pkl
└── dados/
    └── catalogo.pdf

```

## 🏗️ Arquitetura da Solução

O sistema opera com dois fluxos **distintos e complementares** e interface
```
                    ┌──────────────────────┐
                    │    FAQ.pdf / PDFs    │
                    │  Streamlit Upload    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │        rag.py        │
                    │ Embeddings           │
                    │ FAISS                │
                    │ Retriever            │
                    └──────────┬───────────┘
                               │
                               │ Contexto relevante
                               ▼
                    ┌──────────────────────┐
                    │      agente.py       │
                    │     ReAct Agent      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    ferramentas.py    │
                    │  consultar_base()    │
                    └──────────┬───────────┘
                               │
                               │ Tool
                               ▼
                    ┌──────────────────────┐
                    │        Gemini        │
                    │         LLM          │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       RESPOSTA       │
                    └──────────────────────┘
```

1. **Fluxo de Ingestion (Upload Dinâmico):**
   * O arquivo `dados/FAQ.pdf` já foi processado pela `criar_vectorstore` e salva na pasta `vecstore`.
   * O usuário pode enviar novos PDFs através do `file_uploader`.
   * O arquivo é divido em *chunks* (`RecursiveCharacterTextSplitter`), transformado em vetores (`GoogleGenerativeAIEmbeddings`) e adicionado ao índice **FAISS** em memória sem passar pelo agente.

2. **Fluxo de Consulta e Orquestração (ReAct):**
   * O usuário faz uma pergunta via interface de chat.
   * O **Agente ReAct** (`AgentExecutor`) analisa a pergunta e decide se precisa acionar a ferramenta `@tool`.
   * A ferramenta executa a busca por similaridade no banco vetorial FAISS através da função `buscar_base`.
   * Os trechos mais relevantes são devolvidos ao agente, que gera uma resposta precisa e fundamentada, evitando alucinações.
  
3. **Interface do Usuário (UI):**
   * Construída em **Streamlit**, permitindo chat interativo com histórico de conversa e upload de novos PDFs em tempo real.
  
## 🛠️ Tecnologias e Ferramentas

* **Linguagem:** Python 3.10+
* **Interface do Usuário:** Streamlit
* **Orquestração de IA:** LangChain (`langchain-google-genai`, `langchain-community`)
* **Modelo de Linguagem (LLM):** Google Gemini (`ChatGoogleGenerativeAI`)
* **Modelo de Embeddings:** `GoogleGenerativeAIEmbeddings` (`models/gemini-embedding-001`)
* **Banco Vetorial:** FAISS (`langchain-community.vectorstores`)
* **Processamento de PDFs:** `PyPDFLoader` (`pypdf`)

---

## 🚀 Instruções de Instalação e Execução

### 1. Clonar o Repositório e Criar o Ambiente Virtual

```bash
# Clone este repositório
git clone [https://github.com/seu-usuario/projeto-ecommerce.git](https://github.com/seu-usuario/projeto-ecommerce.git)
cd projeto-ecommerce

# Crie e ative o ambiente virtual
python -m venv .venv

# No Windows:
.venv\Scripts\activate
```

### 2. Instalar as Dependências

```bash
# Clone este repositório
pip install -r requirements.txt
```

### 4. Configurar a Chave de API
Crie um arquivo `.env` no diretório raiz ou configure a chave no seu projeto:
```python
# .env
GEMINI_API_KEY = "SUA_CHAVE_API_DO_GOOGLE_GEMINI"
```

### 5. Executar a aplicação
```bash
streamlit run App.py
```

---

## ❓ Exemplos de Perguntas Suportadas

O agente responde a dúvidas gerais baseadas nos documentos indexados:

* *"Quais são as formas de pagamento aceitas pela loja?"*
* *"Vocês oferecem parcelamento sem juros?"*
* *"Como funciona a política de troca e devolução?"*
---

## 💬 Exemplos do APP e de Respostas Geradas

<img width="1302" height="691" alt="image" src="https://github.com/user-attachments/assets/816b0528-bdb7-4c8e-a025-5e9be4d6ad9c" />

<img width="1303" height="681" alt="image" src="https://github.com/user-attachments/assets/9f4e495c-d236-43cb-8d99-a8c35ab5295c" />

## Link da Cloud:
* https://agentecommerceoci.streamlit.app





