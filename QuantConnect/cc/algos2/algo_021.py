from AlgorithmImports import *


class Algo021(QCAlgorithm):
    """TQQQ with Hard Equity-Curve Drawdown Stop (25% from peak)."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol

        self.qqq_sma = self.SMA(self.qqq, 50, Resolution.Daily)

        self.peak_equity = 0.0
        self.in_cooldown = False

        self.SetWarmUp(60, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay(self.qqq),
            self.TimeRules.AfterMarketOpen(self.qqq, 30),
            self.Rebalance,
        )

    def Rebalance(self):
        if self.IsWarmingUp:
            return
        if not self.qqq_sma.IsReady:
            return

        equity = self.Portfolio.TotalPortfolioValue
        if equity > self.peak_equity:
            self.peak_equity = equity

        dd = 0.0 if self.peak_equity == 0 else (equity - self.peak_equity) / self.peak_equity

        if not self.in_cooldown:
            if dd <= -0.25:
                self.Liquidate()
                self.in_cooldown = True
                return
            # hold 100% TQQQ
            if not self.Portfolio[self.tqqq].Invested:
                self.SetHoldings(self.tqqq, 1.0)
        else:
            # cooldown — only re-enter when QQQ above 50d SMA
            qqq_price = self.Securities[self.qqq].Price
            if qqq_price > self.qqq_sma.Current.Value:
                self.in_cooldown = False
                self.peak_equity = equity  # reset peak on re-entry
                self.SetHoldings(self.tqqq, 1.0)
