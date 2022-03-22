import asyncio
import json
import websockets

cc = "btcusd"
interval = "1m"
socket = f"wss://stream.binance.com:9443/ws/{cc}t@kline_{interval}"
print(socket)


ws = websockets.connect("wss://stream.binance.com:9443/ws/{cc}t@kline_{interval}")
print(ws)
