import math

import numpy as np
import pandas as pd
import pandas_ta as pta

from ta.trend import VortexIndicator
from datetime import datetime
from simple_chalk import chalk


def vortex_1(df, n):
    """Custom implementation, inspired off TradingView Pinescript example

    Args:
        df (pandas.DataFrame): market data
        n (int): period of analysis
    """
    high = df["High"]
    low = df["Low"]
    close = df["Close"]
    time = df["Open Time"]

    n = 3
    TR = pta.ATR(high, low, close)
    STR = TR.rolling(n).sum()

    for i in range(1, len(low)):
        VMP = math.fabs(high[i] - low[i - 1])
        VMM = math.fabs(low[i] - high[i - 1])
        VIP = VMP / STR[i - 1]
        VIM = VMM / STR[i - 1]

        curr_time = int(time[i]) / 1000
        curr_time = datetime.utcfromtimestamp(curr_time).strftime("%Y-%m-%d %H:%M:%S")
        if VIP > VIM:
            print(curr_time, chalk.green.bold("| buy  |"), end=" ")
        else:
            print(curr_time, chalk.red.bold("| sell |"), end=" ")

        print(f"VIP = {VIP}, VIM = {VIM}")


def vortex_2(df, n):
    """Naive implementation found on the internet. Does not output VIP and VIM values

    Args:
        df (pandas.DataFrame): market data
        n (int): period of analysis

    Returns:
        pandas.DataFrame: Vortex indicator results
    """
    i = 0
    TR = [0]
    while i < df.index[-1]:
        Range = max(df.at[i + 1, "High"], df.at[i, "Close"]) - min(df.at[i + 1, "Low"], df.at[i, "Close"])
        TR.append(Range)
        i = i + 1
    i = 0
    VM = [0]
    while i < df.index[-1]:
        Range = abs(df.at[i + 1, "High"] - df.at[i, "Low"]) - abs(df.at[i + 1, "Low"] - df.at[i, "High"])
        VM.append(Range)
        i = i + 1

    VI = pd.Series(pd.Series(VM).rolling(n).sum() / pd.Series(TR).rolling(n).sum(), name="Vortex_" + str(n))
    df = df.join(VI)
    return df


if __name__ == "__main__":

    df = pd.read_csv("data/csv/btcusd_15min.csv", sep=",")

    pandas_vtx = pta.vortex(df["High"], df["Low"], df["Close"], 3)
    ta_vtx = VortexIndicator(df["High"], df["Low"], df["Close"], 3)

    df["VTXP_3_Pandas"] = pandas_vtx["VTXP_3"]
    df["VTXM_3_Pandas"] = pandas_vtx["VTXM_3"]
    df["VTXP_3_Ta"] = ta_vtx.vortex_indicator_pos()
    df["VTXM_3_Ta"] = ta_vtx.vortex_indicator_neg()

    for idx, row in df.iterrows():
        curr_time = int(row["Open Time"]) / 1000
        curr_time = datetime.utcfromtimestamp(curr_time).strftime("%Y-%m-%d %H:%M:%S")

        if row["VTXP_3_Ta"] > row["VTXM_3_Ta"]:
            print(
                chalk.yellow("pta"),
                curr_time,
                chalk.green.bold("| buy |"),
                f'VIP = {row["VTXP_3_Pandas"]}, VIM = {row["VTXM_3_Pandas"]}',
            )
            print("ta ", curr_time, chalk.green.bold("| buy |"), f'VIP = {row["VTXP_3_Ta"]}, VIM = {row["VTXM_3_Ta"]}')
        else:
            print(
                chalk.yellow("pta"),
                curr_time,
                chalk.red.bold("| buy |"),
                f'VIP = {row["VTXP_3_Pandas"]}, VIM = {row["VTXM_3_Pandas"]}',
            )
            print("ta ", curr_time, chalk.red.bold("| buy |"), f'VIP = {row["VTXP_3_Ta"]}, VIM = {row["VTXM_3_Ta"]}')
