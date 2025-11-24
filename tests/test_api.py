"""Integration tests for API endpoints."""
import pytest
from fastapi.testclient import TestClient
from backend.app.main import create_app
from backend.app.services import EmbeddingService, VectorStore, CulturalAnalyzer
from backend.app.services.data_loader import DataLoader
import numpy as np


@pytest.fixture
def client():
    """Create test client with initialized app."""
    app = create_app()

    # Initialize services with minimal data
    embedding_service = EmbeddingService()
    vector_store = VectorStore(embedding_dim=embedding_service.embedding_dim)

    # Create minimal test dataset
    test_data = [
        {
            "name": "Test Writer",
            "category": "writer",
            "period": "20th century",
            "themes": ["test"],
            "writing_style": "test style",
            "texts": ["This is a test text for embedding."],
            "recommendation": {"book": "Test Book", "type": "novel", "year": "2000"}
        }
    ]

    # Prepare and index
    data_loader = DataLoader()
    texts, metadata = data_loader.prepare_for_indexing(test_data)
    embeddings = embedding_service.encode(texts)
    vector_store.add_vectors(embeddings, metadata)

    # Initialize analyzer
    analyzer = CulturalAnalyzer(embedding_service, vector_store)

    # Store in app state
    app.state.embedding_service = embedding_service
    app.state.vector_store = vector_store
    app.state.analyzer = analyzer

    return TestClient(app)


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True
    assert data["index_size"] > 0


def test_analyze_endpoint_success(client):
    """Test successful analysis."""
    request_data = {
        "text": "This is a test text for analysis. It contains multiple sentences. Each sentence has different words and meanings.",
        "mode": "detailed",
        "top_k": 1
    }

    response = client.post("/api/analyze", json=request_data)
    assert response.status_code == 200

    data = response.json()
    assert "matches" in data
    assert "projection" in data
    assert "processing_time_ms" in data
    assert len(data["matches"]) == 1


def test_analyze_endpoint_text_too_short(client):
    """Test analysis with text that's too short."""
    request_data = {
        "text": "Too short",
        "mode": "detailed",
        "top_k": 3
    }

    response = client.post("/api/analyze", json=request_data)
    assert response.status_code == 422  # Validation error


def test_analyze_endpoint_invalid_mode(client):
    """Test analysis with invalid mode."""
    request_data = {
        "text": "This is a test text for analysis with sufficient length to pass validation.",
        "mode": "invalid_mode",
        "top_k": 3
    }

    response = client.post("/api/analyze", json=request_data)
    assert response.status_code == 422  # Validation error


def test_analyze_endpoint_different_top_k(client):
    """Test analysis with different top_k values."""
    request_data = {
        "text": "This is a comprehensive test text for analysis. It explores various themes and ideas.",
        "mode": "quick",
        "top_k": 1
    }

    response = client.post("/api/analyze", json=request_data)
    assert response.status_code == 200

    data = response.json()
    assert len(data["matches"]) <= 1


def test_analyze_response_structure(client):
    """Test that analysis response has correct structure."""
    request_data = {
        "text": "Philosophical musings about existence and the nature of reality. What does it mean to be?",
        "mode": "detailed",
        "top_k": 1
    }

    response = client.post("/api/analyze", json=request_data)
    assert response.status_code == 200

    data = response.json()

    # Check matches structure
    assert isinstance(data["matches"], list)
    if len(data["matches"]) > 0:
        match = data["matches"][0]
        assert "name" in match
        assert "score" in match
        assert "reason" in match
        assert "category" in match
        assert "period" in match
        assert "key_themes" in match
        assert "recommendation" in match

    # Check projection structure
    assert isinstance(data["projection"], list)

    # Check user summary
    assert "user_embedding_summary" in data
    assert "features" in data["user_embedding_summary"]
