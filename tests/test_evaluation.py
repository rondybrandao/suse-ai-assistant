import json

from app.evaluation.retrieval import calculate_recall_at_k

# Caminho do dataset de avaliação.
# Esse arquivo já contém as perguntas e os contextos
# recuperados pelo nosso pipeline RAG.
EVALUATION_FILE = "data/evaluation/rag_eval.json"

def load_evaluation_dataset():
    """
    Carrega o arquivo JSON e transforma seu conteúdo
    em uma lista de dicionários Python.
    """

    with open(
        EVALUATION_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)

def evaluate_retrieval(item):
    """
    Avalia o Retrieval de uma pergunta.

    Para isso precisamos saber quais chunks são
    considerados relevantes para a pergunta.
    """

    