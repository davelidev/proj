from AlgorithmImports import *

class ZFromMedianMAD(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(120, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq, 100, Resolution.Daily)
        if h.empty or len(h)<100: return
        vals=sorted(float(x) for x in h["close"].values)
        n=len(vals); med=(vals[n//2] + vals[(n-1)//2]) / 2.0
        dev=sorted(abs(v-med) for v in vals)
        mad=(dev[n//2] + dev[(n-1)//2]) / 2.0
        if mad<=0: return
        z=(self.Securities[self.qqq].Price - med) / mad
        bull = z > 0.5  # half-MAD above median
        if bull:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq,1.0)
        else:
            if not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil,1.0)

    def OnData(self, data): pass
