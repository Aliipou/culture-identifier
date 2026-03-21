"""Sentence-transformer wrapper for style embedding."""
from sentence_transformers import SentenceTransformer
import numpy as np

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


class StyleEmbedder:
    """Encodes text into a dense semantic vector for style comparison.

    Uses a multilingual sentence-transformer so it handles both French
    source texts and English input text correctly.
    """

    def __init__(self, model_name: str = MODEL_NAME):
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str) -> np.ndarray:
        """Encode a text string into a normalized embedding vector.

        Args:
            text: Input text of any length. Longer texts are averaged
                  across sentence chunks automatically.

        Returns:
            1-D numpy array of shape (embedding_dim,), L2 normalized.
        """
        embedding = self.model.encode(text, normalize_embeddings=True)
        return embedding

    def embed_batch(self, texts: list[str]) -> np.ndarray:
        """Encode multiple texts in a single forward pass.

        Args:
            texts: List of text strings.

        Returns:
            2-D numpy array of shape (n_texts, embedding_dim).
        """
        return self.model.encode(texts, normalize_embeddings=True, batch_size=32)
