from AlgorithmImports import *


class Algo044(QCAlgorithm):
    """#44 — Trend exit also on TQQQ self-SMA (catch leveraged decay early)."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.sma_qqq  = self.SMA(self.qqq, 150, Resolution.Daily)
        self.sma_tqqq = self.SMA(self.tqqq, 100, Resolution.Daily)
        self.SetWarmUp(170, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq),
                         self.TimeRules.AfterMarketOpen(self.tqqq, 30),
                         self.Rebalance)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma_qqq.IsReady or not self.sma_tqqq.IsReady: return
        qqq_in = self.Securities[self.qqq].Price > self.sma_qqq.Current.Value
        tqqq_in = self.Securities[self.tqqq].Price > self.sma_tqqq.Current.Value
        in_trend = qqq_in and tqqq_in  # double-confirmation
        invested = self.Portfolio[self.tqqq].Invested
        if in_trend and not invested:
            self.SetHoldings(self.tqqq, 1.0)
        elif not in_trend and invested:
            self.Liquidate(self.tqqq)
