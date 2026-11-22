"""Server bridge MT5 (Flask) untuk menghubungkan Android app dengan MT5 terminal."""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

from mt5_connector import connect_mt5, get_account_info, get_symbols, get_tick, get_rates, place_order
from signals import generate_signal, get_daily_high_low, find_swing_high_low
from telegram_notifier import send_signal_alert

app = Flask(__name__)
CORS(app)

mt5 = None


@app.before_first_request
def init_mt5():
    global mt5
    try:
        mt5 = connect_mt5()
        print("MT5 terhubung.")
    except Exception as e:
        print("MT5 tidak terhubung: {}".format(e))


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/account", methods=["GET"])
def account():
    info = get_account_info()
    return jsonify(info if info else {"error": "Tidak bisa ambil info akun"})


@app.route("/symbols", methods=["GET"])
def symbols():
    group = request.args.get("group", "*")
    syms = get_symbols(group=group)
    return jsonify({"symbols": syms})


@app.route("/tick/<symbol>", methods=["GET"])
def tick(symbol):
    t = get_tick(symbol)
    return jsonify(t if t else {"error": "Tidak ada data tick"})


@app.route("/daily/<symbol>", methods=["GET"])
def daily(symbol):
    d = get_daily_high_low(symbol)
    return jsonify(d if d else {"error": "Tidak ada data harian"})


@app.route("/signal/<symbol>", methods=["GET"])
def signal(symbol):
    s = generate_signal(symbol)
    if s:
        send_signal_alert(s)
    return jsonify(s if s else {"error": "Tidak bisa generate sinyal"})


@app.route("/rates/<symbol>", methods=["GET"])
def rates(symbol):
    timeframe = request.args.get("timeframe", "D1")
    count = int(request.args.get("count", "100"))
    tf_map = {
        "M1": 1, "M5": 5, "M15": 15, "H1": 16385, "H4": 16388, "D1": 16408,
    }
    tf = tf_map.get(timeframe, 16408)
    r = get_rates(symbol, tf, count)
    return jsonify({"symbol": symbol, "rates": r})


@app.route("/trade", methods=["POST"])
def trade():
    data = request.get_json()
    symbol = data.get("symbol")
    order_type = data.get("type")
    volume = float(data.get("volume", 0.01))
    price = float(data.get("price", 0))
    sl = float(data.get("sl", 0))
    tp = float(data.get("tp", 0))

    mt5_type = (
        mt5.ORDER_TYPE_BUY if order_type == "buy" else mt5.ORDER_TYPE_SELL
    ) if mt5 else None

    if not mt5 or mt5_type is None:
        return jsonify({"error": "MT5 tidak tersedia"}), 500

    result = place_order(symbol, mt5_type, volume, price, sl, tp)
    return jsonify({"result": result._asdict() if result else None})


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)