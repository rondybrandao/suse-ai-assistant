from app.rag.loader import load_documents 
from app.rag.chunker import split_documents 
from app.rag.embeddings import generate_embeddings 
from app.rag.qdrant_client import (
    client, 
    create_collection,
    insert_embeddings
)

from app.config import settings

# Carregar documentos

documents = load_documents()

print(f"Quantidade de documentos: {len(documents)}")

# Dividir em Chunks

chunks = split_documents(documents)

print(f"Quantidade de chunks: {len(chunks)}")

# Gerar Embeddings

texts = [
    chunk.page_content
    for chunk in chunks
]

embeddings = generate_embeddings(texts)

print(f"Quantidade de Embeddings: {len(embeddings)}")
print(f"Dimensão do embedding: {embeddings.shape[1]}")

# Testar Conexão com Qdrant

collections = client.get_collections()

print("Conexão com Qdrant Ok")

# Criar collection

create_collection()

# Inserir Embeddings

inserted = insert_embeddings(
    chunks,
    embeddings,
)

print(f"Embeddings inseridos: {inserted}")

# Validar

collection_info = client.get_collection(
    collection_name=settings.qdrant_collection
)

print(
    f"Quantidade de pontos no Qdrant: "
    f"{collection_info.points_count}"
)


#Resultado

if collection_info.points_count == inserted:
    print()
    print("===================================")
    print("Teste Qdrant: OK")
    print("===================================")
else:
    print()
    print("===================================")
    print("Teste Qdrant: Falhou")
    print("===================================")
    print(
        f"Esperado: {inserted} | " 
        f"Encontrado: {collection_info.points_count}" 
    )