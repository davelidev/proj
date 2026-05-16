from AlgorithmImports import *

class ThreeState_VIXBands(QCAlgorithm):
    """3-state by VIX bands: <20 bull, 20-30 mixed, >30 bear."""
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil  = self.AddEquity("BIL",  Resolution.Daily).Symbol
        self.vix  = self.AddData(CBOE, "VIX", Resolution.Daily).Symbol
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Rebalance)
        self.state = None

    def Rebalance(self):
        if not self.Securities.ContainsKey(self.vix):
            return
        v = self.Securities[self.vix].Price
        if v <= 0: return
        if v < 20: ns, wt, wb = "BULL", 1.0, 0.0
        elif v < 30: ns, wt, wb = "MIXED", 0.5, 0.5
        else: ns, wt, wb = "BEAR", 0.0, 1.0
        if ns != self.state:
            self.SetHoldings(self.tqqq, wt)
            self.SetHoldings(self.bil, wb)
            self.state = ns

    def OnData(self, data): pass
