from AlgorithmImports import *

class TwoBarNRBreak(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.lo10=self.MIN(self.qqq,10,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(40, Resolution.Daily)
        self.brk_high=None; self.armed_days=0

    def Rebalance(self):
        if self.IsWarmingUp or not self.lo10.IsReady: return
        h=self.History(self.qqq, 20, Resolution.Daily)
        if h.empty or len(h)<20: return
        # 2-bar range = max(H[i], H[i-1]) - min(L[i], L[i-1])
        ranges=[]
        for i in range(1, 20):
            hi = max(float(h["high"].iloc[i]), float(h["high"].iloc[i-1]))
            lo = min(float(h["low"].iloc[i]),  float(h["low"].iloc[i-1]))
            ranges.append((hi-lo, hi, lo, i))
        last_range = ranges[-1]
        if last_range[0] == min(r[0] for r in ranges):
            self.brk_high = last_range[1]
            self.brk_low  = last_range[2]
            self.armed_days = 3
        if self.brk_high is None: return
        price = self.Securities[self.qqq].Price
        if not self.Portfolio[self.tqqq].Invested:
            if price > self.brk_high and self.armed_days > 0:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq, 1.0)
        else:
            if price < self.brk_low:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil, 1.0)
        self.armed_days = max(0, self.armed_days - 1)

    def OnData(self, data): pass
