from AlgorithmImports import *

class Connors5DayHighPullback(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.aroon=self.AROON(self.qqq, 25, Resolution.Daily)
        self.hi10=self.MAX(self.qqq, 10, Resolution.Daily)
        self.lo5=self.MIN(self.qqq, 5, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(40, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp or not (self.aroon.IsReady and self.hi10.IsReady and self.lo5.IsReady): return
        h=self.History(self.qqq, 7, Resolution.Daily)
        if h.empty or len(h)<7: return
        c=[float(x) for x in h["close"].values]
        # pattern: c[1] is 5-day high (max of past 5), c[2..5] all lower closes, c[6] up again
        if c[1] != max(c[0:6]): pass_pat=False
        else:
            pulled = all(c[i] < c[i-1] for i in range(2,6))
            today_up = c[6] > c[5]
            pass_pat = pulled and today_up
        regime_bull = self.aroon.AroonUp.Current.Value > self.aroon.AroonDown.Current.Value
        if not self.Portfolio[self.tqqq].Invested:
            if pass_pat and regime_bull:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq, 1.0)
        else:
            if self.Securities[self.qqq].Price >= self.hi10.Current.Value*0.999 or self.Securities[self.qqq].Price <= self.lo5.Current.Value*1.001:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil, 1.0)

    def OnData(self, data): pass
