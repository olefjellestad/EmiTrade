import ccxt
import pandas as pd

import ccxt
import pandas as pd

def get_ohlcv_data(limit=100):
    exchange = ccxt.kucoin()
    markets = exchange.load_markets()
    
    # Hent topp "limit" par som slutter på USDT
    usdt_pairs = [symbol for symbol in markets if symbol.endswith("/USDT")]
    usdt_pairs = usdt_pairs[:limit]

    data = {}
    for symbol in usdt_pairs:
        try:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=50)
            df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            data[symbol] = df
            print(f"✅ {symbol} lastet inn")
        except Exception as e:
            print(f"❌ Kunne ikke hente data for {symbol}: {e}")

    return data