import WebSocket from "ws";

const cc = "btcusd";
const interval = "1m";
const socket = `wss://stream.binance.com:9443/ws/${cc}t@kline_${interval}`;

const ws = new WebSocket(socket);
ws.onmessage = function (e) {
  console.log(JSON.parse(e.data));
};
