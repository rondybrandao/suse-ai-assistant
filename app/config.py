from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "SUSE AI Assistant"
    app_env: str = "development"

    qdrant_host: str = "localhost"
    qdrant_port: int = 6333

    qdrant_collection: str = "suse_documents"

    embedding_model: str = (
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    gemini_api_key: str

    class Config:
        env_file = ".env"


settings = Settings()