from AlgorithmImports import *

class TQQQinTrendElseMegaCap(QCAlgorithm):
    """TQQQ when QQQ > 200-day Donchian midline; else top-5 mega-cap defensive basket."""
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelection, self.FineSelection)

        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol

        self.high200 = self.MAX(self.qqq, 200, Resolution.Daily)
        self.low200  = self.MIN(self.qqq, 200, Resolution.Daily)
        self.SetWarmUp(220, Resolution.Daily)

        self.symbols = []
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Rebalance)

    def CoarseSelection(self, coarse):
        return [x.Symbol for x in sorted(coarse, key=lambda x: x.DollarVolume, reverse=True)[:100]]

    def FineSelection(self, fine):
        self.symbols = [x.Symbol for x in sorted(fine, key=lambda x: x.MarketCap, reverse=True)[:5]]
        return self.symbols

    def Rebalance(self):
        if self.IsWarmingUp or not (self.high200.IsReady and self.low200.IsReady):
            return
        midline = (self.high200.Current.Value + self.low200.Current.Value) / 2.0
        price = self.Securities[self.qqq].Price
        in_trend = price > midline

        if in_trend:
            # liquidate mega-caps, go full TQQQ
            for sym in list(self.Securities.Keys):
                if sym in (self.qqq, self.tqqq): continue
                if self.Portfolio[sym].Invested:
                    self.Liquidate(sym)
            if not self.Portfolio[self.tqqq].Invested:
                self.SetHoldings(self.tqqq, 1.0)
        else:
            # defensive: top-5 mega-caps
            if self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.tqqq)
            if not self.symbols:
                return
            target = set(self.symbols)
            for sym in list(self.Securities.Keys):
                if sym in (self.qqq, self.tqqq): continue
                if self.Portfolio[sym].Invested and sym not in target:
                    self.Liquidate(sym)
            w = 1.0 / len(self.symbols)
            for s in self.symbols:
                self.SetHoldings(s, w)

    def OnData(self, data): pass
