from AlgorithmImports import *

class GracefulStepDownTQQQTop1(QCAlgorithm):
    """Aroon-25 + Donchian-200 mid 3-state with mega-cap as defense:
       BULL  → 100% TQQQ
       MIXED → 50% TQQQ + 50% Top-1 mega-cap
       BEAR  → 100% Top-1 mega-cap
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
        self.symbols = [x.Symbol for x in sorted(fine, key=lambda x: x.MarketCap, reverse=True)[:1]]
        return self.symbols

    def Rebalance(self):
        if self.IsWarmingUp or not (self.aroon.IsReady and self.hi200.IsReady and self.lo200.IsReady):
            return
        if not self.symbols: return
        top1 = self.symbols[0]
        up = self.aroon.AroonUp.Current.Value
        dn = self.aroon.AroonDown.Current.Value
        mid = (self.hi200.Current.Value + self.lo200.Current.Value) / 2.0
        price = self.Securities[self.qqq].Price
        aroon_bull = up > 70 and up > dn
        donch_bull = price > mid

        if aroon_bull and donch_bull:
            ns, weights = "BULL",  {self.tqqq: 1.0, top1: 0.0}
        elif aroon_bull or donch_bull:
            ns, weights = "MIXED", {self.tqqq: 0.5, top1: 0.5}
        else:
            ns, weights = "BEAR",  {self.tqqq: 0.0, top1: 1.0}

        if ns != self.state:
            # liquidate stale defensive (in case universe rotated)
            for sym in list(self.Securities.Keys):
                if sym in (self.qqq, self.tqqq, top1): continue
                if self.Portfolio[sym].Invested:
                    self.Liquidate(sym)
            for s, w in weights.items():
                self.SetHoldings(s, w)
            self.state = ns

    def OnData(self, data): pass
