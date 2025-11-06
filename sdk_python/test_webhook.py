from stocklens import StockLens
import json

print("Testing n8n webhook integration...\n")

# Test with your webhook URL
sl = StockLens()  # Uses default webhook URL

# Test 1: Simple analyze (with news)
print("1. Testing analyze() with news sentiment:")
try:
    result = sl.analyze("INFY", use_news=True)
    print(f"   Label: {result['label']}")
    print(f"   Score: {result['score']}")
    if "news_sentiment" in result:
        print(f"   News Articles: {result['news_sentiment']}")
    print(f"   Technical Indicators: {'Available' if 'error' not in result['indicators'] else 'Error: ' + str(result['indicators'].get('error'))}")
except Exception as e:
    print(f"   Error: {e}")

print("\n2. Testing full process_symbol() workflow:")
try:
    result = sl.process_symbol("INFY", do_tts=False)  # Skip TTS for testing
    print(f"   Symbol: {result.get('symbol')}")
    print(f"   Articles Found: {len(result.get('articles', []))}")
    print(f"   Overall Sentiment: {result.get('overall_sentiment', {}).get('overall')}")
    print(f"   Summary: {result.get('summary_text', '')[:100]}...")
except Exception as e:
    print(f"   Error: {e}")

print("\n3. Testing fetch_news() directly:")
try:
    news = sl.fetch_news("INFY")
    print(f"   Symbol: {news.get('symbol')}")
    print(f"   Articles: {len(news.get('articles', []))}")
    if news.get('articles'):
        print(f"   First Article: {news['articles'][0].get('headline', '')[:60]}...")
except Exception as e:
    print(f"   Error: {e}")

print("\n✅ Webhook integration test complete!")

