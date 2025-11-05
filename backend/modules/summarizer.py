from transformers import pipeline

# Load once at startup
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def generate_summary(news_articles):
    if not news_articles:
        return "No relevant news articles found for this stock."

    # Combine all text
    text = " ".join([a.get("headline", "") + " " + a.get("summary", "") for a in news_articles])
    text = text.strip()

    if not text:
        return "No content available for summarization."

    # Hugging Face model limit ~1024 tokens
    text = text[:3000]  # safely truncate longer input

    try:
        result = summarizer(text, max_length=100, min_length=30, do_sample=False)
        return result[0]["summary_text"]
    except Exception as e:
        print("⚠️ Summarization error:", e)
        return "Failed to generate summary due to input size or model error."
