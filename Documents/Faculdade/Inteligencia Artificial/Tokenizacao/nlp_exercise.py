import re
import nltk
import spacy
from nltk.corpus import stopwords
from nltk.util import ngrams

# Download necessary NLTK data
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Corpus
corpus = 'A Sra. Rosa plantou uma rosa no jardim. O céu estava azul e a brisa era suave. Ela pensou: "Seria maravilhoso se todos os dias fossem assim, tão tranquilos quanto uma rosa em flor."'

print("--- 1. Tokenização (por espaços) ---")
# 1. Tokenização: Identificação de palavras distintas no texto.
# A princípio, considere apenas a separação por espaços, sem remoção de pontuação.
tokens_raw = corpus.split()
print(tokens_raw)
print("\n")

print("--- 2. Normalização ---")
# 2. Normalização: Conversão para letras minúsculas e remoção de pontuações.
# Modifique o algoritmo para remover pontuações e converter todas as palavras para letras minúsculas.
# Usando regex para remover pontuação e .lower() para minúsculas.
# Mantendo a estrutura de tokens, mas limpando cada um ou re-tokenizando.
# A instrução sugere: "Modifique o algoritmo para remover pontuações e converter todas as palavras para letras minúsculas."
# Vamos limpar o texto e depois tokenizar, ou limpar os tokens.
# O exemplo do README usa re.findall(r'\w+', text.lower()) que já remove pontuação e tokeniza.
normalized_tokens = re.findall(r'\w+', corpus.lower())
print(normalized_tokens)
print("\n")

print("--- 3. Remoção de Stop Words ---")
# 3. Remoção de palavras irrelevantes (stop words).
stop_words = set(stopwords.words('portuguese'))
filtered_tokens = [word for word in normalized_tokens if word not in stop_words]
print(filtered_tokens)
print("\n")

print("--- 4. Geração de n-gramas ---")
# 4. Geração de n-gramas: Consideração de palavras como grupos (uni, bi, trigrama).
unigrams = list(ngrams(filtered_tokens, 1))
bigrams = list(ngrams(filtered_tokens, 2))
trigrams = list(ngrams(filtered_tokens, 3))

print("Unigrams:", unigrams)
print("Bigrams:", bigrams)
print("Trigrams:", trigrams)
print("\n")

print("--- 5. Lematização ---")
# 5. Lematização: Redução de palavras à sua raiz comum.
# Utilize o spacy para aplicar a lematização no texto.
# Precisamos passar o texto original ou os tokens filtrados?
# O README diz: "Utilize o spacy para aplicar a lematização no texto." e mostra:
# doc = nlp(" ".join(filtered_tokens))
# lemmatized = [token.lemma_ for token in doc]

nlp = spacy.load('pt_core_news_sm')
# Recriando um texto a partir dos tokens filtrados para o spacy processar, 
# ou processando o texto original e filtrando depois?
# O exemplo do README sugere processar os tokens filtrados: doc = nlp(" ".join(filtered_tokens))
doc = nlp(" ".join(filtered_tokens))
lemmatized = [token.lemma_ for token in doc]
print(lemmatized)