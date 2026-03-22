# API Guide

## Identify Culture

```bash
POST /identify
Content-Type: application/json

{
  "text": "Hyvää huomenta! Miten menee?",
  "top_k": 3
}
```

Response:

```json
{
  "predictions": [
    {"culture": "Finnish", "confidence": 0.94, "language": "fi"},
    {"culture": "Estonian", "confidence": 0.04, "language": "et"},
    {"culture": "Swedish", "confidence": 0.01, "language": "sv"}
  ],
  "processing_ms": 12
}
```

## Batch Identification

```bash
POST /identify/batch
Content-Type: application/json

{
  "texts": ["...", "...", "..."],
  "top_k": 1
}
```

## Supported Cultures

| Culture | Language Codes | Training Samples |
|---|---|---|
| Finnish | fi | 50,000 |
| Swedish | sv | 45,000 |
| Norwegian | nb, nn | 40,000 |
| Danish | da | 38,000 |
| Estonian | et | 25,000 |

## Confidence Calibration

Confidence scores are calibrated using Platt scaling on a held-out validation set. A score >= 0.85 indicates high confidence.
