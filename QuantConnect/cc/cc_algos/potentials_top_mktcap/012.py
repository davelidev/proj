from AlgorithmImports import *

class MktCapIBSRegime(QCAlgorithm):
    """Top-5 market cap universe: equal weight in bull trend; IBS<0.2 dip picks in bear."""
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.sma = self.SMA(self.qqq, 200, Resolution.Daily)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self._select)
        self.SetWarmUp(252, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq, 45), self.Rebalance)
        self._syms = set()

    def _select(self, fundamental):
        elig = [f for f in fundamental if f.HasFundamentalData and f.MarketCap > 0 and f.Price > 5]
        elig.sort(key=lambda f: f.MarketCap, reverse=True)
        self._syms = {f.Symbol for f in elig[:5]}
        return list(self._syms)

    def OnSecuritiesChanged(self, changes):
        for sec in changes.RemovedSecurities:
            self.Liquidate(sec.Symbol)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma.IsReady or not self._syms: return
        syms = [s for s in self._syms if s in self.Securities]
        if not syms: return
        in_trend = self.Securities[self.qqq].Price > self.sma.Current.Value
        if in_trend:
            w = 1.0 / len(syms)
            for s in syms: self.SetHoldings(s, w)
        else:
            targets = []
            for s in syms:
                bar = self.Securities[s]
                h, l, c = bar.High, bar.Low, bar.Close
                if h > l and (c - l) / (h - l) < 0.2:
                    targets.append(s)
            if targets:
                w = 1.0 / len(targets)
                for s in targets: self.SetHoldings(s, w)
            for s in syms:
                if s not in targets and self.Portfolio[s].Invested:
                    self.Liquidate(s)
