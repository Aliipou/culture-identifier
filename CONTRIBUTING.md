# Contributing to culture-identifier

## Setup

```bash
git clone https://github.com/Aliipou/culture-identifier.git
cd culture-identifier
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Running Tests

```bash
make test
```

## Adding a New Cultural Figure

1. Create `data/figures/figure_name.txt` with representative excerpts (500-2000 words total)
2. Run `python scripts/build_profiles.py` to generate the embedding
3. Add metadata to `analyzer/profiles.py`:
   ```python
   "Figure Name": {
       "embedding": load_embedding("figure_name"),
       "category": "philosopher",  # or "writer", "artist"
       "period": "20th century",
       "description": "One-line description"
   }
   ```
4. Add test cases in `tests/test_similarity.py`

## Source Text Guidelines

- Use published, public domain works where possible
- Minimum 500 words of source text per figure for reliable embeddings
- French originals are preferred — the model is multilingual
- Document the source in a comment in the data file

## Code Style

- Python 3.9+, type hints on all public functions
- `ruff` for linting, `black` for formatting
- Docstrings on all public classes and functions

## Commit Messages

`feat:`, `fix:`, `docs:`, `test:`, `chore:`
