from AlgorithmImports import *


class Algo007(QCAlgorithm):
    """Antonacci Dual Momentum (GTAA-style): SPY/EFA absolute & relative momentum vs BIL."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        self.efa = self.AddEquity("EFA", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol

        self.lookback = 252  # 12 months

        self.Schedule.On(
            self.DateRules.MonthStart(self.spy),
            self.TimeRules.AfterMarketOpen(self.spy, 30),
            self.Rebalance,
        )

    def total_return(self, sym):
        hist = self.History(sym, self.lookback + 1, Resolution.Daily)
        if hist.empty or "close" not in hist.columns:
            return None
        closes = hist["close"].values
        if len(closes) < self.lookback + 1:
            return None
        return (closes[-1] / closes[0]) - 1.0

    def Rebalance(self):
        spy_r = self.total_return(self.spy)
        efa_r = self.total_return(self.efa)
        bil_r = self.total_return(self.bil)
        if spy_r is None or efa_r is None or bil_r is None:
            return

        risk_max = max(spy_r, efa_r)
        if risk_max > bil_r:
            winner = self.spy if spy_r >= efa_r else self.efa
            for sym in [self.spy, self.efa, self.bil]:
                if sym != winner and self.Portfolio[sym].Invested:
                    self.Liquidate(sym)
            self.SetHoldings(winner, 1.0)
        else:
            for sym in [self.spy, self.efa]:
                if self.Portfolio[sym].Invested:
                    self.Liquidate(sym)
            self.SetHoldings(self.bil, 1.0)
