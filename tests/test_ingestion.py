from app.rag.loader import load_documents
from app.rag.chunker import split_documents


documents = load_documents()

print(f"Documentos carregados: {len(documents)}")

chunks = split_documents(documents)

print(f"Chunks gerados: {len(chunks)}")

for index, chunk in enumerate(chunks):
    print("\n" + "=" * 60)
    print(f"CHUNK {index + 1}")
    print("=" * 60)
    print(chunk.page_content)
    print("\nMETADATA:")
    print(chunk.metadata)