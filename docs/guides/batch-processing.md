# Batch Processing

## HTTP Batch API

Process multiple texts in one request:

```bash
POST /identify/batch
Content-Type: application/json

{
  "texts": [
    "Hyvää huomenta!",
    "God morgon!",
    "Guten Morgen!"
  ],
  "top_k": 1
}
```

Response:

```json
{
  "results": [
    {"culture": "Finnish", "confidence": 0.94, "language": "fi"},
    {"culture": "Swedish", "confidence": 0.96, "language": "sv"},
    {"culture": "German", "confidence": 0.91, "language": "de"}
  ],
  "processing_ms": 28,
  "batch_size": 3
}
```

## Python Client

```python
from culture_identifier import CultureIdentifier

client = CultureIdentifier(api_url="http://localhost:8000")

texts = ["Hyvää huomenta!", "God morgon!", "Guten Morgen!"]
results = client.identify_batch(texts, top_k=1)

for text, result in zip(texts, results):
    print(f"{text!r} → {result.culture} ({result.confidence:.0%})")
```

## Large-Scale Processing

```python
import asyncio
from culture_identifier import AsyncCultureIdentifier

async def process_dataset(texts: list[str]) -> list[dict]:
    client = AsyncCultureIdentifier(api_url="...", concurrency=10)
    return await client.identify_batch_parallel(texts, batch_size=100)
```
