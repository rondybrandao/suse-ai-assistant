from app.suse.os_service import OsService


BELEZA_ID = "mock-ml-suse"


def main():
    service = OsService()

    os_list = service.listar(
        BELEZA_ID
    )

    print(
        f"OS encontradas: {len(os_list)}"
    )

    for os in os_list[:5]:
        print(
            os.get("numero"),
            os.get("status"),
            os.get("cliente", {}).get("nome"),
        )


if __name__ == "__main__":
    main()