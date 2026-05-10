from AlgorithmImports import *


class Algo010(QCAlgorithm):
    """#10 — QQQ SMA150 trend + RSI(2)<10 mean-reversion overlay (full TQQQ on either signal)."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.sma  = self.SMA(self.qqq, 150, Resolution.Daily)
        self.rsi  = self.RSI(self.tqqq, 2, MovingAverageType.Wilders, Resolution.Daily)
        self.SetWarmUp(170, Resolution.Daily)
        self.bar_count = 0
        self.entry_bar = None
        self.holding_mr = False
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq),
                         self.TimeRules.AfterMarketOpen(self.tqqq, 30),
                         self.Rebalance)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma.IsReady or not self.rsi.IsReady: return
        self.bar_count += 1
        in_trend = self.Securities[self.qqq].Price > self.sma.Current.Value
        invested = self.Portfolio[self.tqqq].Invested
        rsi_val  = self.rsi.Current.Value

        if in_trend:
            if not invested: self.SetHoldings(self.tqqq, 1.0)
            self.holding_mr = False
        else:
            # Below 150d SMA: only enter on RSI(2)<10 oversold dip, exit on RSI>70 or 5d
            if not invested and rsi_val < 10:
                self.SetHoldings(self.tqqq, 1.0)
                self.entry_bar = self.bar_count
                self.holding_mr = True
            elif invested and self.holding_mr:
                held = self.bar_count - (self.entry_bar or self.bar_count)
                if rsi_val > 70 or held >= 5:
                    self.Liquidate(self.tqqq)
                    self.holding_mr = False
                    self.entry_bar = None
            elif invested and not self.holding_mr:
                # Was a trend hold, regime broke -> liquidate
                self.Liquidate(self.tqqq)
