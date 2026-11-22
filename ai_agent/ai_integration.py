"""Integrasi AI dengan NVIDIA NIM untuk analisis pasar."""
import os
import json
import requests
from dotenv import load_dotenv
from config import NVIDIA_API_KEY, BRIDGE_URL, LOT_SIZE, AI_PROVIDER

load_dotenv()


class AIIntegration:
    """Kelas untuk integrasi AI dengan NVIDIA NIM."""

    def __init__(self):
        self.nvidia_api_key = NVIDIA_API_KEY
        self.bridge_url = BRIDGE_URL
        self.lot_size = LOT_SIZE
        self.ai_provider = AI_PROVIDER

    def analyze_with_nvidia_nim(self, symbol, bid, bid_high, bid_low, reason):
        """Analisis pasar menggunakan NVIDIA NIM API."""
        if not self.nvidia_api_key:
            return {"error": "NVIDIA_API_KEY tidak diatur"}

        prompt = (
            f"Anda adalah asisten trading crypto profesional. Berikan analisis singkat untuk simbol {symbol}.
"
            f"Data pasar:
"
            f"- Bid: {bid}
"
            f"- Daily High (Swing High): {bid_high}
"
            f"- Daily Low (Swing Low): {bid_low}
"
            f"- Sinyal dasar: {reason}
"
            f"- Lot size disarankan: {self.lot_size}

"
            "Berikan rekomendasi BUY/SELL/HOLD dengan alasan dan level stop loss serta take profit "
            "berdasarkan swing high dan swing low. Jawab dalam bahasa Indonesia, singkat dan padat."
        )

        try:
            resp = requests.post(
                "https://integrate.api.nvidia.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.nvidia_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "meta/llama-3.1-8b-instruct",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 300,
                    "temperature": 0.7,
                },
                timeout=30,
            )
            if resp.status_code == 200:
                data = resp.json()
                return {
                    "provider": "nvidia_nim",
                    "symbol": symbol,
                    "analysis": data["choices"][0]["message"]["content"],
                    "lot_size": self.lot_size,
                }
            else:
                return {"error": f"NVIDIA NIM API error: {resp.status_code} {resp.text}"}
        except Exception as e:
            return {"error": f"NVIDIA NIM request gagal: {str(e)}"}

    def analyze_market(self, symbol, bid, bid_high, bid_low, reason, provider=None):
        """Analisis pasar menggunakan AI provider yang dipilih."""
        provider = provider or self.ai_provider or "nvidia_nim"
        if provider == "nvidia_nim":
            return self.analyze_with_nvidia_nim(symbol, bid, bid_high, bid_low, reason)
        else:
            return {"error": f"Provider AI '{provider}' tidak didukung. Gunakan 'nvidia_nim'."}


def get_ai_analysis(symbol, bid, bid_high, bid_low, reason, provider=None):
    """Fungsi helper untuk analisis AI."""
    ai = AIIntegration()
    return ai.analyze_market(symbol, bid, bid_high, bid_low, reason, provider)