from app.tools.erp_tools import ErpTools


BELEZA_ID = "mock-ml-suse"


def main():
    tools = ErpTools()

    result = tools.get_cancelled_os(
        BELEZA_ID
    )

    print(
        f"Total de OS canceladas: "
        f"{result['total']}"
    )

    print("\nPrimeiras OS:")

    for os in result["os"][:10]:
        print(
            os["numero"],
            os["cliente"],
            os["pagamento_pendente"],
        )


if __name__ == "__main__":
    main()