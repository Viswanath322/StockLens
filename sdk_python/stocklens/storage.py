from typing import Optional, Dict, Any

try:
    from pymongo import MongoClient
except Exception:
    MongoClient = None  # optional dependency


class MongoStorage:
    def __init__(self, uri: str, db_name: str = "stocklens"):
        if MongoClient is None:
            raise RuntimeError("pymongo is not installed. Install with `pip install pymongo`.")
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def save_article_analysis(self, symbol: str, articles: list) -> str:
        doc = {"symbol": symbol, "articles": articles}
        res = self.db["articles"].insert_one(doc)
        return str(res.inserted_id)

    def save_summary(self, symbol: str, summary_text: str, audio_path: Optional[str] = None) -> str:
        doc = {"symbol": symbol, "summary_text": summary_text, "audio_path": audio_path}
        res = self.db["summaries"].insert_one(doc)
        return str(res.inserted_id)

    def save_indicators(self, symbol: str, indicators: Dict[str, Any]) -> str:
        doc = {"symbol": symbol, "indicators": indicators}
        res = self.db["indicators"].insert_one(doc)
        return str(res.inserted_id)

