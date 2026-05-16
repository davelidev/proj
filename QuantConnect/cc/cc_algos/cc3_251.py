from AlgorithmImports import *

class Top1MegaCap_Median(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection, self.FineSelection)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.SetWarmUp(220, Resolution.Daily); self.symbols=[]
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)

    def CoarseSelection(self, coarse):
        return [x.Symbol for x in sorted(coarse, key=lambda x: x.DollarVolume, reverse=True)[:100]]
    def FineSelection(self, fine):
        self.symbols=[x.Symbol for x in sorted(fine, key=lambda x: x.MarketCap, reverse=True)[:1]]
        return self.symbols

    def Rebalance(self):
        if self.IsWarmingUp or not self.symbols: return
        top1=self.symbols[0]
        h=self.History(self.qqq, 200, Resolution.Daily)
        if h.empty or len(h)<200: return
        c=[float(x) for x in h["close"].values]; med=sorted(c)[100]
        in_trend=self.Securities[self.qqq].Price>med
        for sym in list(self.Securities.Keys):
            if sym in (self.qqq, self.bil, top1): continue
            if self.Portfolio[sym].Invested: self.Liquidate(sym)
        if in_trend:
            if self.Portfolio[self.bil].Invested: self.Liquidate(self.bil)
            self.SetHoldings(top1, 1.0)
        else:
            if self.Portfolio[top1].Invested: self.Liquidate(top1)
            if not self.Portfolio[self.bil].Invested:
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data): pass
