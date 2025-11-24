"""Tests for embedding service."""
import pytest
import numpy as np
from backend.app.services.embedding_service import EmbeddingService


@pytest.fixture
def embedding_service():
    """Create embedding service for testing."""
    return EmbeddingService()


def test_embedding_service_initialization(embedding_service):
    """Test that embedding service initializes correctly."""
    assert embedding_service.model is not None
    assert embedding_service.embedding_dim > 0


def test_preprocess_text(embedding_service):
    """Test text preprocessing."""
    text = "This   is  a    test   with   extra     spaces!"
    processed = embedding_service.preprocess_text(text)

    assert "  " not in processed
    assert processed.strip() == processed


def test_extract_features(embedding_service):
    """Test feature extraction."""
    text = "This is a test. How are you? This is another sentence."
    features = embedding_service.extract_features(text)

    assert "sentence_count" in features
    assert "word_count" in features
    assert "avg_sentence_length" in features
    assert features["sentence_count"] == 3
    assert features["word_count"] > 0


def test_encode_single_text(embedding_service):
    """Test encoding a single text."""
    text = "This is a test sentence for embedding."
    embedding, features = embedding_service.encode_single(text)

    assert isinstance(embedding, np.ndarray)
    assert len(embedding) == embedding_service.embedding_dim
    assert isinstance(features, dict)


def test_encode_multiple_texts(embedding_service):
    """Test encoding multiple texts."""
    texts = [
        "First test sentence.",
        "Second test sentence.",
        "Third test sentence."
    ]
    embeddings = embedding_service.encode(texts)

    assert embeddings.shape[0] == len(texts)
    assert embeddings.shape[1] == embedding_service.embedding_dim


def test_embedding_normalization(embedding_service):
    """Test that embeddings are normalized."""
    text = "Test sentence for normalization check."
    embedding, _ = embedding_service.encode_single(text)

    norm = np.linalg.norm(embedding)
    assert np.isclose(norm, 1.0, atol=1e-5)


def test_feature_question_density(embedding_service):
    """Test question density feature."""
    text_with_questions = "What is life? Why are we here? These are important questions."
    text_without_questions = "Life is a journey. We are here to learn."

    features_with = embedding_service.extract_features(text_with_questions)
    features_without = embedding_service.extract_features(text_without_questions)

    assert features_with["question_density"] > features_without["question_density"]


def test_feature_complex_words(embedding_service):
    """Test complex word ratio feature."""
    simple_text = "The cat sat on the mat."
    complex_text = "The philosophical contemplation necessitates extraordinary consideration."

    features_simple = embedding_service.extract_features(simple_text)
    features_complex = embedding_service.extract_features(complex_text)

    assert features_complex["complex_word_ratio"] > features_simple["complex_word_ratio"]
