from langchain.agents import create_react_agent
from langchain.agents import AgentExecutor
from langchain.prompts import PromptTemplate

from ferramentas import criar_ferramentas
from llm import get_llm


# =========================
# FERRAMENTAS
# =========================

tools = criar_ferramentas()


# =========================
# PROMPT DO AGENTE
# =========================

prompt_react = PromptTemplate(
    input_variables=[
        "input",
        "agent_scratchpad",
        "tools",
        "tool_names"
    ],
    template="""
Você é um assistente virtual de e-commerce.

Você sempre responde em português.

Sua função é ajudar clientes a encontrar produtos
e obter informações sobre o catálogo da loja.

Você possui acesso às seguintes ferramentas:

{tools}

Utilize as ferramentas quando precisar consultar
informações sobre produtos.

Nunca invente produtos, preços ou especificações.

Se uma informação não estiver disponível no catálogo,
informe claramente ao cliente.

Use o seguinte formato:

Question: a pergunta do cliente

Thought: pense sobre o que precisa ser feito

Action: a ferramenta que deve ser utilizada,
uma das [{tool_names}]

Action Input: entrada para a ferramenta

Observation: resultado da ferramenta

... (esse processo pode se repetir)

Thought: Agora eu sei a resposta final

Final Answer: resposta final para o cliente

Question: {input}

Thought: {agent_scratchpad}
"""
)


# =========================
# AGENTE
# =========================

agente = create_react_agent(
    llm=get_llm(),
    tools=tools,
    prompt=prompt_react
)


# =========================
# EXECUTOR
# =========================

orquestrador = AgentExecutor(
    agent=agente,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)