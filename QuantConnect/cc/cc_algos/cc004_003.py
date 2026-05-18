from AlgorithmImports import *

class ThreeStateTQQQTop3(QCAlgorithm):
    """3-state with Top-3 mega-cap as the defensive sleeve (no cash):
       BULL  → 100% TQQQ
       MIXED → 50% TQQQ + 50% Top-3 mega-cap
       BEAR  → 100% Top-3 mega-cap
    """
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelection, self.FineSelection)

        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol

        self.aroon = self.AROON(self.qqq, 25, Resolution.Daily)
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
        self.symbols = [x.Symbol for x in sorted(fine, key=lambda x: x.MarketCap, reverse=True)[:3]]
        return self.symbols

    def Rebalance(self):
        if self.IsWarmingUp or not (self.aroon.IsReady and self.hi200.IsReady and self.lo200.IsReady):
            return
        if not self.symbols: return
        up = self.aroon.AroonUp.Current.Value
        dn = self.aroon.AroonDown.Current.Value
        mid = (self.hi200.Current.Value + self.lo200.Current.Value) / 2.0
        price = self.Securities[self.qqq].Price
        a_bull = up > 70 and up > dn
        d_bull = price > mid

        if a_bull and d_bull:
            ns, w_tqqq, w_mega = "BULL", 1.0, 0.0
        elif a_bull or d_bull:
            ns, w_tqqq, w_mega = "MIXED", 0.5, 0.5
        else:
            ns, w_tqqq, w_mega = "BEAR", 0.0, 1.0

        if ns != self.state:
            target = set(self.symbols) | {self.tqqq}
            for sym in list(self.Securities.Keys):
                if sym == self.qqq: continue
                if self.Portfolio[sym].Invested and sym not in target:
                    self.Liquidate(sym)
            self.SetHoldings(self.tqqq, w_tqqq)
            per = w_mega / len(self.symbols)
            for s in self.symbols:
                self.SetHoldings(s, per)
            self.state = ns

    def OnData(self, data): pass
