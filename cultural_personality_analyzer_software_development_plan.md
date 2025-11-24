# Cultural Personality Analyzer — Software Development Plan

## 1. Concept Summary
A system that uses NLP to analyze user text (or short question responses) and identifies which French philosopher, writer, or artist the user's personality/thinking resembles. Not a superficial quiz — a semi-scientific analysis based on embeddings and modern NLP, with an interactive cultural mapping output.

---

## 2. Goals & Success Indicators
- Core goal: produce meaningful, convincing cultural-personality matches.
- Quality indicators: clarity of explanation, user perception of match accuracy, qualitative feedback from test groups.
- Constraints: avoid deterministic claims; emphasize uncertainty and model limitations.

---

## 3. MVP
**Inputs:** free-form text (150–500 words recommended) or five short-answer prompts.

**Outputs:**
- Top 1–3 suggested cultural matches (French writers/philosophers/artists).
- Short explanation (2–4 sentences) focusing on linguistic/semantic cues.
- Recommended book/film from the matched figure.
- Simple interactive visualization: the user’s embedding projected on a 2D map.

**Tech components:**
- Sentence embeddings
- Nearest-neighbor similarity search
- Lightweight frontend for input + results display

---

## 4. System Architecture
1. **Frontend:** React (or Streamlit for rapid prototyping)
2. **Backend API:** FastAPI
3. **Model Serving:** Sentence-transformer embeddings using multilingual or French-specific models (e.g., CamemBERT-SBERT)
4. **Vector Database:** FAISS / Milvus / Pinecone
5. **Relational Database:** PostgreSQL for metadata and logs
6. **Storage:** S3-like object storage for texts/media
7. **Monitoring:** Grafana/Prometheus + Sentry
8. **Deployment:** Docker + Kubernetes or managed container services

---

## 5. Data Curation
**Sources:** novels, essays, interviews, critical analyses.

**Reference Dataset:**
- 50–150 French cultural figures
- For each figure: 3–10 representative texts
- Each document includes metadata and thematic tags

**Preprocessing:**
- Text normalization, deduplication, tokenization
- Feature extraction (readability, sentiment, thematic signals, sentence length distribution)

**Human Annotation:**
- Annotators validate match quality and help build evaluation sets.

---

## 6. Modeling & Matching Logic
1. **Embedding Extraction:** sentence-transformers (e.g., paraphrase-multilingual-mpnet-base-v2 or CamemBERT variants).
2. **Similarity Search:** cosine similarity for top‑K retrieval.
3. **Explainability Layer:**
   - Highlight overlapping themes, recurring keywords, stylistic similarities.
   - Provide short justifications referencing semantic clusters.
4. **Rule-Based Layer:** prioritize relevant categories (e.g., philosophy vs literature) based on user text.
5. **Calibration:** fallback responses when similarity scores fall below threshold.

---

## 7. Product & UX Rules
- Be transparent about uncertainty.
- Allow users to rate the accuracy of matches.
- Provide an interpretability panel showing why a match was selected.
- Avoid cultural/political/ideological stereotyping.

---

## 8. Evaluation
**Quantitative:** precision@K using human-validated comparisons.

**Qualitative:** user testing with French literature/culture enthusiasts.

**A/B Testing:** compare different explanation styles.

---

## 9. Privacy & Ethics
- User text is sensitive; do not store without consent.
- If stored, anonymize and allow full deletion.
- Document model limitations and possible biases.

---

## 10. Technology Stack
- **Language:** Python 3.10+
- **Backend:** FastAPI
- **ML:** Hugging Face Transformers, sentence-transformers
- **Vector DB:** FAISS / Milvus / Pinecone
- **DB:** PostgreSQL
- **Frontend:** React + Tailwind (or Streamlit prototype)
- **Deployment:** Docker, Kubernetes
- **CI/CD:** GitHub Actions

---

## 11. Risks & Weaknesses
- Weakness of reference corpus: low-quality or insufficient texts = meaningless matches.
- Curator bias: narrow cultural representation.
- Explainability difficulty: embedding-based logic is opaque.
- Privacy concerns: users may not trust text storage.

---

## 12. Practical Checklist
1. Build initial list of 50–150 French cultural figures.
2. Collect representative texts.
3. Design metadata schema.
4. Test two embedding models (multilingual vs French-specific).
5. Implement embedding pipeline + FAISS indexing.
6. Implement `/analyze` endpoint.
7. Build basic frontend UI.
8. Conduct annotation and human evaluation.
9. Implement user feedback collection.
10. Improve explainability layer.
11. Draft privacy policy and user consent flow.

---

## 13. Team Roles
- **Product Owner:** prioritization and feature definition
- **ML Engineer:** model development
- **Backend Engineer:** API & infrastructure
- **Frontend Engineer:** UI/UX
- **Annotators:** human evaluation

---

## 14. Example API
```
POST /analyze
Body: { "text": "...", "mode": "detailed" }
Response: {
  "matches": [
    { "name": "Valeria Luiselli", "score": 0.87, "reason": "..." }
  ],
  "projection": { ... },
  "suggestion": { "book": "The Story of My Teeth" }
}
```

---

## 15. Future Extensions
- Image-based personality cues (cross-modal embeddings)
- Long-term personalization
- Expansion to other cultures/languages (Italian, Spanish, etc.)

---

## 16. Final Hard Truths
- If you don’t invest heavily in building a high-quality reference corpus, the product becomes shallow.
- If explanation quality is weak, users won’t trust the matches.

