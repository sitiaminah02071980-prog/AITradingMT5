"""Notifikasi ke Telegram."""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "8000471218")


def send_message(text):
    """Kirim pesan teks ke Telegram chat."""
    if not TELEGRAM_BOT_TOKEN:
        print("TELEGRAM_BOT_TOKEN tidak diatur, pesan tidak terkirim.")
        return False

    url = "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except Exception as e:
        print("Gagal mengirim pesan Telegram: {}".format(e))
        return False


def send_signal_alert(signal_data):
    """Kirim alert sinyal trading ke Telegram."""
    text = (
        "<b>🚨 Sinyal Trading MT5</b>\n"
        "Simbol: " + signal_data["symbol"] + "\n"
        "Sinyal: " + signal_data["signal"] + "\n"
        "Bid: " + str(signal_data["bid"]) + "\n"
        "Daily High: " + str(signal_data["bid_high"]) + "\n"
        "Daily Low: " + str(signal_data["bid_low"]) + "\n"
        "Lot: " + str(signal_data.get("lot_size", 0.01)) + "\n"
        "Alasan: " + signal_data["reason"]
    )
    return send_message(text)