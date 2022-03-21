import axios from "axios";

axios.defaults.params = {};
axios.defaults.params["apikey"] = process.env.ALPHA_VANTAGE_API_KEY;

export default axios.create({
  baseURL: "https://www.alphavantage.co",
});
