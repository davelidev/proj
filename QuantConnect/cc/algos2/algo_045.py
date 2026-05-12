from AlgorithmImports import *


class Algo045(QCAlgorithm):
    """#45 — TQQQ ↔ TLT switch by SMA200. Risk-on/risk-off rotation."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tlt  = self.AddEquity("TLT",  Resolution.Daily).Symbol
        self.sma  = self.SMA(self.qqq, 200, Resolution.Daily)
        self.SetWarmUp(220, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq),
                         self.TimeRules.AfterMarketOpen(self.tqqq, 30),
                         self.Rebalance)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma.IsReady: return
        in_trend = self.Securities[self.qqq].Price > self.sma.Current.Value
        if in_trend:
            if not self.Portfolio[self.tqqq].Invested:
                if self.Portfolio[self.tlt].Invested: self.Liquidate(self.tlt)
                self.SetHoldings(self.tqqq, 1.0)
        else:
            if not self.Portfolio[self.tlt].Invested:
                if self.Portfolio[self.tqqq].Invested: self.Liquidate(self.tqqq)
                self.SetHoldings(self.tlt, 1.0)
