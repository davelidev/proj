from AlgorithmImports import *

class AroonTQQQ_MegaCapDefense(QCAlgorithm):
    """TQQQ when Aroon(25) bullish on QQQ; else Top-5 mega-cap defensive basket."""
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelection, self.FineSelection)

        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol

        self.aroon = self.AROON(self.qqq, 25, Resolution.Daily)
        self.SetWarmUp(35, Resolution.Daily)

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
        if self.IsWarmingUp or not self.aroon.IsReady:
            return
        up = self.aroon.AroonUp.Current.Value
        dn = self.aroon.AroonDown.Current.Value
        bullish = up > 70 and up > dn

        if bullish:
            for sym in list(self.Securities.Keys):
                if sym in (self.qqq, self.tqqq): continue
                if self.Portfolio[sym].Invested:
                    self.Liquidate(sym)
            if not self.Portfolio[self.tqqq].Invested:
                self.SetHoldings(self.tqqq, 1.0)
        else:
            if self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.tqqq)
            if not self.symbols: return
            target = set(self.symbols)
            for sym in list(self.Securities.Keys):
                if sym in (self.qqq, self.tqqq): continue
                if self.Portfolio[sym].Invested and sym not in target:
                    self.Liquidate(sym)
            w = 1.0 / len(self.symbols)
            for s in self.symbols:
                self.SetHoldings(s, w)

    def OnData(self, data): pass
