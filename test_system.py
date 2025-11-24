"""End-to-end system test."""
import sys
sys.path.insert(0, 'backend')

from backend.app.services import EmbeddingService, VectorStore, CulturalAnalyzer
from backend.app.services.data_loader import DataLoader
from backend.app.core import settings
import time

def main():
    print("=" * 80)
    print("CULTURAL PERSONALITY ANALYZER - SYSTEM TEST")
    print("=" * 80)
    print()

    # Step 1: Load embedding service
    print("[1/5] Loading embedding model...")
    start = time.time()
    embedding_service = EmbeddingService(model_name=settings.embedding_model)
    print(f"[OK] Model loaded in {time.time() - start:.2f}s")
    print(f"  - Embedding dimension: {embedding_service.embedding_dim}")
    print()

    # Step 2: Initialize vector store
    print("[2/5] Initializing vector store...")
    vector_store = VectorStore(embedding_dim=embedding_service.embedding_dim)
    print(f"[OK] Vector store initialized")
    print()

    # Step 3: Load and index dataset
    print("[3/5] Loading cultural figures dataset...")
    data_loader = DataLoader()
    data = data_loader.load_dataset(settings.dataset_path)
    data_loader.validate_dataset(data)
    print(f"[OK] Loaded {len(data)} cultural figures")
    print()

    print("[4/5] Generating embeddings and building index...")
    start = time.time()
    texts, metadata = data_loader.prepare_for_indexing(data)
    embeddings = embedding_service.encode(texts, show_progress=True)
    vector_store.add_vectors(embeddings, metadata)
    print(f"[OK] Index built in {time.time() - start:.2f}s")
    print(f"  - Indexed {vector_store.size()} cultural figures")
    print()

    # Step 4: Initialize analyzer
    print("[5/5] Initializing cultural analyzer...")
    analyzer = CulturalAnalyzer(embedding_service, vector_store)
    print("[OK] Analyzer ready")
    print()

    # Test analysis with sample texts
    print("=" * 80)
    print("RUNNING TEST ANALYSES")
    print("=" * 80)
    print()

    test_texts = [
        {
            "name": "Existential Reflection",
            "text": """Life is absurd, yet we must find meaning in this absurdity. Every day we wake up,
            perform our routines, and yet we know that one day it will all end. The question is not
            whether life has meaning, but whether we have the courage to create meaning despite the
            inherent meaninglessness of existence. We are free, radically free, and this freedom is
            both our greatest gift and our heaviest burden. To exist is to be thrown into a world
            we did not choose, yet we must choose how to live within it."""
        },
        {
            "name": "Romantic Contemplation",
            "text": """Love is the most profound force in the universe. When I look into your eyes, I see
            not just another person, but a reflection of my own soul. The beauty of the world reveals
            itself in moments of passion, in the gentle touch of a hand, in the poetry of existence.
            Nature speaks to us through its beauty, and we respond with our hearts. Every sunset is
            a reminder that life is fleeting, and thus we must cherish every moment of connection."""
        },
        {
            "name": "Social Commentary",
            "text": """Society oppresses the individual through its institutions and norms. The powerful
            maintain their position by controlling discourse, by shaping what we consider normal and
            acceptable. We must question authority, challenge the status quo, and fight for justice.
            The system is designed to benefit the few at the expense of the many. True freedom requires
            revolution, not just of the political order, but of our consciousness itself."""
        }
    ]

    for i, test in enumerate(test_texts, 1):
        print(f"\nTest {i}: {test['name']}")
        print("-" * 80)
        print(f"Text excerpt: {test['text'][:100]}...")
        print()

        start = time.time()
        matches, projection, summary = analyzer.analyze(test['text'], top_k=3, mode="detailed")
        elapsed = (time.time() - start) * 1000

        print(f"[OK] Analysis completed in {elapsed:.0f}ms")
        print()
        print("Top Matches:")
        for j, match in enumerate(matches, 1):
            print(f"  {j}. {match['name']} ({match['category']}) - Score: {match['score']:.2f}")
            print(f"     Period: {match['period']}")
            print(f"     Reason: {match['reason'][:120]}...")
            if match.get('recommendation') and match['recommendation'].get('book'):
                print(f"     Recommended: {match['recommendation']['book']}")
            print()

        print(f"Writing Features:")
        features = summary['features']
        print(f"  - Word count: {features['word_count']}")
        print(f"  - Sentence count: {features['sentence_count']}")
        print(f"  - Avg sentence length: {features['avg_sentence_length']:.1f} words")
        print(f"  - Question density: {features['question_density']*100:.1f}%")
        print(f"  - Complex words: {features['complex_word_ratio']*100:.1f}%")
        print(f"  - Detected themes: {', '.join(summary['themes'][:3])}")
        print()

    print("=" * 80)
    print("ALL TESTS PASSED SUCCESSFULLY!")
    print("=" * 80)
    print()
    print("System is ready for deployment!")
    print()
    print("To start the server:")
    print("  cd backend")
    print("  uvicorn app.main:app --reload")
    print()
    print("Then open frontend/index.html in a browser")
    print("or start a simple HTTP server:")
    print("  cd frontend")
    print("  python -m http.server 3000")
    print()

if __name__ == "__main__":
    main()
