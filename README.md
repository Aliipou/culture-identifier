<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&amp;logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

# Cultural Personality Analyzer

**Match your writing style to French cultural figures using NLP and semantic similarity.**

</div>

## What It Does

You write a few sentences. The system analyzes your writing style, vocabulary choices, and rhetorical patterns, then matches you with a French cultural figure — philosopher, writer, or artist — whose documented style is most similar to yours.

## How It Works

Each cultural figure in the database has a style embedding computed from their works. When you submit text, the system embeds it using the same model and finds the nearest neighbors by cosine similarity.

The match is not based on topic or content — it is purely about style. A short text about cooking can match Sartre if the syntax and vocabulary patterns align.

## Cultural Figures Included

Philosophers: Sartre, Camus, Beauvoir, Voltaire, Descartes, Pascal

Writers: Flaubert, Proust, Zola, Hugo, Baudelaire, Rimbaud

Artists: descriptions of artistic philosophy from Monet, Picasso, Duchamp

## Quick Start

```bash
git clone https://github.com/Aliipou/culture-identifier.git
cd culture-identifier
pip install -r requirements.txt
python app.py
# Open http://localhost:5000
```

## License

MIT
