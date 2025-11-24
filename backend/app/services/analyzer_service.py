"""Cultural personality analyzer service."""
import numpy as np
from typing import List, Dict, Any, Tuple
from sklearn.decomposition import PCA
from loguru import logger
import re
from collections import Counter

from .embedding_service import EmbeddingService
from .vector_store import VectorStore


class CulturalAnalyzer:
    """Main analyzer for matching user text to cultural figures."""

    def __init__(self, embedding_service: EmbeddingService, vector_store: VectorStore):
        """Initialize the analyzer.

        Args:
            embedding_service: Service for generating embeddings
            vector_store: Vector store for similarity search
        """
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.pca = None
        self._fit_pca()

    def _fit_pca(self):
        """Fit PCA for 2D projection visualization."""
        if self.vector_store.size() > 0:
            embeddings = self.vector_store.get_all_embeddings()
            self.pca = PCA(n_components=2, random_state=42)
            self.pca.fit(embeddings)
            logger.info("PCA fitted for 2D projection")

    def _extract_themes(self, text: str) -> List[str]:
        """Extract thematic keywords from text.

        Args:
            text: Input text

        Returns:
            List of theme keywords
        """
        # Common philosophical/literary theme words
        theme_keywords = {
            'existential': ['existence', 'being', 'mortality', 'death', 'life', 'meaning', 'absurd'],
            'political': ['power', 'society', 'justice', 'freedom', 'oppression', 'revolution', 'state'],
            'romantic': ['love', 'passion', 'desire', 'beauty', 'emotion', 'heart', 'soul'],
            'rational': ['reason', 'logic', 'mind', 'thought', 'intellect', 'rational', 'analysis'],
            'spiritual': ['god', 'divine', 'soul', 'faith', 'religious', 'spiritual', 'transcendent'],
            'nature': ['nature', 'natural', 'world', 'earth', 'organic', 'wild', 'landscape'],
            'human_condition': ['suffering', 'joy', 'pain', 'happiness', 'consciousness', 'identity'],
            'artistic': ['art', 'beauty', 'aesthetic', 'creative', 'imagination', 'expression'],
            'social': ['community', 'relationship', 'other', 'society', 'collective', 'individual'],
            'language': ['language', 'words', 'writing', 'discourse', 'communication', 'text']
        }

        text_lower = text.lower()
        found_themes = []

        for theme, keywords in theme_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                found_themes.append(theme)

        return found_themes[:5]  # Return top 5 themes

    def _generate_explanation(
        self,
        user_text: str,
        match_metadata: Dict[str, Any],
        score: float,
        user_features: Dict[str, Any]
    ) -> str:
        """Generate explanation for why a match was made.

        Args:
            user_text: User's input text
            match_metadata: Metadata of matched figure
            score: Similarity score
            user_features: Extracted features from user text

        Returns:
            Explanation string
        """
        explanations = []

        # Score-based confidence
        if score > 0.75:
            confidence = "strong"
        elif score > 0.60:
            confidence = "moderate"
        else:
            confidence = "possible"

        # Theme overlap
        user_themes = self._extract_themes(user_text)
        figure_themes = match_metadata.get('themes', [])
        common_themes = set(user_themes) & set(figure_themes)

        if common_themes:
            theme_str = ', '.join(common_themes)
            explanations.append(f"Your writing explores {theme_str} themes similar to {match_metadata['name']}")

        # Writing style analysis
        if user_features.get('avg_sentence_length', 0) > 20:
            if 'writing_style' in match_metadata and 'complex' in match_metadata['writing_style']:
                explanations.append("Your complex sentence structure mirrors their philosophical depth")

        if user_features.get('question_density', 0) > 0.2:
            if match_metadata.get('category') == 'philosopher':
                explanations.append("Your questioning nature reflects their philosophical inquiry")

        # Default explanation if none generated
        if not explanations:
            explanations.append(
                f"The semantic patterns in your text show {confidence} alignment "
                f"with {match_metadata['name']}'s characteristic expression"
            )

        return ". ".join(explanations) + "."

    def analyze(
        self,
        text: str,
        top_k: int = 3,
        mode: str = "detailed"
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, float]], Dict[str, Any]]:
        """Analyze user text and find matching cultural figures.

        Args:
            text: User input text
            top_k: Number of top matches to return
            mode: Analysis mode ('detailed' or 'quick')

        Returns:
            Tuple of (matches, projection_data, user_embedding_summary)
        """
        logger.info(f"Analyzing text of length {len(text)} in {mode} mode")

        # Generate embedding and extract features
        user_embedding, user_features = self.embedding_service.encode_single(text)

        # Search for similar figures
        scores, metadata_list = self.vector_store.search(user_embedding, top_k=top_k)

        # Build matches with explanations
        matches = []
        for score, metadata in zip(scores, metadata_list):
            if mode == "detailed":
                explanation = self._generate_explanation(text, metadata, score, user_features)
            else:
                explanation = f"Your text shows semantic similarity to {metadata['name']}'s work (score: {score:.2f})."

            match = {
                "name": metadata['name'],
                "score": float(score),
                "reason": explanation,
                "category": metadata['category'],
                "period": metadata['period'],
                "key_themes": metadata.get('themes', [])[:3],
                "recommendation": metadata.get('recommendation', {})
            }
            matches.append(match)

        # Generate 2D projection
        projection_data = self._generate_projection(user_embedding)

        # User embedding summary
        user_summary = {
            "features": user_features,
            "themes": self._extract_themes(text),
            "embedding_norm": float(np.linalg.norm(user_embedding))
        }

        logger.info(f"Analysis complete. Found {len(matches)} matches")
        return matches, projection_data, user_summary

    def _generate_projection(self, user_embedding: np.ndarray) -> List[Dict[str, Any]]:
        """Generate 2D projection for visualization.

        Args:
            user_embedding: User's embedding vector

        Returns:
            List of projection points with labels
        """
        if self.pca is None or self.vector_store.size() == 0:
            return []

        # Get all figure embeddings
        figure_embeddings = self.vector_store.get_all_embeddings()
        figure_metadata = self.vector_store.get_all_metadata()

        # Combine with user embedding
        all_embeddings = np.vstack([figure_embeddings, user_embedding.reshape(1, -1)])

        # Project to 2D
        projections = self.pca.transform(all_embeddings)

        # Build result
        projection_data = []

        # Add figure projections (sample subset for performance)
        sample_size = min(20, len(figure_metadata))
        indices = np.random.choice(len(figure_metadata), sample_size, replace=False)

        for idx in indices:
            projection_data.append({
                "x": float(projections[idx][0]),
                "y": float(projections[idx][1]),
                "label": figure_metadata[idx]['name']
            })

        # Add user projection
        projection_data.append({
            "x": float(projections[-1][0]),
            "y": float(projections[-1][1]),
            "label": "You"
        })

        return projection_data
