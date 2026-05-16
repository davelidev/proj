from AlgorithmImports import *

class ConnorsThreeDownOneUp(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.aroon=self.AROON(self.qqq, 25, Resolution.Daily)
        self.hi5=self.MAX(self.qqq, 5, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(40, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp or not (self.aroon.IsReady and self.hi5.IsReady): return
        h=self.History(self.qqq, 5, Resolution.Daily)
        if h.empty or len(h)<5: return
        c=[float(x) for x in h["close"].values]
        # pattern: c[0]>c[1]>c[2]>c[3] (3 down moves), then c[4]>c[3] (today up)
        three_down = c[0]>c[1] and c[1]>c[2] and c[2]>c[3]
        today_up = c[4] > c[3]
        regime_bull = self.aroon.AroonUp.Current.Value > self.aroon.AroonDown.Current.Value
        if not self.Portfolio[self.tqqq].Invested:
            if three_down and today_up and regime_bull:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq, 1.0)
        else:
            if self.Securities[self.qqq].Price >= self.hi5.Current.Value*0.999:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil, 1.0)

    def OnData(self, data): pass
