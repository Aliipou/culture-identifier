<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&amp;color=gradient&amp;customColorList=3,9,15&amp;height=200&amp;section=header&amp;text=Cultural%20Personality%20Analyzer&amp;fontSize=36&amp;fontColor=fff&amp;animation=twinkling&amp;fontAlignY=38&amp;desc=Which%20French%20thinker%20writes%20like%20you%3F&amp;descAlignY=55&amp;descSize=18" />

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&amp;logo=python&amp;logoColor=white)](https://python.org)
[![Transformers](https://img.shields.io/badge/Transformers-4.x-FFD21E?style=flat&amp;logo=huggingface&amp;logoColor=black)](https://huggingface.co/transformers)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=flat&amp;logo=flask)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

**Match your writing style to iconic French philosophers, writers, and artists.**

*Not about what you say — about how you say it.*

</div>

---

## The Idea

Every writer has a signature. The rhythm of their sentences, the density of their vocabulary, the way they build an argument or paint an image. These stylistic fingerprints persist across topics — Camus writes about football differently than Flaubert, even when both are being concise.

This system encodes those fingerprints as dense semantic vectors and finds whose voice yours most resembles.

---

## How It Works

```
Your text
    |
    v
[Sentence Embedder]      Encodes your text into a 768-dim semantic vector
    |                    using a fine-tuned multilingual sentence-transformer
    v
[Style Profiles]         Pre-computed embeddings of each cultural figure's
    |                    representative works (essays, letters, excerpts)
    v
[Cosine Similarity]      Ranks all figures by similarity to your text
    |
    v
[Explanation Engine]     Highlights the specific stylistic features
                         that drove the match (sentence length, lexical
                         density, rhetorical patterns, emotional register)
```

---

## Cultural Figures

<table>
<tr><th>Philosophers</th><th>Writers</th><th>Artists</th></tr>
<tr>
<td>

- Jean-Paul Sartre
- Albert Camus
- Simone de Beauvoir
- Voltaire
- René Descartes
- Blaise Pascal

</td>
<td>

- Gustave Flaubert
- Marcel Proust
- Émile Zola
- Victor Hugo
- Charles Baudelaire
- Arthur Rimbaud

</td>
<td>

- Claude Monet
- Pablo Picasso
- Marcel Duchamp

*(artistic philosophy)*

</td>
</tr>
</table>

---

## Quick Start

```bash
git clone https://github.com/Aliipou/culture-identifier.git
cd culture-identifier
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000` in your browser.

---

## Example

```
Input: "The absurdity of existence does not negate our freedom to choose.
        On the contrary, it is precisely because nothing is predetermined
        that every choice carries its full weight."

Top Match: Albert Camus (0.91)
Reason:    Existential framing, short declarative sentences, use of
           paradox to reveal rather than obscure, direct address
           of the reader.

Runner-up: Jean-Paul Sartre (0.84)
Runner-up: Simone de Beauvoir (0.79)
```

---

## Project Structure

```
culture-identifier/
├── app.py                  Flask application and routes
├── analyzer/
│   ├── embedder.py         Sentence-transformer wrapper
│   ├── profiles.py         Pre-computed cultural figure embeddings
│   ├── similarity.py       Cosine similarity and ranking
│   └── explainer.py        Feature extraction for match explanation
├── data/
│   └── figures/            Source texts for each cultural figure
├── static/                 CSS, JS, images
├── templates/              HTML templates
├── tests/
│   ├── test_embedder.py
│   ├── test_similarity.py
│   └── test_explainer.py
└── requirements.txt
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python, Flask |
| NLP | `sentence-transformers` (multilingual-MiniLM-L12-v2) |
| Similarity | Cosine similarity via `scikit-learn` |
| Frontend | Vanilla JS, CSS animations |
| Model | Runs locally, no API key needed |

---

## Extending It

**Adding a new figure**
1. Add source texts to `data/figures/your_figure.txt`
2. Run `python scripts/build_profiles.py` to recompute embeddings
3. Add metadata to `analyzer/profiles.py`

**Changing the model**
The embedder is swappable. Any `sentence-transformers` compatible model works. Multilingual models handle French source texts better.

---

## License

MIT

---

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&amp;color=gradient&amp;customColorList=3,9,15&amp;height=80&amp;section=footer" />
</div>
