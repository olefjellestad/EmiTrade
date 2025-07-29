
from datetime import datetime
import pandas as pd
import talib

def get_session():
    now = datetime.utcnow()
    hour = now.hour
    if 0 <= hour < 8:
        return "Asia"
    elif 8 <= hour < 16:
        return "London"
    else:
        return "New York"

def evaluate_volume_strength(df):
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    if latest['close'] > prev['close']:
        return 5 if latest['volume'] > prev['volume'] else 3
    elif latest['close'] < prev['close']:
        return 4 if latest['volume'] > prev['volume'] else 2
    return 1

def mock_orderbook_sentiment(symbol):
    return "🤖 Kjøpspress"

def calculate_trade_levels(latest, prev, direction):
    buffer = 0.002  # 0.2% buffer
    entry = latest['close']

    if direction == "long":
        stop_loss = prev['low'] * (1 - buffer)
        target = latest['close'] * 1.02
    else:
        stop_loss = prev['high'] * (1 + buffer)
        target = latest['close'] * 0.98

    return round(entry, 4), round(stop_loss, 4), round(target, 4)

def analyze_symbol(df, symbol, btc_trend):
    signal = None
    df['rsi'] = talib.RSI(df['close'], timeperiod=14)
    macd, macdsignal, _ = talib.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    df['macd'] = macd
    df['macd_signal'] = macdsignal

    latest = df.iloc[-1]
    prev = df.iloc[-2]
    bos = latest['close'] > prev['high']
    choch = latest['close'] < prev['low']

    if latest['rsi'] < 35 and bos:
        entry, sl, tp = calculate_trade_levels(latest, prev, "long")
        signal = {
            "symbol": symbol,
            "rsi": round(latest["rsi"], 2),
            "macd": round(latest["macd"], 4),
            "macd_signal": round(latest["macd_signal"], 4),
            "volume": int(latest["volume"]),
            "comment": "✅ Break of Structure med lav RSI",
            "type": "Swing",
            "rating": evaluate_volume_strength(df),
            "session": get_session(),
            "btc_trend": btc_trend,
            "orderbook_bias": mock_orderbook_sentiment(symbol),
            "entry_price": entry,
            "stop_loss": sl,
            "target": tp,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    return signal

def analyze_signals(market_data):
    signals = []
    btc_df = market_data.get("BTC/USDT")
    btc_trend = "⚠️ Sideways"

    if btc_df is not None:
        btc_df['rsi'] = talib.RSI(btc_df['close'], timeperiod=14)
        macd, macdsignal, _ = talib.MACD(btc_df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
        btc_df['macd'] = macd
        btc_df['macd_signal'] = macdsignal
        latest = btc_df.iloc[-1]
        prev = btc_df.iloc[-2]
        bos = latest['close'] > prev['high']
        choch = latest['close'] < prev['low']
        if bos and latest['rsi'] > 50 and latest['macd'] > latest['macd_signal']:
            btc_trend = "📈 Bullish"
        elif choch and latest['rsi'] < 50 and latest['macd'] < latest['macd_signal']:
            btc_trend = "📉 Bearish"

    for symbol, df in market_data.items():
        signal = analyze_symbol(df, symbol, btc_trend)
        if signal:
            signals.append(signal)
    return signals
