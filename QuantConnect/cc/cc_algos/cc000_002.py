from AlgorithmImports import *


class Algo002(QCAlgorithm):
    """ — Top-5 tech by market cap; RSI(2) < 30 dip entry above SMA(50); 15% stop or 1yr-ATH exit. Monday only."""

    SLOT_W = 0.20

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.Settings.AutomaticIndicatorWarmUp = True
        self.Settings.SeedInitialPrices = True

        self._qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol  # anchor for scheduler
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self._select_tech)
        self.SetWarmUp(252, Resolution.Daily)

        self._ind = {}  # sym -> {rsi, max, sma50}

        self.Schedule.On(
            self.DateRules.Every(DayOfWeek.Monday),
            self.TimeRules.AfterMarketOpen(self._qqq, 30),
            self.Rebalance,
        )

    def _select_tech(self, fundamental):
        filtered = [
            f for f in fundamental
            if f.HasFundamentalData
            and f.AssetClassification.MorningstarSectorCode == MorningstarSectorCode.Technology
        ]
        return [f.Symbol for f in sorted(filtered, key=lambda f: f.MarketCap)[-5:]]

    def OnSecuritiesChanged(self, changes):
        for sec in changes.AddedSecurities:
            sym = sec.Symbol
            self._ind[sym] = {
                "rsi":   self.RSI(sym, 2),
                "max":   self.MAX(sym, 252),
                "sma50": self.SMA(sym, 50),
            }
        for sec in changes.RemovedSecurities:
            sym = sec.Symbol
            self._ind.pop(sym, None)
            if self.Portfolio[sym].Invested:
                self.Liquidate(sym)

    def Rebalance(self):
        if self.IsWarmingUp: return

        total = self.Portfolio.TotalPortfolioValue

        for sym, ind in list(self._ind.items()):
            if not self.Portfolio[sym].Invested: continue
            if not (ind["max"].IsReady and ind["sma50"].IsReady): continue
            price = self.Securities[sym].Price
            if price <= self.Portfolio[sym].AveragePrice * 0.85 or price >= ind["max"].Current.Value:
                self.Liquidate(sym)

        invested_w = sum(
            self.Portfolio[s].HoldingsValue / total
            for s in self._ind if self.Portfolio[s].Invested
        ) if total > 0 else 0
        budget = max(0.0, 1.0 - invested_w)

        for sym, ind in self._ind.items():
            if self.Portfolio[sym].Invested or budget < 0.005: continue
            if not (ind["max"].IsReady and ind["sma50"].IsReady): continue
            price = self.Securities[sym].Price
            if ind["rsi"].Current.Value < 30 and price > ind["sma50"].Current.Value:
                entry_w = min(self.SLOT_W, budget)
                self.SetHoldings(sym, entry_w)
                budget -= entry_w

    def OnData(self, data): pass
