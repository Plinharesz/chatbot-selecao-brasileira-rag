import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma
# MISTURA OS DOIS MUNDOS:
from langchain_huggingface import HuggingFaceEmbeddings # Busca Local (Grátis)
from langchain_google_genai import ChatGoogleGenerativeAI # Resposta Inteligente (Gemini)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CONFIGURAÇÕES ---
CHROMA_PATH = "chroma_db"
api_key = os.environ.get("GOOGLE_API_KEY")

print("⚽ Aquecendo o time...")

rag_chain = None

try:
    # 1. Embeddings LOCAIS (Tem que ser igual ao criar_banco.py)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # 2. Carrega Banco_de_Dados
    vector_store = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 15})
    
    # 3. LLM (Gemini continua gerando o texto final se ele nao ver a chave API)
    if not api_key:
        print("⚠️ AVISO: Sem chave GOOGLE_API_KEY, o chat não vai responder.")
    
    llm = ChatGoogleGenerativeAI(model="models/gemini-flash-latest", temperature=0.2, google_api_key=api_key)

    # 4. Prompt Bot_Selecao
    template = """
    Você é um especialista na Seleção Brasileira.
    Use o contexto abaixo para responder. Se não souber, diga que não tem a informação.
    
    Contexto: {context}
    Pergunta: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    
    def format_docs(docs):
        return "\n\n".join([doc.page_content for doc in docs])

    # 5. Chain
    rag_chain = (
        {"context": retriever | RunnableLambda(format_docs), "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    print("✅ Servidor Pronto!")

except Exception as e:
    print(f"❌ Erro ao iniciar: {e}")

class UserRequest(BaseModel):
    prompt: str

@app.post("/api/chat")
async def chat(request: UserRequest):
    if not rag_chain:
        return {"resposta": "Erro no servidor (IA não carregou)."}
    try:
        resposta = rag_chain.invoke(request.prompt)
        return {"resposta": resposta}
    except Exception as e:
        return {"resposta": f"Erro: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)