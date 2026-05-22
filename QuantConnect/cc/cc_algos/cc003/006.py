# TqqqIbs_25_90_sma200
from AlgorithmImports import *


class TqqqIbs_25_90_sma200(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.sym = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.sma = self.SMA(self.qqq, 200, Resolution.Daily)
        self.SetWarmUp(210, Resolution.Daily)
        self.Schedule.On(
            self.DateRules.EveryDay(self.qqq),
            self.TimeRules.BeforeMarketClose(self.qqq, 10),
            self.Rebalance,
        )

    def _ibs(self):
        bars = self.History(self.qqq, 1, Resolution.Daily)
        if bars.empty:
            return None
        h, l, c = bars.iloc[-1][["high", "low", "close"]]
        if h == l:
            return 0.5
        return (c - l) / (h - l)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma.IsReady:
            return
        price = self.Securities[self.qqq].Price
        bull = price > self.sma.Current.Value
        ibs = self._ibs()
        if ibs is None:
            return
        if not self.Portfolio.Invested:
            if bull and ibs < 0.25:
                self.SetHoldings(self.sym, 1.0)
        else:
            if ibs > 0.9 or price < self.sma.Current.Value:
                self.Liquidate(self.sym)
