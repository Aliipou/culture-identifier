"""Configuration management."""
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """Application settings."""

    # API Settings
    api_title: str = "Cultural Personality Analyzer API"
    api_version: str = "1.0.0"
    api_description: str = "NLP-based system to match user personality with French cultural figures"

    # Model Settings
    embedding_model: str = "paraphrase-multilingual-mpnet-base-v2"
    similarity_threshold: float = 0.50
    default_top_k: int = 3

    # Data Paths
    dataset_path: str = "../data/cultural_figures/dataset.json"
    index_path: str = "../data/faiss_index.bin"
    metadata_path: str = "../data/metadata.json"

    # CORS
    allow_origins: list = ["*"]  # Allow all origins for development

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
