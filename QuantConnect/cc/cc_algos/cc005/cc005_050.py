from AlgorithmImports import *

class ROCD200_Trail5_Top1Fill(QCAlgorithm):
    """ROC+D200 entry, 5% trail exit, Top-1 mega-cap fills 50% on exit; other 50% BIL."""
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelection, self.FineSelection)
        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil  = self.AddEquity("BIL",  Resolution.Daily).Symbol
        self.roc   = self.ROC(self.qqq, 20, Resolution.Daily)
        self.hi200 = self.MAX(self.qqq, 200, Resolution.Daily)
        self.lo200 = self.MIN(self.qqq, 200, Resolution.Daily)
        self.hi20  = self.MAX(self.qqq, 20,  Resolution.Daily)
        self.SetWarmUp(220, Resolution.Daily)
        self.symbols = []
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Rebalance)

    def CoarseSelection(self, coarse):
        return [x.Symbol for x in sorted(coarse, key=lambda x: x.DollarVolume, reverse=True)[:100]]

    def FineSelection(self, fine):
        self.symbols = [x.Symbol for x in sorted(fine, key=lambda x: x.MarketCap, reverse=True)[:1]]
        return self.symbols

    def Rebalance(self):
        if self.IsWarmingUp or not (self.roc.IsReady and self.hi200.IsReady and self.lo200.IsReady and self.hi20.IsReady):
            return
        if not self.symbols: return
        top1 = self.symbols[0]
        mid = (self.hi200.Current.Value + self.lo200.Current.Value) / 2.0
        price = self.Securities[self.qqq].Price
        dd_20 = price / self.hi20.Current.Value - 1.0
        bull = self.roc.Current.Value > 0 and price > mid and dd_20 > -0.05

        if bull:
            for sym in list(self.Securities.Keys):
                if sym in (self.qqq, self.tqqq): continue
                if self.Portfolio[sym].Invested: self.Liquidate(sym)
            self.SetHoldings(self.tqqq, 1.0)
        else:
            for sym in list(self.Securities.Keys):
                if sym in (self.qqq, self.tqqq, self.bil, top1): continue
                if self.Portfolio[sym].Invested: self.Liquidate(sym)
            if self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.tqqq)
            self.SetHoldings(top1, 0.5)
            self.SetHoldings(self.bil, 0.5)

    def OnData(self, data): pass
