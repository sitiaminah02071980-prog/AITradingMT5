"""Integrasi AI dengan OpenAI dan Gemini untuk analisis pasar."""
import os
import json
import requests
from dotenv import load_dotenv
from config import OPENAI_API_KEY, GEMINI_API_KEY, BRIDGE_URL, LOT_SIZE

load_dotenv()


class AIIntegration:
    """Kelas untuk integrasi AI dengan OpenAI dan Gemini."""

    def __init__(self):
        self.openai_api_key = OPENAI_API_KEY
        self.gemini_api_key = GEMINI_API_KEY
        self.bridge_url = BRIDGE_URL
        self.lot_size = LOT_SIZE

    def analyze_with_openai(self, symbol, bid, bid_high, bid_low, reason):
        """Analisis pasar menggunakan OpenAI API."""
        if not self.openai_api_key:
            return {"error": "OPENAI_API_KEY tidak diatur"}

        prompt = (
            f"Anda adalah asisten trading crypto profesional. Berikan analisis singkat untuk simbol {symbol}.\n"
            f"Data pasar:\n"
            f"- Bid: {bid}\n"
            f"- Daily High (Swing High): {bid_high}\n"
            f"- Daily Low (Swing Low): {bid_low}\n"
            f"- Sinyal dasar: {reason}\n"
            f"- Lot size disarankan: {self.lot_size}\n\n"
            "Berikan rekomendasi BUY/SELL/HOLD dengan alasan dan level stop loss serta take profit "
            "berdasarkan swing high dan swing low. Jawab dalam bahasa Indonesia, singkat dan padat."
        )

        try:
            resp = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.openai_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 300,
                    "temperature": 0.7,
                },
                timeout=30,
            )
            if resp.status_code == 200:
                data = resp.json()
                return {
                    "provider": "openai",
                    "symbol": symbol,
                    "analysis": data["choices"][0]["message"]["content"],
                    "lot_size": self.lot_size,
                }
            else:
                return {"error": f"OpenAI API error: {resp.status_code} {resp.text}"}
        except Exception as e:
            return {"error": f"OpenAI request gagal: {str(e)}"}

    def analyze_with_gemini(self, symbol, bid, bid_high, bid_low, reason):
        """Analisis pasar menggunakan Gemini API."""
        if not self.gemini_api_key:
            return {"error": "GEMINI_API_KEY tidak diatur"}

        prompt = (
            f"Anda adalah asisten trading crypto profesional. Berikan analisis singkat untuk simbol {symbol}.\n"
            f"Data pasar:\n"
            f"- Bid: {bid}\n"
            f"- Daily High (Swing High): {bid_high}\n"
            f"- Daily Low (Swing Low): {bid_low}\n"
            f"- Sinyal dasar: {reason}\n"
            f"- Lot size disarankan: {self.lot_size}\n\n"
            "Berikan rekomendasi BUY/SELL/HOLD dengan alasan dan level stop loss serta take profit "
            "berdasarkan swing high dan swing low. Jawab dalam bahasa Indonesia, singkat dan padat."
        )

        try:
            resp = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.gemini_api_key}",
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [
                        {
                            "parts": [{"text": prompt}]
                        }
                    ]
                },
                timeout=30,
            )
            if resp.status_code == 200:
                data = resp.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return {
                    "provider": "gemini",
                    "symbol": symbol,
                    "analysis": text,
                    "lot_size": self.lot_size,
                }
            else:
                return {"error": f"Gemini API error: {resp.status_code} {resp.text}"}
        except Exception as e:
            return {"error": f"Gemini request gagal: {str(e)}"}

    def analyze_market(self, symbol, bid, bid_high, bid_low, reason, provider="openai"):
        """Analisis pasar menggunakan AI provider yang dipilih."""
        if provider == "gemini":
            return self.analyze_with_gemini(symbol, bid, bid_high, bid_low, reason)
        else:
            return self.analyze_with_openai(symbol, bid, bid_high, bid_low, reason)


def get_ai_analysis(symbol, bid, bid_high, bid_low, reason, provider="openai"):
    """Fungsi helper untuk analisis AI."""
    ai = AIIntegration()
    return ai.analyze_market(symbol, bid, bid_high, bid_low, reason, provider)