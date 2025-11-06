import requests
from typing import Dict, Any, Optional, List, Tuple

from .summarizer import generate_summary
from .tts import generate_audio
from .sentiment import analyze_sentiment
from .storage import MongoStorage  # optional at runtime if user imports
from .indicators import get_technical_indicators


def _compute_overall_sentiment(articles: List[Dict[str, Any]]) -> Dict[str, Any]:
    sentiments = [a.get("sentiment") for a in articles if a.get("sentiment")]
    pos = sentiments.count("Positive")
    neg = sentiments.count("Negative")
    neu = sentiments.count("Neutral")
    total = len(sentiments)
    overall = "Positive"
    if neg > pos:
        overall = "Negative"
    elif pos == neg:
        overall = "Neutral"
    return {
        "positive_articles": pos,
        "negative_articles": neg,
        "neutral_articles": neu,
        "total_articles": total,
        "overall": overall,
    }


class StockLens:
    def __init__(self, n8n_webhook_url: Optional[str] = None, audio_output_dir: str = "static/audio", api_key: Optional[str] = None):
        # Default to your n8n webhook if not provided
        if n8n_webhook_url:
            self.n8n_webhook_url = n8n_webhook_url.rstrip("/")
        else:
            # Use default webhook URL
            self.n8n_webhook_url = "https://owl-winning-legally.ngrok-free.app/webhook/sentiment"
        self.audio_output_dir = audio_output_dir
        self.api_key = api_key

    def fetch_news(self, symbol: str) -> Dict[str, Any]:
        if not self.n8n_webhook_url:
            raise ValueError("n8n_webhook_url is not set. Provide it in StockLens(..., n8n_webhook_url=\"...\").")
        url = f"{self.n8n_webhook_url}?stock={symbol}"
        # Optionally forward api_key as query param if provided
        if self.api_key:
            url += f"&api_key={self.api_key}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }
        # Add ngrok bypass header if using ngrok URL
        if "ngrok" in self.n8n_webhook_url:
            headers["ngrok-skip-browser-warning"] = "true"
        
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list) and data:
            data = data[0]
        data["symbol"] = symbol.upper()
        data.setdefault("articles", [])
        return data

    def analyze_articles(self, articles: List[Dict[str, Any]]) -> None:
        for article in articles:
            combined_text = f"{article.get('headline', '')} {article.get('summary', '')}".strip()
            sentiment, score = analyze_sentiment(combined_text)
            article["sentiment"] = sentiment
            article["score"] = score

    def process_symbol(self, symbol: str, *, do_tts: bool = True, storage: Optional[MongoStorage] = None) -> Dict[str, Any]:
        data = self.fetch_news(symbol)
        self.analyze_articles(data.get("articles", []))

        overall = _compute_overall_sentiment(data.get("articles", []))
        data["overall_sentiment"] = overall

        summary_text = generate_summary(data.get("articles", []))
        data["summary_text"] = summary_text

        audio_path = None
        if do_tts:
            audio_path = generate_audio(summary_text, symbol, output_dir=self.audio_output_dir)
        data["audio_path"] = audio_path

        if storage is not None:
            storage.save_article_analysis(symbol, data.get("articles", []))
            storage.save_summary(symbol, summary_text, audio_path)

        return data

    def analyze(self, symbol: str, use_news: bool = True) -> Dict[str, Any]:
        """Analyze stock sentiment combining technical indicators and optionally news sentiment.
        
        Args:
            symbol: Stock symbol to analyze
            use_news: If True (default), fetch news from n8n webhook and combine with technical indicators
        
        Returns a dict with: { label: str, score: float, indicators: dict, news_sentiment: dict (optional) }
        """
        indicators = get_technical_indicators(symbol)
        tech_score = 0.0
        news_score = 0.0
        news_sentiment = None
        
        # Calculate technical indicators score
        if "error" not in indicators:
            rsi = indicators.get("RSI")
            macd = indicators.get("MACD")
            signal = indicators.get("Signal")
            
            if isinstance(rsi, (int, float)):
                if rsi >= 60:
                    tech_score += 0.35
                elif rsi <= 40:
                    tech_score -= 0.35
            
            if isinstance(macd, (int, float)) and isinstance(signal, (int, float)):
                if macd > signal:
                    tech_score += 0.45
                elif macd < signal:
                    tech_score -= 0.45
        
        # Optionally fetch and analyze news sentiment
        if use_news and self.n8n_webhook_url:
            try:
                news_data = self.fetch_news(symbol)
                articles = news_data.get("articles", [])
                if articles:
                    self.analyze_articles(articles)
                    overall = _compute_overall_sentiment(articles)
                    news_sentiment = overall
                    # Convert news sentiment to score: Positive=0.5, Neutral=0, Negative=-0.5
                    if overall["overall"] == "Positive":
                        news_score = 0.5 * (overall["positive_articles"] / max(overall["total_articles"], 1))
                    elif overall["overall"] == "Negative":
                        news_score = -0.5 * (overall["negative_articles"] / max(overall["total_articles"], 1))
            except Exception:
                # If news fetch fails, continue with technical indicators only
                pass
        
        # Combine scores (weighted: 60% tech, 40% news if available)
        if news_sentiment:
            combined_score = (tech_score * 0.6) + (news_score * 0.4)
        else:
            combined_score = tech_score
        
        label = "Neutral"
        if combined_score >= 0.2:
            label = "Positive"
        elif combined_score <= -0.2:
            label = "Negative"
        
        result = {
            "label": label,
            "score": round(combined_score, 2),
            "indicators": indicators,
        }
        
        if news_sentiment:
            result["news_sentiment"] = news_sentiment
        
        return result

