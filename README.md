# Cultural Personality Analyzer

Match your writing style and intellectual voice to iconic French philosophers, writers, and artists — using sentence embeddings and cosine similarity, no API key required.

---

## 1. Problem

Most personality tools map you to archetypes or trait dimensions. This system asks a different question: **whose intellectual lineage does your writing reflect?**

Given a text sample, it identifies which French cultural figures — Sartre, Camus, Flaubert, Baudelaire, and others — your writing most resembles. The match is driven not by topic overlap but by stylistic and semantic fingerprints: sentence rhythm, argumentative structure, lexical density, rhetorical register, and thematic preoccupations. A short paragraph about everyday frustration can reveal whether you write like an existentialist or a naturalist.

---

## 2. Architecture

```
User text input
      |
      v
[Sentence Embedder]
  paraphrase-multilingual-mpnet-base-v2
  Encodes input into a 768-dim semantic vector
      |
      v
[FAISS Vector Store]
  Pre-indexed embeddings of cultural figures'
  representative texts (essays, letters, excerpts)
      |
      v
[Cosine Similarity Search]
  Ranks all indexed figures by distance to user vector
      |
      v
[CulturalAnalyzer]
  Extracts thematic keywords, generates 2D PCA projection
  for visualization, builds match explanation
      |
      v
[FastAPI Response]
  Ranked matches + similarity scores + style summary
```

The backend is fully stateless per request. All embeddings are computed once at startup and held in memory via FAISS; query time is sub-100ms after the model loads.

---

## 3. Design Decisions

**Why `sentence-transformers`?**
Sentence-level embeddings capture semantic and stylistic intent better than token-level models for this task. `paraphrase-multilingual-mpnet-base-v2` handles both English and French source texts, which matters because the reference corpus includes original French works.

**Why these cultural figures?**
The reference set covers distinct intellectual styles: Sartre's dense phenomenology, Camus's lucid prose, Proust's exhaustive introspection, Baudelaire's lyrical intensity, Flaubert's clinical realism. They were chosen to maximize differentiation in embedding space, not for encyclopedic coverage.

**FastAPI over Flask**
The initial prototype was Flask (reflected in legacy README badges). The production backend uses FastAPI for async request handling, automatic OpenAPI docs at `/docs`, and Pydantic model validation. The CPU-bound embedding inference runs synchronously inside async endpoints — acceptable given model warm-up at startup.

**FAISS over brute-force numpy**
Even with a small reference corpus (~20 figures), FAISS gives a consistent interface if the corpus grows. Index build time at startup is negligible.

---

## 4. Tech Stack

| Component      | Technology                                      |
|----------------|-------------------------------------------------|
| Backend        | Python 3.12, FastAPI, Uvicorn                   |
| NLP Model      | `sentence-transformers` (multilingual-mpnet)    |
| Vector Search  | FAISS                                           |
| Similarity     | Cosine similarity + PCA projection              |
| Validation     | Pydantic v2                                     |
| Logging        | Loguru                                          |
| Frontend       | Vanilla JS, Nginx (served separately)           |
| Container      | Docker multi-stage, non-root user               |

---

## 5. Running Locally

**Without Docker**
```bash
git clone https://github.com/Aliipou/culture-identifier.git
cd culture-identifier
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

API available at `http://localhost:8000` — interactive docs at `http://localhost:8000/docs`.

**With Docker Compose**
```bash
docker compose up --build
```

Backend on port `8000`, frontend (Nginx) on port `3000`.

---

## 6. API Example

Analyze a text sample:
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "The absurdity of existence does not negate our freedom to choose. On the contrary, it is precisely because nothing is predetermined that every choice carries its full weight.",
    "top_k": 3,
    "mode": "standard"
  }'
```

Example response:
```json
{
  "matches": [
    {
      "name": "Albert Camus",
      "similarity": 0.91,
      "themes": ["existential", "rational"],
      "style_summary": "Existential framing, short declarative sentences, use of paradox"
    },
    {
      "name": "Jean-Paul Sartre",
      "similarity": 0.84,
      "themes": ["existential", "political"]
    }
  ],
  "projection": [...],
  "processing_time_ms": 42.3
}
```

Health check:
```bash
curl http://localhost:8000/health
# {"status": "ok"}
```

---

## 7. Limitations

- **Language bias**: The embedding model handles multilingual input but was trained primarily on English and major European languages. Short or highly idiomatic texts in less-represented languages will produce less reliable matches.
- **Small reference corpus**: ~20 cultural figures is enough to show the concept but not enough for confident disambiguation. Figures with similar styles (e.g., Sartre and de Beauvoir) will produce close similarity scores.
- **No stylometric features**: Matches are purely embedding-based. Classic stylometric signals — sentence length distribution, function word frequencies, punctuation patterns — are not explicitly modeled; they influence the embedding only implicitly.
- **French-intellectual scope**: The corpus covers 19th–20th century French philosophy and literature. Writers from other traditions will find their closest match within this set, which may not be meaningful.
- **Cold start**: The model (~400MB) and FAISS index load at startup. First boot takes 30–60 seconds depending on hardware.

---

## License

MIT
