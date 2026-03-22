# Accuracy and Limitations

## Supported Cultures and Accuracy

| Culture | Precision | Recall | F1 | Min text length |
|---|---|---|---|---|
| Finnish | 0.96 | 0.94 | 0.95 | 5 tokens |
| Swedish | 0.97 | 0.96 | 0.96 | 5 tokens |
| Norwegian | 0.93 | 0.91 | 0.92 | 10 tokens |
| Danish | 0.94 | 0.92 | 0.93 | 10 tokens |
| Estonian | 0.91 | 0.89 | 0.90 | 10 tokens |

## When Accuracy Drops

1. **Very short texts** (< 5 tokens): Confidence is unreliable
2. **Mixed-language texts**: Classified by dominant language
3. **Transliterated text**: Latin-script Finnish/Estonian harder to separate
4. **Technical text** (code, URLs, numbers): May default to generic Western European

## Confidence Thresholds

| Confidence | Interpretation | Recommendation |
|---|---|---|
| >= 0.90 | High confidence | Use prediction directly |
| 0.70–0.90 | Moderate confidence | Consider top-2 results |
| < 0.70 | Low confidence | Show "uncertain" to user |

## Improving Accuracy

Provide more context:

```python
# Less accurate: 3 words
client.identify("hyvää huomenta")

# More accurate: full sentence
client.identify("Hyvää huomenta! Miten menee tänään?")
```
