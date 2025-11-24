# Cultural Personality Analyzer

A sophisticated NLP-based system that analyzes user text and matches it with French cultural figures (philosophers, writers, and artists) based on semantic similarity and linguistic patterns.

## Screenshots

### Main Interface
![Main Interface](screenshots/Screenshot_1.png)
*Beautiful, modern UI for text input with real-time word counting*

### Analysis Results
![Analysis Results](screenshots/Screenshot_2.png)
*Detailed cultural figure matches with similarity scores and explanations*

### Cultural Landscape Visualization
![2D Projection](screenshots/Screenshot_3.png)
*Interactive 2D visualization showing your position in cultural space*

### Writing Analysis Dashboard
![Writing Features](screenshots/wScreenshot_4.png)
*Comprehensive linguistic feature analysis of your text*

> **Note**: Screenshots show the application running on `http://localhost:5000` with backend on port `8080`

## Features

- **Advanced NLP Analysis**: Uses state-of-the-art sentence transformers for semantic understanding
- **30+ Cultural Figures**: Comprehensive dataset of French philosophers, writers, and artists
- **Explainable AI**: Provides detailed explanations for why matches were made
- **Interactive Visualization**: 2D projection showing your position in cultural space
- **Real-time Analysis**: Fast processing with FAISS vector search
- **Beautiful UI**: Modern, responsive interface built with Tailwind CSS

## Architecture

### Backend
- **FastAPI**: High-performance REST API
- **Sentence Transformers**: Multilingual embeddings (paraphrase-multilingual-mpnet-base-v2)
- **FAISS**: Efficient similarity search
- **Python 3.10+**: Modern Python features

### Frontend
- **HTML/CSS/JS**: Vanilla JavaScript for simplicity
- **Tailwind CSS**: Beautiful, responsive design
- **Chart.js**: Interactive visualizations

## Quick Start

### Prerequisites
- Python 3.10+
- pip

### Installation

1. **Clone the repository**
```bash
cd culture-project
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the backend**
```bash
cd backend
python -m app.main
```

The API will be available at `http://localhost:8000`

4. **Run the frontend**
```bash
cd frontend
python -m http.server 3000
```

The UI will be available at `http://localhost:3000`

### Using Docker

```bash
docker-compose up -d
```

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`
- API Docs: `http://localhost:8000/docs`

## API Endpoints

### POST /api/analyze
Analyze text and get cultural figure matches.

**Request:**
```json
{
  "text": "Your text here (150-500 words recommended)",
  "mode": "detailed",
  "top_k": 3
}
```

**Response:**
```json
{
  "matches": [
    {
      "name": "Albert Camus",
      "score": 0.87,
      "reason": "Explanation...",
      "category": "philosopher",
      "period": "20th century",
      "key_themes": ["existential", "absurd"],
      "recommendation": {
        "book": "The Stranger",
        "type": "novel",
        "year": "1942"
      }
    }
  ],
  "projection": [...],
  "user_embedding_summary": {...},
  "processing_time_ms": 234.5
}
```

### GET /api/health
Health check endpoint.

## Testing

Run the comprehensive test suite:

```bash
pytest tests/ -v --cov=backend
```

## Dataset

The system includes 30 French cultural figures:

**Philosophers:**
- Albert Camus, Simone de Beauvoir, Jean-Paul Sartre
- Michel Foucault, René Descartes, Blaise Pascal
- Montaigne, Jean-Jacques Rousseau, Montesquieu
- Roland Barthes

**Writers:**
- Marcel Proust, Victor Hugo, Émile Zola
- Voltaire, Gustave Flaubert, Marguerite Duras
- Arthur Rimbaud, Honoré de Balzac, André Gide
- Stendhal, Colette, Charles Baudelaire
- Molière, Georges Sand, Paul Valéry
- André Malraux, Françoise Sagan, Jules Verne
- Hélène Cixous, Guy de Maupassant, Anaïs Nin
- Antoine de Saint-Exupéry

Each figure includes:
- Representative texts (3-10 samples)
- Thematic categorization
- Writing style analysis
- Book recommendations

## How It Works

1. **Text Input**: User provides 150-500 words of free-form text
2. **Preprocessing**: Text is cleaned and normalized
3. **Feature Extraction**: Linguistic features are extracted
4. **Embedding**: Text is converted to semantic vector using sentence transformers
5. **Similarity Search**: FAISS finds most similar cultural figures
6. **Explanation**: AI generates detailed reasoning for matches
7. **Visualization**: PCA projects embeddings to 2D space

## Project Structure

```
culture-project/
├── backend/
│   └── app/
│       ├── api/
│       │   └── routes.py
│       ├── core/
│       │   └── config.py
│       ├── models/
│       │   └── schemas.py
│       ├── services/
│       │   ├── embedding_service.py
│       │   ├── vector_store.py
│       │   ├── analyzer_service.py
│       │   └── data_loader.py
│       └── main.py
├── data/
│   └── cultural_figures/
│       └── dataset.json
├── frontend/
│   ├── index.html
│   └── app.js
├── tests/
│   ├── test_embedding_service.py
│   ├── test_vector_store.py
│   └── test_api.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Configuration

Edit `backend/app/core/config.py` to customize:
- Embedding model
- Similarity threshold
- Default top-k results
- CORS origins

## Performance

- Average analysis time: ~200-500ms
- Embedding dimension: 768
- Index size: 30 cultural figures
- Scalable to 1000+ figures

## Privacy & Ethics

- No data is stored without consent
- All processing is done on-demand
- Explanations emphasize uncertainty
- Avoids cultural stereotyping

## Future Extensions

- [ ] Expansion to other cultures (Italian, Spanish, etc.)
- [ ] Long-term user personalization
- [ ] Image-based personality analysis
- [ ] Multi-language support
- [ ] PostgreSQL for persistent storage
- [ ] User feedback collection

## License

This project is for educational and research purposes.

## Contributing

Contributions welcome! Please ensure:
- All tests pass
- Code is formatted with black
- Type hints are included
- Documentation is updated

## Support

For issues or questions, please open a GitHub issue.
