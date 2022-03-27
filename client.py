import os
from binance.client import Client
from dotenv import load_dotenv

load_dotenv()

BinanceClient = Client(os.environ.get("BINANCE_API_KEY"), os.environ.get("BINANCE_API_SECRET"))
