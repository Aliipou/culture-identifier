# CLI Usage

culture-identifier includes a command-line interface for quick identification and batch processing.

## Single Text

```bash
culture-identify "Hyvää huomenta!"

Culture: Finnish (94%)
Language: fi
```

## Batch from File

```bash
culture-identify --input texts.txt --output results.jsonl --top-k 3

# results.jsonl:
{"text": "Hyvää huomenta!", "predictions": [{"culture": "Finnish", "confidence": 0.94}]}
{"text": "God morgon!", "predictions": [{"culture": "Swedish", "confidence": 0.96}]}
```

## Pipe Mode

```bash
cat data.csv | culture-identify --format csv --column text | head

text,culture,confidence
"Hyvää huomenta!",Finnish,0.94
"God morgon!",Swedish,0.96
```

## Options

```
--top-k INT          Number of results per text (default: 1)
--threshold FLOAT    Min confidence to include (default: 0.0)
--format TEXT        Output format: json, jsonl, csv, tsv (default: jsonl)
--column TEXT        Column name for CSV/TSV input (default: text)
--api-url URL        Override API URL (default: http://localhost:8000)
--batch-size INT     Batch size for API calls (default: 100)
```
