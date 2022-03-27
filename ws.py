import json
import pprint
import sys
import os
import csv
import threading
import websocket


def on_open(ws):
    print("Connection opened...")


def on_close(ws):
    sys.exit()


def on_message(ws, message):
    res = json.loads(message)

    data_obj = {
        # meta data
        "event_type": res["e"],
        "event_time": res["E"],
        "symbol": res["s"],
        # market data
        "kline_start_time": res["k"]["t"],
        "kline_close_time": res["k"]["T"],
        "interval": res["k"]["i"],
        "first_trade_id": res["k"]["f"],
        "last_trade_id": res["k"]["L"],
        "open_price": res["k"]["o"],
        "close_price": res["k"]["c"],
        "high_price": res["k"]["h"],
        "low_price": res["k"]["l"],
        "base_asset_volume": res["k"]["v"],
        "number_of_trades": res["k"]["n"],
        "is_this_kline_closed": res["k"]["x"],
        "quote_asset_volume": res["k"]["q"],
        "taker_buy_base_asset_volume": res["k"]["V"],
        "taker_buy_quote_asset_volume": res["k"]["Q"],
    }

    filename = f'data/csv/{res["s"]}.csv'  # e.g. data/csv/BTCUSDT.csv
    with open(filename, "a", encoding="UTF8", newline="") as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=data_obj.keys())
        # if not os.path.isfile(filename):

        csv_writer.writerow(data_obj)

    pprint.pprint(data_obj)


def spin_ws(symbol="btcusdt", interval="1m"):
    socketAddr = f"wss://stream.binance.com:9443/ws/{symbol}@kline_{interval}"
    ws = websocket.WebSocketApp(socketAddr, on_open=on_open, on_close=on_close, on_message=on_message)
    ws.run_forever()


def get_wss_kline(symbol_list, interval):
    threads = [threading.Thread(target=spin_ws, args=[symbol, interval]) for symbol in symbol_list]
    [t.start() for t in threads]
    [t.join() for t in threads]


if __name__ == "__main__":
    symbol_list = ["btcusdt", "ethusdt"]
    get_wss_kline(symbol_list, "1m")
