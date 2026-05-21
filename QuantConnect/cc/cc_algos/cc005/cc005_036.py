from AlgorithmImports import *

class FiveStateTQQQTop1(QCAlgorithm):
    """5-state with 3 filters (ROC20, D100, D200) + Top-1 mega-cap fill:
       n bull / out of 3 maps to (TQQQ, Top1) weights:
       3 → 100% TQQQ
       2 → 70% TQQQ + 30% Top-1
       1 → 30% TQQQ + 70% Top-1
       0 → 0% TQQQ + 100% Top-1 (no BIL — keep equity exposure on small bears)
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
        self.hi100 = self.MAX(self.qqq, 100, Resolution.Daily)
        self.lo100 = self.MIN(self.qqq, 100, Resolution.Daily)
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
        if self.IsWarmingUp or not (self.roc.IsReady and self.hi100.IsReady and self.lo100.IsReady
                                    and self.hi200.IsReady and self.lo200.IsReady):
            return
        if not self.symbols: return
        top1 = self.symbols[0]
        mid100 = (self.hi100.Current.Value + self.lo100.Current.Value) / 2.0
        mid200 = (self.hi200.Current.Value + self.lo200.Current.Value) / 2.0
        price = self.Securities[self.qqq].Price
        n = int(self.roc.Current.Value > 0) + int(price > mid100) + int(price > mid200)
        plan = {3: (1.0, 0.0), 2: (0.7, 0.3), 1: (0.3, 0.7), 0: (0.0, 1.0)}
        wt, wm = plan[n]
        if n != self.state:
            for sym in list(self.Securities.Keys):
                if sym in (self.qqq, self.tqqq, top1): continue
                if self.Portfolio[sym].Invested: self.Liquidate(sym)
            self.SetHoldings(self.tqqq, wt)
            self.SetHoldings(top1, wm)
            self.state = n

    def OnData(self, data): pass
