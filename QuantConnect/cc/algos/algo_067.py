from AlgorithmImports import *


class Algo067(QCAlgorithm):
    """#67 — 5 most mkt cap with 6mo momentum re-rank + SMA200 cash gate."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.sma = self.SMA(self.qqq, 200, Resolution.Daily)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.Coarse, self.Fine)
        self.SetWarmUp(160, Resolution.Daily)
        self.candidates = []
        self.Schedule.On(self.DateRules.MonthStart(),
                         self.TimeRules.At(10, 0), self.R)

    def Coarse(self, c):
        sel = [x for x in c if x.HasFundamentalData and x.Price > 5]
        sel.sort(key=lambda x: x.DollarVolume, reverse=True)
        return [x.Symbol for x in sel[:200]]

    def Fine(self, f):
        sel = [x for x in f if x.MarketCap > 5e10]
        sel.sort(key=lambda x: x.MarketCap, reverse=True)
        self.candidates = [x.Symbol for x in sel[:30]]
        return self.candidates

    def R(self):
        if self.IsWarmingUp or not self.sma.IsReady or not self.candidates: return
        in_trend = self.Securities[self.qqq].Price > self.sma.Current.Value
        if not in_trend:
            for s in list(self.Portfolio.Keys):
                if self.Portfolio[s].Invested: self.Liquidate(s)
            return
        history = self.History(self.candidates, 130, Resolution.Daily)
        if history.empty: return
        moms = {}
        for sym in self.candidates:
            try:
                if sym not in history.index.get_level_values(0): continue
                closes = history.loc[sym]['close']
                if len(closes) < 130: continue
                moms[sym] = (closes.iloc[-1] / closes.iloc[0]) - 1
            except: continue
        if not moms: return
        ranked = sorted(moms.items(), key=lambda x: x[1], reverse=True)
        top5 = [s for s, _ in ranked[:5]]
        if not top5: return
        w = 1.0 / len(top5)
        for sym in list(self.Portfolio.Keys):
            if self.Portfolio[sym].Invested and sym not in top5: self.Liquidate(sym)
        for sym in top5: self.SetHoldings(sym, w)
