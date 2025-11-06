# StockLens Python SDK

Utilities for stock news summarization, technical indicators, text-to-speech, and text sentiment.

## Installation

```bash
pip install .
# or with optional MongoDB support
pip install .[mongo]
```

## Minimal sentiment (your requested style)

```python
from stocklens import StockLens

# Uses default n8n webhook automatically
sl = StockLens(api_key="your_api_key")
sentiment = sl.analyze("INFY")
print(sentiment)
# -> { 'label': 'Positive' | 'Neutral' | 'Negative', 'score': 0.xx, 'indicators': {...}, 'news_sentiment': {...} }

# analyze() combines technical indicators + news sentiment from n8n webhook
# To use only technical indicators: sl.analyze("INFY", use_news=False)
```

## Quick Start

```python
from stocklens import generate_summary, get_technical_indicators, generate_audio, analyze_sentiment
from stocklens.storage import MongoStorage

articles = [
    {"headline": "Company beats estimates", "summary": "Earnings exceeded expectations."},
    {"headline": "Guidance raised", "summary": "Management increased FY guidance."},
]

summary = generate_summary(articles)
print("Summary:", summary)

ind = get_technical_indicators("INFY")
print("Indicators:", ind)

path = generate_audio(summary, symbol="INFY")
print("Audio file:", path)

sent, score = analyze_sentiment("This stock looks strong with improving fundamentals")
print(sent, score)

# Optional: persist to MongoDB
# storage = MongoStorage("mongodb://localhost:27017", db_name="stocklens")
# storage.save_summary("INFY", summary, path)
# storage.save_indicators("INFY", ind)
```

## Whole-project facade (backend flow as SDK)

You can run the full workflow (fetch news via your n8n webhook, per-article sentiment, overall metrics, LLM summary, optional TTS, optional MongoDB persistence) via the `StockLens` class:

```python
from stocklens import StockLens
# Optionally: from stocklens.storage import MongoStorage

# Uses default webhook: https://owl-winning-legally.ngrok-free.app/webhook/sentiment
sl = StockLens()  # Or specify custom: StockLens(n8n_webhook_url="https://...")
result = sl.process_symbol("INFY", do_tts=True)

print(result["overall_sentiment"])  # dict with counts + overall label
print(result["summary_text"])       # LLM summary
print(result["audio_path"])         # mp3 path if TTS enabled
```

### CLI

```bash
# Uses default webhook
python -m stocklens INFY --audio-dir ./audio

# Custom webhook
python -m stocklens INFY --webhook https://your-ngrok/webhook/sentiment --audio-dir ./audio

# disable tts
python -m stocklens INFY --webhook https://your-ngrok/webhook/sentiment --no-tts

# with MongoDB persistence
python -m stocklens INFY --webhook https://your-ngrok/webhook/sentiment --mongo-uri mongodb://localhost:27017 --mongo-db stocklens
```

## Notes
- First use of `generate_summary` downloads the HF model; ensure internet access.
- `generate_audio` writes an MP3 file to `static/audio` by default; pass `output_dir` to override.
- `get_technical_indicators` queries Yahoo Finance and may be rate-limited; results include RSI, MACD, and Bollinger Bands.

