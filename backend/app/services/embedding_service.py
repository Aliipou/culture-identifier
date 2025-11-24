"""Embedding service using sentence-transformers."""
import numpy as np
from typing import List, Tuple, Dict, Any
from sentence_transformers import SentenceTransformer
from loguru import logger
import re


class EmbeddingService:
    """Service for generating text embeddings."""

    def __init__(self, model_name: str = "paraphrase-multilingual-mpnet-base-v2"):
        """Initialize the embedding service.

        Args:
            model_name: Name of the sentence-transformer model to use
        """
        logger.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        logger.info(f"Model loaded successfully. Embedding dimension: {self.embedding_dim}")

    def preprocess_text(self, text: str) -> str:
        """Preprocess text before embedding.

        Args:
            text: Raw input text

        Returns:
            Cleaned and normalized text
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)

        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?;:\'-]', '', text)

        # Normalize quotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")

        return text.strip()

    def extract_features(self, text: str) -> Dict[str, Any]:
        """Extract linguistic features from text.

        Args:
            text: Input text

        Returns:
            Dictionary of extracted features
        """
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        words = text.split()

        # Calculate basic features
        avg_sentence_length = np.mean([len(s.split()) for s in sentences]) if sentences else 0
        avg_word_length = np.mean([len(w) for w in words]) if words else 0

        # Punctuation density
        punctuation_count = len(re.findall(r'[.,!?;:]', text))
        punctuation_density = punctuation_count / len(words) if words else 0

        # Question density (philosophical tendency)
        question_count = text.count('?')
        question_density = question_count / len(sentences) if sentences else 0

        # Complex vocabulary indicators
        long_words = [w for w in words if len(w) > 8]
        complex_word_ratio = len(long_words) / len(words) if words else 0

        return {
            "sentence_count": len(sentences),
            "word_count": len(words),
            "avg_sentence_length": float(avg_sentence_length),
            "avg_word_length": float(avg_word_length),
            "punctuation_density": float(punctuation_density),
            "question_density": float(question_density),
            "complex_word_ratio": float(complex_word_ratio)
        }

    def encode(self, texts: List[str], show_progress: bool = False) -> np.ndarray:
        """Encode texts into embeddings.

        Args:
            texts: List of texts to encode
            show_progress: Whether to show progress bar

        Returns:
            Array of embeddings
        """
        # Preprocess texts
        processed_texts = [self.preprocess_text(text) for text in texts]

        # Generate embeddings
        embeddings = self.model.encode(
            processed_texts,
            show_progress_bar=show_progress,
            convert_to_numpy=True,
            normalize_embeddings=True  # L2 normalization for cosine similarity
        )

        return embeddings

    def encode_single(self, text: str) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Encode a single text and extract features.

        Args:
            text: Input text

        Returns:
            Tuple of (embedding, features)
        """
        embedding = self.encode([text])[0]
        features = self.extract_features(text)

        return embedding, features
