"""Tests for vector store."""
import pytest
import numpy as np
from backend.app.services.vector_store import VectorStore


@pytest.fixture
def vector_store():
    """Create vector store for testing."""
    return VectorStore(embedding_dim=384)


@pytest.fixture
def sample_embeddings():
    """Create sample embeddings."""
    return np.random.randn(10, 384).astype('float32')


@pytest.fixture
def sample_metadata():
    """Create sample metadata."""
    return [
        {"name": f"Figure {i}", "category": "writer"}
        for i in range(10)
    ]


def test_vector_store_initialization(vector_store):
    """Test vector store initialization."""
    assert vector_store.embedding_dim == 384
    assert vector_store.index is not None
    assert vector_store.size() == 0


def test_add_vectors(vector_store, sample_embeddings, sample_metadata):
    """Test adding vectors to store."""
    vector_store.add_vectors(sample_embeddings, sample_metadata)

    assert vector_store.size() == 10


def test_add_vectors_dimension_mismatch(vector_store, sample_metadata):
    """Test that wrong dimension raises error."""
    wrong_embeddings = np.random.randn(10, 512).astype('float32')

    with pytest.raises(ValueError):
        vector_store.add_vectors(wrong_embeddings, sample_metadata)


def test_add_vectors_metadata_mismatch(vector_store, sample_embeddings):
    """Test that metadata length mismatch raises error."""
    wrong_metadata = [{"name": "Test"}]  # Only 1 instead of 10

    with pytest.raises(ValueError):
        vector_store.add_vectors(sample_embeddings, wrong_metadata)


def test_search(vector_store, sample_embeddings, sample_metadata):
    """Test similarity search."""
    vector_store.add_vectors(sample_embeddings, sample_metadata)

    # Search with first embedding
    query = sample_embeddings[0]
    scores, metadata = vector_store.search(query, top_k=3)

    assert len(scores) == 3
    assert len(metadata) == 3
    assert scores[0] >= scores[1] >= scores[2]  # Scores should be descending


def test_search_empty_index():
    """Test search on empty index."""
    empty_store = VectorStore(embedding_dim=384)
    query = np.random.randn(384).astype('float32')

    scores, metadata = empty_store.search(query, top_k=3)

    assert len(scores) == 0
    assert len(metadata) == 0


def test_get_all_embeddings(vector_store, sample_embeddings, sample_metadata):
    """Test retrieving all embeddings."""
    vector_store.add_vectors(sample_embeddings, sample_metadata)

    all_embeddings = vector_store.get_all_embeddings()

    assert all_embeddings.shape == sample_embeddings.shape


def test_get_all_metadata(vector_store, sample_embeddings, sample_metadata):
    """Test retrieving all metadata."""
    vector_store.add_vectors(sample_embeddings, sample_metadata)

    all_metadata = vector_store.get_all_metadata()

    assert len(all_metadata) == len(sample_metadata)
