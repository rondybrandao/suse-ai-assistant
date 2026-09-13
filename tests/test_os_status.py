from collections import Counter

from app.suse.os_service import OsService


BELEZA_ID = "mock-ml-suse"


def main():
    service = OsService()

    os_list = service.listar(
        BELEZA_ID
    )

    combinations = Counter(
        (
            os.get("status"),
            os.get("pendencias", {}).get("pagamento"),
        )
        for os in os_list
    )

    print(
        f"Total de OS: {len(os_list)}"
    )

    print("\nCombinações encontradas:")

    for (status, pagamento), quantidade in sorted(
        combinations.items()
    ):
        print(
            f"status={status:<25} "
            f"pagamento={str(pagamento):<5} "
            f"quantidade={quantidade}"
        )


if __name__ == "__main__":
    main()