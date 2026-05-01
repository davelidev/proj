from AlgorithmImports import *

class DefensiveRotation(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        tickers = ["SPY", "QQQ", "TQQQ", "SQQQ"]
        self.syms = {t: self.AddEquity(t, Resolution.Daily).Symbol for t in tickers}

        self.rsi2 = self.RSI(self.syms["TQQQ"], 2, MovingAverageType.Wilders, Resolution.Daily)
        self.sma200 = self.SMA(self.syms["TQQQ"], 200, Resolution.Daily)
        self.sma20 = self.SMA(self.syms["TQQQ"], 20, Resolution.Daily)

        self.SetWarmUp(200, Resolution.Daily)
        self.Schedule.On(
            self.DateRules.EveryDay("TQQQ"),
            self.TimeRules.AfterMarketOpen("TQQQ", 35),
            self.Rebalance,
        )
        self._current_pick = None

    def _pick(self):
        price = self.Securities[self.syms["TQQQ"]].Price
        sma20 = self.sma20.Current.Value
        sma200 = self.sma200.Current.Value
        r2 = self.rsi2.Current.Value
        if price > sma200:
            if price > sma20 or r2 < 20:
                return "TQQQ"
        else:
            if price < sma20 or r2 > 80:
                return "SQQQ"
        return None

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma200.IsReady or not self.sma20.IsReady or not self.rsi2.IsReady:
            return
        pick = self._pick()
        if pick == self._current_pick:
            return
        self._current_pick = pick
        if pick is None:
            self.Liquidate()
        else:
            self.SetHoldings(self.syms[pick], 1.0, liquidateExistingHoldings=True)
