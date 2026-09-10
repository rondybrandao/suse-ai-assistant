from app.rag.loader import load_documents
from app.rag.chunker import split_documents
from app.rag.embeddings import generate_embeddings

documents = load_documents()

chunks = split_documents(documents)

texts = [
    chunk.page_content
    for chunk in chunks
]

embeddings = generate_embeddings(texts)

print(f"Quantidade de chunks: {len(chunks)}")
print(f"Quantidade de Embeddings: {len(embeddings)}")
print(f"Dimensão do embedding: {len(embeddings[0])}")
print(f"Primeiros valores: {embeddings[0][:5]}")