import yfinance as yf
import pandas as pd
import numpy as np
import requests

def _safe_float(value):
    try:
        return float(value) if value is not None else None
    except Exception:
        return None

def get_technical_indicators(symbol):
    try:
        # Try multiple suffixes to fetch valid data
        possible_symbols = [symbol.upper(), f"{symbol.upper()}.NS", f"{symbol.upper()}.BO", f"{symbol.upper()}.NSE"]
        data = None
        successful_symbol = None

        # Use a custom session with a desktop User-Agent to avoid provider blocking
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
        })

        for s in possible_symbols:
            try:
                # Attempt 1: download API
                temp = yf.download(s, period="6mo", interval="1d", progress=False, show_errors=False, threads=False, session=session)
                if temp is not None and not temp.empty and len(temp) >= 30:
                    data = temp
                    successful_symbol = s
                    break

                # Attempt 2: Ticker.history fallback
                ticker = yf.Ticker(s, session=session)
                hist = ticker.history(period="6mo", interval="1d")
                if hist is not None and not hist.empty and len(hist) >= 30:
                    data = hist
                    successful_symbol = s
                    break

                # Attempt 3: Direct Yahoo chart API
                url = f"https://query1.finance.yahoo.com/v8/finance/chart/{s}?range=6mo&interval=1d"
                resp = session.get(url, timeout=10)
                if resp.status_code == 200:
                    j = resp.json()
                    result_nodes = (j or {}).get("chart", {}).get("result", [])
                    if result_nodes:
                        node = result_nodes[0]
                        indicators = (node.get("indicators", {}) or {}).get("quote", [])
                        closes = indicators[0].get("close") if indicators else None
                        if closes:
                            # Filter out None values and build a minimal DataFrame with Close
                            close_series = pd.Series(closes, dtype=float)
                            close_series = close_series.dropna()
                            if len(close_series) >= 30:
                                data = pd.DataFrame({"Close": close_series.values})
                                successful_symbol = s
                                break
            except Exception as e:
                continue

        if data is None or data.empty:
            return {"error": f"No valid data found for symbol: {symbol}. Tried: {', '.join(possible_symbols)}"}

        close_prices = data["Close"].values.astype(float)
        result = {"symbol": successful_symbol}

        # RSI calculation
        def calculate_rsi(prices, period=14):
            delta = pd.Series(prices).diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi.dropna().iloc[-1] if not rsi.dropna().empty else None

        result["RSI"] = _safe_float(calculate_rsi(close_prices))

        # MACD calculation
        def calculate_macd(prices, fast=12, slow=26, signal=9):
            ema_fast = pd.Series(prices).ewm(span=fast).mean()
            ema_slow = pd.Series(prices).ewm(span=slow).mean()
            macd_line = ema_fast - ema_slow
            signal_line = macd_line.ewm(span=signal).mean()
            return macd_line.dropna().iloc[-1] if not macd_line.dropna().empty else None, signal_line.dropna().iloc[-1] if not signal_line.dropna().empty else None

        macd, signal = calculate_macd(close_prices)
        result["MACD"] = _safe_float(macd)
        result["Signal"] = _safe_float(signal)

        # Bollinger Bands calculation
        def calculate_bollinger_bands(prices, period=20, std_dev=2):
            sma = pd.Series(prices).rolling(window=period).mean()
            std = pd.Series(prices).rolling(window=period).std()
            upper = sma + (std * std_dev)
            lower = sma - (std * std_dev)
            return upper.dropna().iloc[-1] if not upper.dropna().empty else None, sma.dropna().iloc[-1] if not sma.dropna().empty else None, lower.dropna().iloc[-1] if not lower.dropna().empty else None

        bb_upper, bb_middle, bb_lower = calculate_bollinger_bands(close_prices)
        result["BOLL_UPPER"] = _safe_float(bb_upper)
        result["BOLL_MIDDLE"] = _safe_float(bb_middle)
        result["BOLL_LOWER"] = _safe_float(bb_lower)

        return result

    except Exception as e:
        return {"error": str(e)}
