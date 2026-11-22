"""Konfigurasi AI Agent."""
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
BRIDGE_URL = os.getenv("BRIDGE_URL", "http://localhost:5000")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "8000471218")
LOT_SIZE = float(os.getenv("LOT_SIZE", "0.01"))
AI_PROVIDER = os.getenv("AI_PROVIDER", "openai")

CRYPTO_SYMBOLS = ["BTC", "ETH", "SOL", "XRP", "ADA", "DOGE", "TRX", "LTC", "LINK", "DOT"]