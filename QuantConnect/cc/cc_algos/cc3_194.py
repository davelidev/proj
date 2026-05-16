from AlgorithmImports import *

class VIXSpikeFade(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.vix=self.AddData(CBOE, "VIX", Resolution.Daily).Symbol
        self.aroon=self.AROON(self.qqq, 25, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(35, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp or not self.aroon.IsReady or not self.Securities.ContainsKey(self.vix): return
        h=self.History(self.vix, 5, Resolution.Daily)
        if h.empty or len(h)<5: return
        v=[float(x) for x in h["value"].values]
        was_spike = max(v[:3]) > 30
        falling = v[-1] < v[-2]
        regime = self.aroon.AroonUp.Current.Value > self.aroon.AroonDown.Current.Value
        if not self.Portfolio[self.tqqq].Invested:
            if was_spike and falling and regime:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq, 1.0)
        else:
            if v[-1] < 15:  # vol normalized
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil, 1.0)

    def OnData(self, data): pass
