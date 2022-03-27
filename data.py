# Collection and storage of Market data

import json
import pprint
import sys
import websocket
import csv
import threading
from datetime import datetime
from client import BinanceClient, Client


# Web sockets
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


table_header = [
    "Open Time",
    "Open",
    "High",
    "Low",
    "Close",
    "Volume",
    "Close time",
    "Quote asset volume",
    "Number of trades",
    "Taker buy base asset volume",
    "Taker buy quote asset volume",
    "Ignore",
]


def write_csv(file, data):
    with open("data/csv/" + file, "w", encoding="UTF8", newline="") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=",")
        csv_writer.writerow(table_header)
        # format date times
        # for row in data:
        #     row[0] = datetime.utcfromtimestamp(int(row[0])).strftime("%Y-%m-%d %H:%M:%S")
        #     row[6] = datetime.utcfromtimestamp(int(row[6])).strftime("%Y-%m-%d %H:%M:%S")
        #     csv_writer.writerow(row)
        csv_writer.writerows(data)


if __name__ == "__main__":
    # (1) Websocket
    symbol_list = ["btcusdt", "ethusdt"]
    get_wss_kline(symbol_list, "1m")

    # (2) Binance client api
    start_time = datetime.now()
    btc_usd_data = BinanceClient.get_klines(symbol="BTCBUSD", interval=Client.KLINE_INTERVAL_15MINUTE)
    # historical_data = BinanceClient.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, "1 Jan, 2012", "1 Jan, 2022")

    threads = [
        threading.Thread(target=write_csv, args=["btcusd_15min.csv", btc_usd_data]),
        # threading.Thread(target=write_csv, args=["2012-2022.csv", historical_data]),
    ]

    [t.start() for t in threads]
    [t.join() for t in threads]

    end_time = datetime.now()
    exec_time = end_time - start_time
    print("exec time: ", exec_time)
