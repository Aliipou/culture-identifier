"""Tests for similarity ranking module."""
import numpy as np
import pytest
from analyzer.similarity import cosine_similarity, rank_matches, Match


def make_embedding(size: int = 384, seed: int = 0) -> np.ndarray:
    rng = np.random.RandomState(seed)
    v = rng.randn(size).astype(np.float32)
    return v / np.linalg.norm(v)  # L2 normalize


def test_cosine_similarity_identical():
    v = make_embedding()
    assert abs(cosine_similarity(v, v) - 1.0) < 1e-5


def test_cosine_similarity_orthogonal():
    v1 = np.zeros(4, dtype=np.float32)
    v1[0] = 1.0
    v2 = np.zeros(4, dtype=np.float32)
    v2[1] = 1.0
    assert abs(cosine_similarity(v1, v2)) < 1e-5


def test_rank_matches_returns_top_k():
    query = make_embedding(seed=0)
    profiles = {
        "Sartre": {"embedding": make_embedding(seed=1), "category": "philosopher",
                   "period": "20th century", "description": "Existentialist philosopher"},
        "Camus": {"embedding": make_embedding(seed=2), "category": "philosopher",
                  "period": "20th century", "description": "Absurdist writer"},
        "Zola": {"embedding": make_embedding(seed=3), "category": "writer",
                 "period": "19th century", "description": "Naturalist novelist"},
    }
    results = rank_matches(query, profiles, top_k=2)
    assert len(results) == 2
    assert isinstance(results[0], Match)
    assert results[0].score >= results[1].score  # Sorted descending


def test_rank_matches_score_in_range():
    query = make_embedding(seed=42)
    profiles = {
        "Hugo": {"embedding": make_embedding(seed=10), "category": "writer",
                 "period": "19th century", "description": "Romantic novelist"},
    }
    results = rank_matches(query, profiles, top_k=1)
    assert -1.0 <= results[0].score <= 1.0
