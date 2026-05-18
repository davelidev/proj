from AlgorithmImports import *

class WideRangeReversal(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.hi5=self.MAX(self.qqq,5,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(20, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp or not self.hi5.IsReady: return
        h=self.History(self.qqq, 11, Resolution.Daily)
        if h.empty or len(h)<11: return
        ranges=[float(h["high"].iloc[i])-float(h["low"].iloc[i]) for i in range(11)]
        last_r=ranges[-1]
        wide_day = last_r >= max(ranges[:-1])
        last_c=float(h["close"].iloc[-1]); last_l=float(h["low"].iloc[-1]); last_h=float(h["high"].iloc[-1])
        if last_r<=0: return
        close_near_low = (last_c - last_l) / last_r < 0.25
        # buy expecting bounce
        if not self.Portfolio[self.tqqq].Invested:
            if wide_day and close_near_low:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq, 1.0)
        else:
            # exit when 5-day high made
            if self.Securities[self.qqq].Price >= self.hi5.Current.Value*0.999:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil, 1.0)

    def OnData(self, data): pass
