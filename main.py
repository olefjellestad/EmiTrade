
import time
import pandas as pd
from datetime import datetime
from kucoin_data import get_ohlcv_data
from ta_engine import analyze_signals
from alert_dispatch import send_telegram_alert

def save_signals_to_csv(signals, filename="signal_log.csv"):
    df = pd.DataFrame(signals)
    df.to_csv(filename, mode='a', header=not pd.io.common.file_exists(filename), index=False)

if __name__ == "__main__":
    print("🚀 SignalBot er aktiv og overvåker markedet kontinuerlig...")

    while True:
        print("\n🔄 Ny analyse-runde starter...")
        print("🔄 Henter OHLCV-data fra KuCoin (topp 100 USDT-par)...")

        try:
            market_data = get_ohlcv_data(limit=100)
        except Exception as e:
            print(f"❌ Feil ved henting av markedsdata: {e}")
            time.sleep(60)
            continue

        print("📊 Kjører teknisk analyse...")
        signals = analyze_signals(market_data)

        if signals:
            print(f"🚨 {len(signals)} signal(er) funnet – sender til Telegram...")
            for signal in signals:
                try:
                    send_telegram_alert(signal)
                except Exception as e:
                    print(f"❌ Telegram-feil: {e}")
            save_signals_to_csv(signals)
        else:
            print("📭 Ingen signaler funnet akkurat nå.")

        print("⏳ Venter i 15 minutter før neste sjekk...")
        time.sleep(900)
