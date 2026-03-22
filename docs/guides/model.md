# Model Guide

## Architecture

culture-identifier uses a hierarchical classification approach:

```
Input text
    │
    ▼
Language Detection (fastText)
    │
    ▼
Culture Classification (fine-tuned XLM-RoBERTa)
    │
    ▼
Confidence Calibration (Platt scaling)
    │
    ▼
Top-K results with confidence scores
```

## Why XLM-RoBERTa?

- Pretrained on 100 languages — Nordic languages well-represented
- Better on short texts (< 100 tokens) than mBERT
- Fine-tuning on cultural text markers outperforms language-only detection

## Training

The model is fine-tuned on a dataset of culturally distinctive text patterns:
- Idioms and proverbs
- Cultural references (foods, places, traditions)
- Writing style markers

## Confidence Calibration

Raw model probabilities are overconfident. We use Platt scaling to produce calibrated probabilities:

```python
from sklearn.calibration import CalibratedClassifierCV

calibrated = CalibratedClassifierCV(base_model, method="sigmoid", cv=5)
calibrated.fit(X_val, y_val)
```

A score of 0.85 means "85% of predictions with this confidence are correct."

## Supported Languages

Nordic languages: Finnish (fi), Swedish (sv), Norwegian (nb/nn), Danish (da), Estonian (et), Icelandic (is).
Baltic and Germanic languages available in the extended model.
