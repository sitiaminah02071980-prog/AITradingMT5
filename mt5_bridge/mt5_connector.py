"""Koneksi ke MetaTrader 5 Terminal."""
import os
from dotenv import load_dotenv

load_dotenv()

MT5_LOGIN = int(os.getenv("MT5_LOGIN", "0"))
MT5_PASSWORD = os.getenv("MT5_PASSWORD", "")
MT5_SERVER = os.getenv("MT5_SERVER", "Headway-Real")


def connect_mt5():
    """Inisialisasi dan login ke MT5 terminal."""
    import MetaTrader5 as mt5

    if not mt5.initialize():
        raise RuntimeError("MT5 initialize() gagal, error code = {}".format(mt5.last_error()))

    authorized = mt5.login(login=MT5_LOGIN, password=MT5_PASSWORD, server=MT5_SERVER)
    if not authorized:
        raise RuntimeError("MT5 login gagal, error code = {}".format(mt5.last_error()))

    return mt5


def get_account_info():
    """Ambil informasi akun MT5."""
    import MetaTrader5 as mt5
    info = mt5.account_info()
    if info is None:
        return None
    return {
        "login": info.login,
        "name": info.name,
        "server": info.server,
        "balance": info.balance,
        "equity": info.equity,
        "currency": info.currency,
    }


def get_symbols(group="*"):
    """Daftar semua simbol crypto yang tersedia di MT5."""
    import MetaTrader5 as mt5
    symbols = mt5.symbols_get(group=group)
    if symbols is None:
        return []
    return [s.name for s in symbols]


def get_tick(symbol):
    """Ambil tick terbaru untuk simbol."""
    import MetaTrader5 as mt5
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        return None
    return {
        "symbol": symbol,
        "bid": tick.bid,
        "ask": tick.ask,
        "last": tick.last,
        "volume": tick.volume,
        "time": tick.time,
    }


def get_rates(symbol, timeframe, count=100):
    """Ambil data harga historis (rates) untuk simbol."""
    import MetaTrader5 as mt5
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
    if rates is None or len(rates) == 0:
        return []
    return rates.tolist()


def place_order(symbol, order_type, volume, price, sl=0.0, tp=0.0, comment="AI Trading MT5"):
    """Buka order trading di MT5."""
    import MetaTrader5 as mt5

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": 10,
        "magic": 234000,
        "comment": comment,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    return result