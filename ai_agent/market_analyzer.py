"""Analisis pasar crypto dari bridge MT5."""
import requests
from config import BRIDGE_URL, CRYPTO_SYMBOLS


def get_symbol_tick(symbol):
    """Ambil tick data untuk simbol dari bridge."""
    try:
        resp = requests.get("{}".format(BRIDGE_URL) + "/tick/" + symbol, timeout=10)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print("Error ambil tick {}: {}".format(symbol, e))
    return None


def get_symbol_daily(symbol):
    """Ambil data daily high/low untuk simbol."""
    try:
        resp = requests.get("{}".format(BRIDGE_URL) + "/daily/" + symbol, timeout=10)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print("Error ambil daily {}: {}".format(symbol, e))
    return None


def analyze_market():
    """Analisis seluruh simbol crypto dan kembalikan hasil."""
    results = []
    for symbol in CRYPTO_SYMBOLS:
        daily = get_symbol_daily(symbol)
        if daily:
            results.append(daily)
    return results