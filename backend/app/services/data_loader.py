"""Data loader for cultural figures dataset."""
import json
from typing import List, Dict, Any
from loguru import logger
from pathlib import Path


class DataLoader:
    """Loader for cultural figures dataset."""

    @staticmethod
    def load_dataset(dataset_path: str) -> List[Dict[str, Any]]:
        """Load the cultural figures dataset.

        Args:
            dataset_path: Path to the dataset JSON file

        Returns:
            List of cultural figure records
        """
        path = Path(dataset_path)
        if not path.exists():
            raise FileNotFoundError(f"Dataset not found: {dataset_path}")

        logger.info(f"Loading dataset from {dataset_path}")
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        logger.info(f"Loaded {len(data)} cultural figures")
        return data

    @staticmethod
    def prepare_for_indexing(data: List[Dict[str, Any]]) -> tuple[List[str], List[Dict[str, Any]]]:
        """Prepare dataset for embedding and indexing.

        Args:
            data: List of cultural figure records

        Returns:
            Tuple of (texts for embedding, metadata)
        """
        texts = []
        metadata = []

        for figure in data:
            # Combine all texts for this figure into one representative corpus
            combined_text = " ".join(figure.get('texts', []))

            # Extract metadata (everything except texts)
            meta = {
                'name': figure['name'],
                'category': figure['category'],
                'period': figure['period'],
                'themes': figure.get('themes', []),
                'writing_style': figure.get('writing_style', ''),
                'recommendation': figure.get('recommendation', {})
            }

            texts.append(combined_text)
            metadata.append(meta)

        logger.info(f"Prepared {len(texts)} texts for indexing")
        return texts, metadata

    @staticmethod
    def validate_dataset(data: List[Dict[str, Any]]) -> bool:
        """Validate dataset structure.

        Args:
            data: List of cultural figure records

        Returns:
            True if valid, raises exception otherwise
        """
        required_fields = ['name', 'category', 'period', 'texts']

        for i, figure in enumerate(data):
            for field in required_fields:
                if field not in figure:
                    raise ValueError(f"Record {i} missing required field: {field}")

            if not isinstance(figure['texts'], list) or len(figure['texts']) == 0:
                raise ValueError(f"Record {i} has invalid 'texts' field")

        logger.info(f"Dataset validation successful: {len(data)} records")
        return True
