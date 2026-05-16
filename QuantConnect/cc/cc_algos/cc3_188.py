from AlgorithmImports import *

class ConnorsMDD4(QCAlgorithm):
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
        consecutive_down = all(c[i]<c[i-1] for i in range(1,5))
        up=self.aroon.AroonUp.Current.Value; dn=self.aroon.AroonDown.Current.Value
        regime_bull = up > dn  # weak bull regime
        if not self.Portfolio[self.tqqq].Invested:
            if consecutive_down and regime_bull:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq, 1.0)
        else:
            if self.Securities[self.qqq].Price >= self.hi5.Current.Value*0.999:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil, 1.0)

    def OnData(self, data): pass
