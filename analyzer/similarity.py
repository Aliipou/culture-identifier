"""Cosine similarity ranking for cultural figure matching."""
from __future__ import annotations
import numpy as np
from dataclasses import dataclass


@dataclass
class Match:
    """A ranked match between user text and a cultural figure."""
    figure: str
    score: float        # Cosine similarity in [0, 1]
    category: str       # "philosopher", "writer", "artist"
    period: str         # e.g., "20th century"
    description: str    # One-line bio


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity between two L2-normalized vectors.

    Since both vectors are pre-normalized, this reduces to a dot product.
    """
    return float(np.dot(a, b))


def rank_matches(
    query_embedding: np.ndarray,
    profiles: dict[str, dict],
    top_k: int = 3,
) -> list[Match]:
    """Rank all cultural figures by similarity to the query embedding.

    Args:
        query_embedding: L2-normalized embedding of user input text.
        profiles: Dict mapping figure name to profile dict containing
                  "embedding", "category", "period", "description".
        top_k: Number of top matches to return.

    Returns:
        List of Match objects sorted by score descending.
    """
    matches = []
    for name, profile in profiles.items():
        score = cosine_similarity(query_embedding, profile["embedding"])
        matches.append(Match(
            figure=name,
            score=score,
            category=profile["category"],
            period=profile["period"],
            description=profile["description"],
        ))
    matches.sort(key=lambda m: m.score, reverse=True)
    return matches[:top_k]
