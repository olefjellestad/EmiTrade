import requests

def send_telegram_alert(signal, token, chat_id):
    try:
        text_msg = (
            f"📈 <b>{signal['symbol']}</b> — <i>{signal['type']}</i>\n"
            f"{signal['comment']}\n"
            f"⭐️ Rating: {signal['rating']}\n"
            f"📊 RSI: {signal['rsi']} | MACD: {signal['macd']}\n"
            f"💼 BTC: {signal['btc_trend']} | {signal['session']} | {signal['orderbook_bias']}\n"
            f"🕒 {signal['timestamp']}"
        )
        send_url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(send_url, data={"chat_id": chat_id, "text": text_msg, "parse_mode": "HTML"})

        if signal.get('chart_path'):
            with open(signal['chart_path'], 'rb') as img:
                send_photo_url = f"https://api.telegram.org/bot{token}/sendPhoto"
                files = {'photo': img}
                data = {'chat_id': chat_id}
                requests.post(send_photo_url, files=files, data=data)

    except Exception as e:
        print(f"❌ Telegram-feil: {e}")