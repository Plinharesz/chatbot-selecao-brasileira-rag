import os
import shutil
import csv
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Carrega a chave do arquivo .env (se tiver)
load_dotenv()

# --- CONFIGURAÇÕES ---
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CSV_FILE = DATA_DIR / "base_conhecimento_brasil.csv"
CHROMA_PATH = BASE_DIR / "chroma_db"

def main():
    # 1. Verifica se o arquivo CSV existe
    if not CSV_FILE.exists():
        print(f"❌ ERRO: O arquivo não foi encontrado em: {CSV_FILE}")
        print("Certifique-se de que você tem o arquivo 'base_conhecimento_brasil.csv' dentro da pasta 'data'.")
        return

    print(f"👀 Lendo dados do arquivo: {CSV_FILE}")

    # 2. Limpar o Banco Antigo (Para não duplicar informações)
    if CHROMA_PATH.exists():
        try:
            shutil.rmtree(CHROMA_PATH)
            print("🗑️ Banco antigo limpo.")
        except:
            print("⚠️ Erro ao apagar pasta (talvez esteja em uso). Tente deletar 'chroma_db' manualmente.")

    # 3. Ingestão (Lê o CSV e transforma em memória)
    try:
        loader = CSVLoader(
            file_path=str(CSV_FILE), 
            source_column="Fato_Ou_Resposta", 
            encoding="utf-8"
        )
        documents = loader.load()
        print(f"📂 Carregando {len(documents)} fatos na memória...")
    except Exception as e:
        print(f"❌ Erro ao ler o CSV: {e}")
        return

    # 4. Treinando a IA
    print("🧠 Treinando a IA (Isso pode levar um pouco)...")
    try:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        Chroma.from_documents(documents, embeddings, persist_directory=str(CHROMA_PATH))
        print("✅ SUCESSO! O bot foi atualizado com as informações do seu arquivo CSV.")
        print("🚀 Agora pode rodar o 'app.py'!")
    except Exception as e:
        print(f"❌ Erro na IA: {e}")

if __name__ == "__main__":
    main()