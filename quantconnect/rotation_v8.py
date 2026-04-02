from datetime import datetime, timedelta
from AlgorithmImports import *

class RotationStrategyV8(QCAlgorithm):
    """
    Rotation V8: The Refined V1 Engine
    Uses the highly successful V1 macro-switching logic, but introduces a 
    1x leverage downshift during bull market pullbacks to reduce max drawdown.
    """
    def Initialize(self):
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100_000)

        self.Schedule.On(
            self.DateRules.EveryDay("QQQ"),
            self.TimeRules.AfterMarketOpen("QQQ", 35),
            self.Rebalance,
        )

        tickers = ["SPY", "QQQ", "TQQQ", "SQQQ"]
        self.syms = {t: self.AddEquity(t, Resolution.Daily).Symbol for t in tickers}

        self.rsi10 = {
            t: self.RSI(self.syms[t], 10, MovingAverageType.Wilders, Resolution.Daily)
            for t in ["SPY", "QQQ"]
        }
        self.sma_spy200 = self.SMA(self.syms["SPY"],  200, Resolution.Daily)
        self.sma_tqqq20 = self.SMA(self.syms["TQQQ"], 20,  Resolution.Daily)

        self.SetWarmUp(200, Resolution.Daily)

    def _pick(self) -> str:
        spy_price  = self.Securities[self.syms["SPY"]].Price
        tqqq_price = self.Securities[self.syms["TQQQ"]].Price

        bull = spy_price > self.sma_spy200.Current.Value
        tqqq_below_20sma = tqqq_price < self.sma_tqqq20.Current.Value
        panic = self.rsi10["QQQ"].Current.Value < 30 or self.rsi10["SPY"].Current.Value < 30

        if bull:
            if tqqq_below_20sma:
                # If there's a panic drop in a bull market, buy TQQQ to catch the snapback
                if panic:
                    return "TQQQ"
                # Otherwise, just a normal pullback, downshift to 1x QQQ to limit DD
                return "QQQ"
            return "TQQQ"
        else:
            # Bear Market Logic (from V1)
            if panic:
                return "TQQQ"
            
            if tqqq_below_20sma:
                return "SQQQ"

            return "TQQQ"

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma_spy200.IsReady or not all(i.IsReady for i in self.rsi10.values()):
            return

        pick = self._pick()
        if not self.Portfolio[self.syms[pick]].Invested:
            self.SetHoldings(self.syms[pick], 1.0, liquidateExistingHoldings=True)

    def OnData(self, data):
        pass
