from AlgorithmImports import *

class RangeExpansionEntry(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(30, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq, 11, Resolution.Daily)
        if h.empty or len(h)<11: return
        prior_ranges=[float(h["high"].iloc[i])-float(h["low"].iloc[i]) for i in range(10)]
        avg_r=sum(prior_ranges)/10
        last_r=float(h["high"].iloc[-1])-float(h["low"].iloc[-1])
        last_o=float(h["open"].iloc[-1]); last_c=float(h["close"].iloc[-1])
        expansion_up = last_r > 1.5*avg_r and last_c > last_o
        # exit: close < open expansion bar OR 5 trading days timeout
        if not self.Portfolio[self.tqqq].Invested:
            if expansion_up:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq,1.0)
        else:
            # exit on close < open (red day) of a wide bar
            if last_r > 1.5*avg_r and last_c < last_o:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil,1.0)

    def OnData(self, data): pass
