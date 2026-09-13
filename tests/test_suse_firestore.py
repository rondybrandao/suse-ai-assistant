from app.suse.os_service import OsService


BELEZA_ID = "mock-ml-suse"


def main():
    service = OsService()

    os_list = service.listar_canceladas(
        BELEZA_ID
    )

    print(
        f"OS canceladas: {len(os_list)}"
    )

    for os in os_list[:10]:
        print(
            os.get("numero"),
            os.get("status"),
            os.get("cliente", {}).get("nome"),
            os.get("pendencias", {}).get("pagamento"),
        )



if __name__ == "__main__":
    main()