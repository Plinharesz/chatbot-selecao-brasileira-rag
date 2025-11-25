# Resolução do Exercício de PLN - Tokenização e Normalização

Este repositório contém a resolução do exercício de Processamento de Linguagem Natural proposto.

## Arquivos

- `nlp_exercise.py`: Script Python contendo a implementação da solução.
- `README.md`: Este arquivo, explicando a solução.

## Pré-requisitos

Para executar o código, é necessário instalar as bibliotecas listadas abaixo. Recomenda-se o uso de um ambiente virtual.

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
pip install nltk spacy
python -m spacy download pt_core_news_sm
```

## Implementação

O script `nlp_exercise.py` realiza as seguintes etapas:

1.  **Tokenização**: O texto é dividido em tokens (palavras) usando espaços como delimitador inicial.
2.  **Normalização**: O texto é convertido para minúsculas e a pontuação é removida utilizando expressões regulares (`re`).
3.  **Remoção de Stop Words**: Palavras irrelevantes (artigos, preposições, etc.) são removidas utilizando a lista de stop words do `nltk` para o português.
4.  **Geração de N-gramas**: São gerados unigramas, bigramas e trigramas a partir dos tokens filtrados.
5.  **Lematização**: As palavras são reduzidas à sua forma base (lema) utilizando a biblioteca `spacy` com o modelo `pt_core_news_sm`.

## Como Executar

Certifique-se de estar com o ambiente virtual ativado e as dependências instaladas.

```bash
python nlp_exercise.py
```

## Resultados Esperados

O script imprimirá no console o resultado de cada etapa do processamento, demonstrando a evolução do texto desde a forma bruta até a forma lematizada.
