from transformers import pipeline

# Load once at import time for efficiency
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def generate_summary(news_articles):
    if not news_articles:
        return "No relevant news articles found for this stock."

    # Accept plain string OR list of dicts/strings
    if isinstance(news_articles, str):
        text = news_articles.strip()
    elif isinstance(news_articles, list):
        if len(news_articles) > 0 and isinstance(news_articles[0], dict):
            text = " ".join([a.get("headline", "") + " " + a.get("summary", "") for a in news_articles]).strip()
        else:
            text = " ".join([str(x) for x in news_articles]).strip()
    else:
        text = str(news_articles).strip()

    if not text:
        return "No content available for summarization."

    # Hugging Face model limit ~1024 tokens; truncate conservatively
    text = text[:3000]
    
    # Dynamically adjust max_length based on input length to avoid warnings
    text_length = len(text.split())
    # For very short texts, return as-is or use minimal summary
    if text_length < 15:
        # For very short texts, return original or simplified version
        if text_length < 10:
            return text  # Too short to summarize meaningfully
        max_len = max(5, text_length - 2)
        min_len = max(3, max_len // 2)
    elif text_length < 30:
        max_len = min(50, max(10, text_length - 5))
        min_len = max(5, max_len // 2)
    else:
        max_len = 100
        min_len = 30

    try:
        result = summarizer(text, max_length=max_len, min_length=min_len, do_sample=False)
        return result[0]["summary_text"]
    except Exception:
        return "Failed to generate summary due to input size or model error."

