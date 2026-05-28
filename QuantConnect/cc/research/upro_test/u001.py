from AlgorithmImports import *
class U001(QCAlgorithm):
    """60% UPRO annual rebalance — UPRO generalization of ensemble/001."""
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.upro = self.AddEquity("UPRO", Resolution.Daily).Symbol
        self.Schedule.On(self.DateRules.YearStart(self.upro),
                         self.TimeRules.AfterMarketOpen(self.upro, 30), self.R)
    def R(self):
        self.SetHoldings(self.upro, 0.6)
    def OnData(self, d): pass
