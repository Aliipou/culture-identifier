"""Vector store using FAISS for similarity search."""
import numpy as np
import faiss
from typing import List, Tuple, Dict, Any
from loguru import logger
import json
import os


class VectorStore:
    """FAISS-based vector store for similarity search."""

    def __init__(self, embedding_dim: int):
        """Initialize the vector store.

        Args:
            embedding_dim: Dimension of embeddings
        """
        self.embedding_dim = embedding_dim
        self.index = None
        self.metadata: List[Dict[str, Any]] = []
        self.embeddings: np.ndarray = None
        self._initialize_index()

    def _initialize_index(self):
        """Initialize FAISS index with optimal settings."""
        # Use IndexFlatIP for cosine similarity (with normalized vectors)
        # This gives exact results, which is fine for our dataset size
        self.index = faiss.IndexFlatIP(self.embedding_dim)
        logger.info(f"Initialized FAISS index with dimension {self.embedding_dim}")

    def add_vectors(self, embeddings: np.ndarray, metadata: List[Dict[str, Any]]):
        """Add vectors to the index.

        Args:
            embeddings: Array of embeddings (N x D)
            metadata: List of metadata dicts for each embedding
        """
        if embeddings.shape[1] != self.embedding_dim:
            raise ValueError(f"Embedding dimension mismatch: expected {self.embedding_dim}, got {embeddings.shape[1]}")

        if len(metadata) != embeddings.shape[0]:
            raise ValueError("Number of metadata entries must match number of embeddings")

        # Ensure embeddings are normalized for cosine similarity
        faiss.normalize_L2(embeddings)

        # Add to index
        self.index.add(embeddings.astype('float32'))
        self.metadata.extend(metadata)

        # Store embeddings for projection
        if self.embeddings is None:
            self.embeddings = embeddings
        else:
            self.embeddings = np.vstack([self.embeddings, embeddings])

        logger.info(f"Added {len(metadata)} vectors to index. Total: {self.index.ntotal}")

    def search(self, query_embedding: np.ndarray, top_k: int = 3) -> Tuple[List[float], List[Dict[str, Any]]]:
        """Search for similar vectors.

        Args:
            query_embedding: Query embedding vector (D,)
            top_k: Number of results to return

        Returns:
            Tuple of (scores, metadata)
        """
        if self.index.ntotal == 0:
            logger.warning("Index is empty")
            return [], []

        # Ensure query is normalized
        query = query_embedding.reshape(1, -1).astype('float32')
        faiss.normalize_L2(query)

        # Search
        top_k = min(top_k, self.index.ntotal)
        scores, indices = self.index.search(query, top_k)

        # Get metadata for results
        results_metadata = [self.metadata[idx] for idx in indices[0]]
        results_scores = scores[0].tolist()

        return results_scores, results_metadata

    def get_all_embeddings(self) -> np.ndarray:
        """Get all stored embeddings.

        Returns:
            Array of all embeddings
        """
        return self.embeddings

    def get_all_metadata(self) -> List[Dict[str, Any]]:
        """Get all stored metadata.

        Returns:
            List of all metadata
        """
        return self.metadata

    def save(self, index_path: str, metadata_path: str):
        """Save index and metadata to disk.

        Args:
            index_path: Path to save FAISS index
            metadata_path: Path to save metadata JSON
        """
        faiss.write_index(self.index, index_path)
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)
        logger.info(f"Saved index to {index_path} and metadata to {metadata_path}")

    def load(self, index_path: str, metadata_path: str):
        """Load index and metadata from disk.

        Args:
            index_path: Path to FAISS index
            metadata_path: Path to metadata JSON
        """
        if not os.path.exists(index_path) or not os.path.exists(metadata_path):
            raise FileNotFoundError("Index or metadata file not found")

        self.index = faiss.read_index(index_path)
        with open(metadata_path, 'r', encoding='utf-8') as f:
            self.metadata = json.load(f)

        logger.info(f"Loaded index with {self.index.ntotal} vectors")

    def size(self) -> int:
        """Get the number of vectors in the index.

        Returns:
            Number of vectors
        """
        return self.index.ntotal if self.index else 0
