import csv
from pathlib import Path

# --- CONFIGURAÇÕES ---
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

ARQUIVO_ORIGINAL = DATA_DIR / "base_conhecimento_brasil.csv"
ARQUIVO_NOVO = DATA_DIR / "novos_jogos.csv"

def integrar_dados():
    if not ARQUIVO_NOVO.exists():
        print(f"❌ Erro: Não achei o arquivo {ARQUIVO_NOVO}")
        return

    # Lista para guardar as novas linhas formatadas
    novas_linhas = []

    print("🔄 Lendo e convertendo os novos jogos...")
    
    # Lendo o CSV complexo do seu amigo
    # ATENÇÃO: Se o arquivo dele usar ponto e vírgula (;) mude o delimiter abaixo
    with open(ARQUIVO_NOVO, mode='r', encoding='utf-8') as f:
        leitor = csv.DictReader(f, delimiter=',') 
        
        for linha in leitor:
            # Aqui acontece a mágica: Transformamos as colunas em TEXTO CORRIDO
            
            # Tratamento para evitar erro se faltar dado
            data = linha.get('Data', 'Data desconhecida')
            partida = linha.get('Partida', 'Partida desconhecida')
            estadio = linha.get('Local', 'Local desconhecido')
            cidade = linha.get('Cidade', '')
            gols = linha.get('Gols', 'Não informado')
            mandante = linha.get('Escalacao_Mandante', '')
            visitante = linha.get('Escalacao_Visitante', '')

            texto_fato = (
                f"Registro de Partida: Em {data}, aconteceu o jogo {partida}. "
                f"O confronto foi um {linha.get('Tipo', 'jogo')} realizado no {estadio} em {cidade}. "
                f"Detalhes dos gols: {gols}. "
                f"Escalação do Mandante: {mandante}. "
                f"Escalação do Visitante: {visitante}."
            )

            # Criando a linha no formato do SEU padrão (3 colunas)
            # Categoria, Subcategoria, Fato
            nova_linha = ["Partidas", f"Jogo {data[-4:]}", texto_fato]
            novas_linhas.append(nova_linha)

    print(f"✅ Processados {len(novas_linhas)} jogos.")
    print("💾 Salvando no seu banco de conhecimento principal...")

    # Escrevendo no seu arquivo original (Modo 'a' = Append/Adicionar ao final)
    with open(ARQUIVO_ORIGINAL, mode='a', newline='', encoding='utf-8') as f:
        escritor = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        escritor.writerows(novas_linhas)

    print("🚀 Sucesso! As partidas foram adicionadas ao 'base_conhecimento_brasil.csv'.")
    print("Agora rode o 'python criar_banco.py' para atualizar a IA.")

if __name__ == "__main__":
    integrar_dados()
    