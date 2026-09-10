from sentence_transformers import SentenceTransformer

from app.config import settings


# Carrega o modelo do embedding
model = SentenceTransformer(
    settings.embedding_model
)

# transforma texto em vetores
def generate_embeddings(texts):
    return model.encode(
        texts,
        convert_to_numpy=True
    )