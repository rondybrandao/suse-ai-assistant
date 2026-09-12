import json

from app.rag.embeddings import generate_embeddings
from app.rag.qdrant_client import search_similar
from app.rag.generator import generate_answer


# Caminho do dataset de avaliação.
# O arquivo contém as perguntas e as respostas esperadas.
EVALUATION_FILE = "data/evaluation/rag_eval.json"


def load_evaluation_dataset():
    """
    Carrega o dataset JSON de avaliação.

    json.load() transforma o conteúdo JSON em
    uma lista de dicionários Python.
    """

    with open(
        EVALUATION_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


def save_evaluation_dataset(dataset):
    """
    Salva o dataset atualizado no mesmo arquivo.

    indent=2 deixa o JSON formatado e fácil
    de ler manualmente.
    """

    with open(
        EVALUATION_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            dataset,
            file,
            ensure_ascii=False,
            indent=2,
        )


def process_question(question):
    """
    Executa o pipeline RAG para uma pergunta.

    Retorna:
        - contextos recuperados pelo Qdrant
        - resposta gerada pelo Gemini
    """

    # Converte a pergunta em um vetor numérico.
    # Esse vetor representa semanticamente a pergunta.
    query_embedding = generate_embeddings(
        [question]
    )[0]

    # Busca no Qdrant os chunks mais semelhantes
    # ao vetor da pergunta.
    results = search_similar(
        query_embedding,
        limit=5,
    )

    # Preserva os IDs do Qdrant.
    # Isso é importante para podermos calcular
    # Recall@K posteriormente.
    retrieved_ids = [
        result.id
        for result in results
    ]

    # Extrai somente o texto dos chunks recuperados.
    contexts = [
        result.payload["text"]
        for result in results
    ]

    # Envia a pergunta + contextos para o LLM
    # gerar a resposta baseada na documentação.
    answer = generate_answer(
        question,
        contexts,
    )

    return (retrieved_ids, contexts, answer)


def main():
    """
    Executa a avaliação para todas as perguntas
    existentes no dataset.
    """

    # Carrega todas as perguntas do arquivo JSON.
    dataset = load_evaluation_dataset()

    print()
    print("========================================")
    print("EXECUÇÃO DO RAG EVAL")
    print("========================================")

    # Percorre cada registro do dataset.
    for index, item in enumerate(
        dataset,
        start=1,
    ):

        question = item["question"]

        print()
        print("----------------------------------------")
        print(f"Pergunta {index}")
        print("----------------------------------------")
        print(question)

        # Executa Retrieval + Generation.
        retrieved_ids, contexts, answer = process_question(
            question
        )

        # Agora o dataset também guarda os IDs dos
        # chunks encontrados pelo Qdrant.
        item["retrieved_ids"] = retrieved_ids

        # Guarda os contextos recuperados
        # dentro do próprio dataset.
        item["retrieved_context"] = contexts

        # Guarda a resposta gerada pelo Gemini.
        item["generated_answer"] = answer

        print()
        print("IDs recuperados:")
        print(retrieved_ids)

        print()
        print("Contextos recuperados:")
        print(len(contexts))

        print()
        print("Resposta gerada:")
        print(answer)

    # Depois que todas as perguntas foram processadas,
    # salva novamente o dataset com os resultados.
    save_evaluation_dataset(dataset)

    print()
    print("========================================")
    print("RAG EVAL FINALIZADO")
    print("========================================")

    print(
        f"Perguntas processadas: {len(dataset)}"
    )

    print()
    print(
        f"Dataset atualizado: {EVALUATION_FILE}"
    )


if __name__ == "__main__":
    main()