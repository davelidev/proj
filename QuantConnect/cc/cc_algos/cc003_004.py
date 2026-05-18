from AlgorithmImports import *

class TurnOfMonth(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil  = self.AddEquity("BIL",  Resolution.Daily).Symbol

        # Enter 2 trading days before month end, exit 4 trading days after month start.
        # Window roughly: T-2, T-1, T (last day), T+1, T+2, T+3.
        self.Schedule.On(self.DateRules.MonthEnd(self.qqq, 2),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Enter)
        self.Schedule.On(self.DateRules.MonthStart(self.qqq, 4),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Exit)

    def Enter(self):
        if not self.Portfolio[self.tqqq].Invested:
            self.Liquidate(self.bil)
            self.SetHoldings(self.tqqq, 1.0)

    def Exit(self):
        if not self.Portfolio[self.bil].Invested:
            self.Liquidate(self.tqqq)
            self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
