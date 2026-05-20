from AlgorithmImports import *

class ThreeState_ROC20_Top1Defense(QCAlgorithm):
    """3-state ROC(20) + Donchian-200 with Top-1 mega-cap as defense:
       BULL  → 100% TQQQ
       MIXED → 50% TQQQ + 50% Top-1
       BEAR  → 100% Top-1
    """
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelection, self.FineSelection)

        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol

        self.roc   = self.ROC(self.qqq, 20, Resolution.Daily)
        self.hi200 = self.MAX(self.qqq, 200, Resolution.Daily)
        self.lo200 = self.MIN(self.qqq, 200, Resolution.Daily)
        self.SetWarmUp(220, Resolution.Daily)

        self.symbols = []
        self.state = None
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Rebalance)

    def CoarseSelection(self, coarse):
        return [x.Symbol for x in sorted(coarse, key=lambda x: x.DollarVolume, reverse=True)[:100]]

    def FineSelection(self, fine):
        self.symbols = [x.Symbol for x in sorted(fine, key=lambda x: x.MarketCap, reverse=True)[:1]]
        return self.symbols

    def Rebalance(self):
        if self.IsWarmingUp or not (self.roc.IsReady and self.hi200.IsReady and self.lo200.IsReady):
            return
        if not self.symbols: return
        top1 = self.symbols[0]
        mid = (self.hi200.Current.Value + self.lo200.Current.Value) / 2.0
        m = self.roc.Current.Value > 0
        d = self.Securities[self.qqq].Price > mid
        if m and d: ns, wt, wm = "BULL", 1.0, 0.0
        elif m or d: ns, wt, wm = "MIXED", 0.5, 0.5
        else: ns, wt, wm = "BEAR", 0.0, 1.0
        if ns != self.state:
            for sym in list(self.Securities.Keys):
                if sym in (self.qqq, self.tqqq, top1): continue
                if self.Portfolio[sym].Invested:
                    self.Liquidate(sym)
            self.SetHoldings(self.tqqq, wt)
            self.SetHoldings(top1, wm)
            self.state = ns

    def OnData(self, data): pass
