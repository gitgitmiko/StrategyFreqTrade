# --- Do not remove these libs ---
from freqtrade.strategy import IStrategy
from typing import Dict, List
from functools import reduce
from pandas import DataFrame
# --------------------------------

import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
import numpy # noqa

class StrategyHBAR(IStrategy):
    """
    Trading strategy for HBAR/USDT Spot
    - Uses EMA and RSI indicators
    - Aims for 2% profit per trade
    """

    INTERFACE_VERSION: int = 3

    # Minimal ROI (target profit 2%)
    minimal_roi = {
        "0": 0.02  # 2% target profit
    }

    # Stop-loss (jika harga turun lebih dari -3%, cut loss)
    stoploss = -0.03

    # Timeframe (gunakan timeframe 5 menit)
    timeframe = '5m'

    # Indikator utama
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Exponential Moving Averages (EMA)
        dataframe['ema10'] = ta.EMA(dataframe, timeperiod=10)
        dataframe['ema50'] = ta.EMA(dataframe, timeperiod=50)

        # Relative Strength Index (RSI)
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        return dataframe

    # Sinyal Entry (Beli)
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['close'] > dataframe['ema10']) &  # Harga breakout dari EMA10
                (dataframe['ema10'] > dataframe['ema50']) &  # EMA10 > EMA50 (tren naik)
                (dataframe['rsi'] < 30)  # RSI rendah (oversold)
            ),
            'enter_long'] = 1
        return dataframe

    # Sinyal Exit (Jual)
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['rsi'] > 70)  # RSI tinggi (overbought)
            ),
            'exit_long'] = 1
        return dataframe
