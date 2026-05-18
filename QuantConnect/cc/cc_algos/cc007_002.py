from AlgorithmImports import *

class Hammer(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.hi_ex=self.MAX(self.qqq, 10, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp or not self.hi_ex.IsReady: return
        h=self.History(self.qqq, 200, Resolution.Daily)
        if h.empty or len(h)<200: return
        c=[float(x) for x in h["close"].values]
        med=sorted(c)[100]
        in_trend = self.Securities[self.qqq].Price > med
        h2=self.History(self.qqq, 4, Resolution.Daily)
        if h2.empty or len(h2)<4: return
        opens=[float(x) for x in h2["open"].values]
        highs=[float(x) for x in h2["high"].values]
        lows=[float(x) for x in h2["low"].values]
        closes=[float(x) for x in h2["close"].values]
        bullish_signal = ((highs[-1]-lows[-1])>0) and ((min(opens[-1],closes[-1])-lows[-1]) >= 2*abs(closes[-1]-opens[-1])) and ((highs[-1]-max(opens[-1],closes[-1])) <= abs(closes[-1]-opens[-1])*0.5)
        if not self.Portfolio[self.tqqq].Invested:
            if bullish_signal and in_trend:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq, 1.0)
        else:
            if (not in_trend) or self.Securities[self.qqq].Price >= self.hi_ex.Current.Value*0.999:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil, 1.0)

    def OnData(self, data): pass
