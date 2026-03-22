# Language Codes Reference

culture-identifier uses ISO 639-1 two-letter language codes.

## Nordic Languages

| Code | Language | Variants |
|---|---|---|
| `fi` | Finnish | — |
| `sv` | Swedish | Sweden (sv-SE), Finland (sv-FI) |
| `nb` | Norwegian Bokmål | — |
| `nn` | Norwegian Nynorsk | — |
| `da` | Danish | — |
| `is` | Icelandic | — |
| `et` | Estonian | — |
| `lv` | Latvian | — |
| `lt` | Lithuanian | — |

## Extended Model Languages

| Code | Language | Code | Language |
|---|---|---|---|
| `de` | German | `nl` | Dutch |
| `fr` | French | `es` | Spanish |
| `pl` | Polish | `cs` | Czech |
| `sk` | Slovak | `hu` | Hungarian |
| `ro` | Romanian | `bg` | Bulgarian |

## Response Format

The API returns BCP 47 tags when a dialect is detected:

```json
{
  "culture": "Swedish",
  "language": "sv-FI",  // Finland Swedish
  "confidence": 0.87
}
```
