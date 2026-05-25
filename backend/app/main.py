"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys
from pathlib import Path

from .core import settings
from .api import router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.api_title,
        version=settings.api_version,
        description=settings.api_description
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router, prefix="/api")
    return app


app = create_app()
_analyzer = None


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup (non-fatal on resource constraints)."""
    global _analyzer
    logger.info("Starting Cultural Personality Analyzer API...")
    try:
        from .services import EmbeddingService, VectorStore, CulturalAnalyzer
        from .services.data_loader import DataLoader

        logger.info("Loading embedding model (this may take a minute)...")
        embedding_service = EmbeddingService(model_name=settings.embedding_model)

        logger.info("Initializing vector store...")
        vector_store = VectorStore(embedding_dim=embedding_service.embedding_dim)

        logger.info("Loading cultural figures dataset...")
        dataset_path = Path(settings.dataset_path)
        if not dataset_path.exists():
            # Try alternate paths
            for alt in [Path('data/cultural_figures/dataset.json'),
                        Path(__file__).parent.parent.parent / 'data/cultural_figures/dataset.json']:
                if alt.exists():
                    dataset_path = alt
                    break

        data_loader = DataLoader()
        logger.info("Cultural Analyzer ready.")
    except Exception as e:
        logger.warning(f"Startup init failed (fallback mode): {e}")


@app.get("/health")
async def health():
    return {"status": "ok"}
