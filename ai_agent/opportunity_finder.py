"""Cari peluang trading terbaik dari analisis pasar."""
from market_analyzer import analyze_market


def find_best_opportunity():
    """Identifikasi peluang trading terbaik berdasarkan swing high/low."""
    results = analyze_market()
    opportunities = []

    for r in results:
        signal = r.get("signal", "HOLD")
        if signal in ("BUY", "SELL"):
            opportunities.append({
                "symbol": r["symbol"],
                "signal": signal,
                "bid": r.get("bid", 0),
                "bid_high": r.get("bid_high", 0),
                "bid_low": r.get("bid_low", 0),
                "reason": r.get("reason", ""),
                "lot_size": 0.01,
            })

    # Urutkan: BUY dan SELL di atas, HOLD di bawah
    opportunities.sort(key=lambda x: 0 if x["signal"] in ("BUY", "SELL") else 1)

    return opportunities[0] if opportunities else None


def get_all_opportunities():
    """Ambil semua peluang trading."""
    results = analyze_market()
    opportunities = []
    for r in results:
        signal = r.get("signal", "HOLD")
        if signal in ("BUY", "SELL"):
            opportunities.append({
                "symbol": r["symbol"],
                "signal": signal,
                "bid": r.get("bid", 0),
                "bid_high": r.get("bid_high", 0),
                "bid_low": r.get("bid_low", 0),
                "reason": r.get("reason", ""),
                "lot_size": 0.01,
            })
    return opportunities