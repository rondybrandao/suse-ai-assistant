from app.rag.router import route_question

def main():
    questions = [
        "Quantas OS estão canceladas?",
        "Quantas OS estão aguardando aprovação?",
        "Como funciona o processo de fechamento de uma OS?",
    ]

    for question in questions:
        route = route_question(question)

        print(
            f"Pergunta: {question}"
        )

        print(
            f"Rota: {route}\n"
        )

if __name__ == "__main__":
    main()