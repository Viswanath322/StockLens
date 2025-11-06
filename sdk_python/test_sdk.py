from stocklens import StockLens

# Simple usage - uses default webhook automatically
sl = StockLens()
sentiment = sl.analyze("AAPL")
print(sentiment)
# Returns: {'label': 'Neutral', 'score': 0.08, 'indicators': {...}, 'news_sentiment': {...}}

# Full workflow with summary and TTS
result = sl.process_symbol("AAPL", do_tts=True)
print(result["overall_sentiment"])  # News sentiment analysis
print(result["summary_text"])       # LLM-generated summary
