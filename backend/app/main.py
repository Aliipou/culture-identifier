"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys
from pathlib import Path

from .core import settings
from .api import router
from .services import EmbeddingService, VectorStore, CulturalAnalyzer
from .services.data_loader import DataLoader


# Configure logging
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="INFO"
)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        Configured FastAPI app
    """
    app = FastAPI(
        title=settings.api_title,
        version=settings.api_version,
        description=settings.api_description
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(router, prefix="/api")

    return app


app = create_app()


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("Starting Cultural Personality Analyzer API...")

    try:
        # Initialize embedding service
        logger.info("Loading embedding model...")
        embedding_service = EmbeddingService(model_name=settings.embedding_model)

        # Initialize vector store
        logger.info("Initializing vector store...")
        vector_store = VectorStore(embedding_dim=embedding_service.embedding_dim)

        # Load and index dataset
        logger.info("Loading cultural figures dataset...")
        dataset_path = Path(settings.dataset_path)

        if not dataset_path.exists():
            raise FileNotFoundError(f"Dataset not found at {dataset_path}")

        data_loader = DataLoader()
        data = data_loader.load_dataset(str(dataset_path))
        data_loader.validate_dataset(data)

        # Prepare and index data
        texts, metadata = data_loader.prepare_for_indexing(data)
        logger.info("Generating embeddings for cultural figures...")
        embeddings = embedding_service.encode(texts, show_progress=True)

        logger.info("Building FAISS index...")
        vector_store.add_vectors(embeddings, metadata)

        # Initialize analyzer
        logger.info("Initializing cultural analyzer...")
        analyzer = CulturalAnalyzer(embedding_service, vector_store)

        # Store in app state
        app.state.embedding_service = embedding_service
        app.state.vector_store = vector_store
        app.state.analyzer = analyzer

        logger.info(f"Startup complete! Indexed {vector_store.size()} cultural figures")

    except Exception as e:
        logger.error(f"Startup failed: {str(e)}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down Cultural Personality Analyzer API...")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Cultural Personality Analyzer API",
        "version": settings.api_version,
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
