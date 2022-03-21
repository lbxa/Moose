import dotenv from "dotenv";
import Alpaca from "@alpacahq/alpaca-trade-api";
dotenv.config();

import api from "./utils/api.js";

const alpaca = new Alpaca({
  keyId: process.env.APCA_PAPER_API_KEY,
  secretKey: process.env.APCA_PAPER_SECRET_KEY,
  paper: true,
});

const account = await alpaca.getAccount();
console.log(`dry powder: $${account.buying_power}`);

const orderData = {
  symbol: "TSLA",
  // qty: 1,
  notional: account.buying_power * 0.9, // will buy fractional shares
  side: "buy",
  type: "market",
  time_in_force: "day",
};

const res = await api.get("/query", {
  params: {
    function: "TIME_SERIES_INTRADAY",
    symbol: "IBM",
    interval: "5min",
  },
});

console.log(res.data);

// const order = await alpaca.createOrder(any);
