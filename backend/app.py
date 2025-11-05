from flask import Flask, request, jsonify
import requests
from textblob import TextBlob
from flask_cors import CORS
from modules.summarizer import generate_summary   # 🧠 NEW
from modules.tts_generator import generate_audio   # 🔊 NEW

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Your n8n webhook URL (production URL)
N8N_WEBHOOK = "https://owl-winning-legally.ngrok-free.app/webhook/sentiment"

def analyze_sentiment(text):
    """Returns sentiment label and score based on polarity."""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        sentiment = "Positive"
    elif polarity < -0.1:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    return sentiment, round(polarity, 2)

@app.route("/api/sentiment", methods=["GET"])
def get_sentiment():
    """Fetch stock news from n8n, analyze sentiment, summarize, and generate audio."""
    symbol = request.args.get("stock", "")
    if not symbol:
        return jsonify({"error": "Please provide a stock symbol, e.g., ?stock=INFY"}), 400

    print(f"🔹 Requested stock: {symbol}")

    # 1️⃣ Fetch news from n8n webhook
    try:
        n8n_url = f"{N8N_WEBHOOK}?stock={symbol}"
        print(f"🔗 Fetching from n8n: {n8n_url}")
        response = requests.get(n8n_url)
        print(f"📦 n8n Response Code: {response.status_code}")
    except Exception as e:
        print("❌ Error fetching from n8n:", e)
        return jsonify({"error": "Failed to reach n8n webhook"}), 500

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch news from n8n"}), 500

    try:
        data = response.json()
        print("✅ Data received from n8n")
    except Exception as e:
        print("❌ JSON parse error:", e)
        return jsonify({"error": "Invalid JSON from n8n"}), 500

    # 2️⃣ Unwrap if it's a list
    if isinstance(data, list) and len(data) > 0:
        data = data[0]

    # 3️⃣ Ensure symbol is consistent
    data["symbol"] = symbol.upper()

    # 4️⃣ Perform sentiment analysis
    print("🧠 Analyzing sentiment for articles...")
    for article in data.get("articles", []):
        combined_text = f"{article['headline']} {article['summary']}"
        sentiment, score = analyze_sentiment(combined_text)
        article["sentiment"] = sentiment
        article["score"] = score
    print("✅ Sentiment analysis complete")

    # 5️⃣ Compute overall sentiment
    sentiments = [a["sentiment"] for a in data.get("articles", [])]
    pos, neg, neu = sentiments.count("Positive"), sentiments.count("Negative"), sentiments.count("Neutral")
    total = len(sentiments)
    overall = "Positive"
    if neg > pos:
        overall = "Negative"
    elif pos == neg:
        overall = "Neutral"
    data["overall_sentiment"] = {
        "positive_articles": pos,
        "negative_articles": neg,
        "neutral_articles": neu,
        "total_articles": total,
        "overall": overall
    }

    # 6️⃣ Generate LLM-based summary and TTS audio
    try:
        print("📝 Generating summary...")
        summary_text = generate_summary(data.get("articles", []))
        print("🔊 Generating audio...")
        audio_path = generate_audio(summary_text, symbol)
        data["summary_text"] = summary_text
        data["audio_url"] = audio_path
        print("✅ Summary and audio generated successfully")
    except Exception as e:
        data["summary_text"] = "Summary generation failed."
        data["audio_url"] = None
        print("⚠️ LLM or TTS Error:", e)

    print("✅ Completed processing request for:", symbol)
    return jsonify(data)


@app.route("/")
def home():
    return "✅ StockLens Backend is running! Use /api/sentiment?stock=INFY"

if __name__ == "__main__":
    app.run(debug=True)
