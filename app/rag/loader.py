from pathlib import Path

from langchain_community.document_loaders import TextLoader


DOCUMENTS_PATH = Path("data/documents")


def load_documents():
    documents = []

    print(f"Diretório: {DOCUMENTS_PATH.resolve()}")
    print(f"Existe: {DOCUMENTS_PATH.exists()}")

    files = list(DOCUMENTS_PATH.glob("*.md"))

    print(f"Arquivos encontrados: {files}")

    for file_path in files:
        print(f"Carregando: {file_path}")

        # abre o arquivo
        loader = TextLoader(
            str(file_path),
            encoding="utf-8",
        )
        # transforma o conteúdo em objetos Document do LangChain.
        documents.extend(loader.load())

    return documents