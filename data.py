# Back testing historical data with threads

import csv
import threading
from datetime import datetime
from client import BinanceClient, Client


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
