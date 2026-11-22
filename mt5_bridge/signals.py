"""Analisis swing high/low dan sinyal trading."""
import MetaTrader5 as mt5


def get_daily_high_low(symbol):
    """Baca daily high (bid_high) dan daily low (bid_low) sebagai referensi swing."""
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        return None
    return {
        "symbol": symbol,
        "bid_high": getattr(tick, "bid_high", 0.0),
        "bid_low": getattr(tick, "bid_low", 0.0),
        "bid": tick.bid,
        "ask": tick.ask,
    }


def find_swing_high_low(symbol, timeframe=mt5.TIMEFRAME_D1, count=50):
    """Tentukan swing high dan swing low dari data historis harian."""
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
    if rates is None or len(rates) == 0:
        return None

    highs = [r["high"] for r in rates]
    lows = [r["low"] for r in rates]

    swing_high = max(highs)
    swing_low = min(lows)

    return {
        "symbol": symbol,
        "swing_high": swing_high,
        "swing_low": swing_low,
        "count": count,
    }


def generate_signal(symbol):
    """Hasilkan sinyal BUY/SELL/HOLD berdasarkan swing high/low."""
    daily = get_daily_high_low(symbol)
    if daily is None:
        return None

    bid = daily["bid"]
    bid_high = daily["bid_high"]
    bid_low = daily["bid_low"]

    if bid >= bid_high:
        signal = "SELL"
        reason = "Harga menyentuh atau melewati daily high (swing high resistance)"
    elif bid <= bid_low:
        signal = "BUY"
        reason = "Harga menyentuh atau di bawah daily low (swing low support)"
    else:
        signal = "HOLD"
        reason = "Harga di antara daily high dan low, tunggu breakout"

    return {
        "symbol": symbol,
        "signal": signal,
        "bid": bid,
        "bid_high": bid_high,
        "bid_low": bid_low,
        "reason": reason,
        "lot_size": 0.01,
    }