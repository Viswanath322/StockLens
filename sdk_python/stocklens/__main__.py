import argparse
from .core import StockLens
from .storage import MongoStorage


def main():
    parser = argparse.ArgumentParser(description="StockLens CLI")
    parser.add_argument("symbol", help="Stock symbol, e.g., INFY")
    parser.add_argument("--webhook", required=True, help="n8n webhook URL that returns articles JSON")
    parser.add_argument("--no-tts", action="store_true", help="Disable TTS generation")
    parser.add_argument("--audio-dir", default="static/audio", help="Directory for mp3 output")
    parser.add_argument("--mongo-uri", default=None, help="MongoDB URI for persistence (optional)")
    parser.add_argument("--mongo-db", default="stocklens", help="MongoDB database name")
    args = parser.parse_args()

    storage = None
    if args.mongo_uri:
        storage = MongoStorage(args.mongo_uri, db_name=args.mongo_db)

    sl = StockLens(args.webhook, audio_output_dir=args.audio_dir)
    result = sl.process_symbol(args.symbol, do_tts=(not args.no_tts), storage=storage)
    # Minimal console output
    print({
        "symbol": result.get("symbol"),
        "overall_sentiment": result.get("overall_sentiment"),
        "summary_text": result.get("summary_text"),
        "audio_path": result.get("audio_path"),
        "articles": len(result.get("articles", [])),
    })


if __name__ == "__main__":
    main()

