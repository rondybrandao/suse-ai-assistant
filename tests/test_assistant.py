from app.rag.assistant import Assistant


BELEZA_ID = "mock-ml-suse"


def main():
    assistant = Assistant()

    question = "Quantas OS estão finalizadas?"

    answer = assistant.answer(
        question,
        BELEZA_ID,
    )

    print(f"Pergunta: {question}")
    print(f"Resposta: {answer}")


if __name__ == "__main__":
    main()