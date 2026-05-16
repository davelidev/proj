from AlgorithmImports import *

class InsideDayBreakout(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.lo10=self.MIN(self.qqq,10,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(20, Resolution.Daily)
        self.inside_high=None
        self.inside_low=None
        self.armed_days=0

    def Rebalance(self):
        if self.IsWarmingUp or not self.lo10.IsReady: return
        h=self.History(self.qqq, 2, Resolution.Daily)
        if h.empty or len(h)<2: return
        ph=float(h["high"].iloc[0]); pl=float(h["low"].iloc[0])
        ch=float(h["high"].iloc[1]); cl=float(h["low"].iloc[1])
        if ch < ph and cl > pl:
            self.inside_high = ch
            self.inside_low = cl
            self.armed_days = 3
        if self.inside_high is None: return
        price = self.Securities[self.qqq].Price
        if not self.Portfolio[self.tqqq].Invested:
            if price > self.inside_high and self.armed_days > 0:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq, 1.0)
        else:
            if price <= self.lo10.Current.Value*1.001:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil, 1.0)
        self.armed_days = max(0, self.armed_days - 1)

    def OnData(self, data): pass
