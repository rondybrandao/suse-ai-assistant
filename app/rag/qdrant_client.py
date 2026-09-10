from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, 
    VectorParams,
    PointStruct,
)

from app.config import settings

# Cria conexao
client = QdrantClient(
    host=settings.qdrant_host,
    port=settings.qdrant_port,
)

def test_connection():
    collections = client.get_collections()

    return collections

def create_collection():
    collections = client.get_collections()

    collection_names = [
        collection.name
        for collection in collections.collections
    ]

    if settings.qdrant_collection not in collection_names:
        client.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )

        print(
            f"Collection '{settings.qdrant_collection}' criada."
        )

    else:
        print(
            f"Collection '{settings.qdrant_collection}' já existe."
        )


def insert_embeddings(chunks, embeddings):
    points = []

    for index, (chunk, embedding) in enumerate(
        zip(chunks, embeddings)
    ):
        point = PointStruct(
            id=index,
            vector=embedding.tolist(),
            payload={
                "text": chunk.page_content,
                "metadata": chunk.metadata,
            },
        )

        points.append(point)

    client.upsert(
        collection_name=settings.qdrant_collection,
        points=points,
    )

    return len(points)

# Buscar chunks mais relevantes
def search_similar(query_embedding, limit=5):
    results = client.query_points(
        collection_name=settings.qdrant_collection,
        query=query_embedding.tolist(),
        limit=limit,
        with_payload=True,
    )

    return results.points