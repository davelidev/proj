from AlgorithmImports import *
import math


class Algo034(QCAlgorithm):
    """Mega-7 EW + Realized-Vol Regime Cash Gate.

    Compute QQQ 20-day annualized return-vol (STD of daily log-returns * sqrt(252)).
    If vol < 25%: hold Mega-7 EW. Else: cash.
    """

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)


        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self._Sel)

        self.regime_in = None
        self.SetWarmUp(40, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay("QQQ"),
            self.TimeRules.AfterMarketOpen("QQQ", 30),
            self.Rebalance,
        )


    def _Sel(self, fundamental):
        elig = [f for f in fundamental
                if f.HasFundamentalData and f.MarketCap > 0 and f.Price > 5]
        elig.sort(key=lambda f: f.MarketCap, reverse=True)
        self._universe = [f.Symbol for f in elig[:5]]
        return self._universe

    def Rebalance(self):
        if self.IsWarmingUp:
            return

        hist = self.History(self.qqq, 22, Resolution.Daily)
        if hist is None or hist.empty:
            return
        try:
            closes = hist["close"].values
        except Exception:
            return
        if len(closes) < 22:
            return

        log_rets = []
        for i in range(1, len(closes)):
            if closes[i - 1] > 0 and closes[i] > 0:
                log_rets.append(math.log(closes[i] / closes[i - 1]))
        if len(log_rets) < 2:
            return

        mean = sum(log_rets) / len(log_rets)
        var = sum((r - mean) ** 2 for r in log_rets) / (len(log_rets) - 1)
        sd = math.sqrt(var)
        ann_vol = sd * math.sqrt(252.0)

        new_regime = ann_vol < 0.25
        if new_regime == self.regime_in:
            return
        self.regime_in = new_regime

        if new_regime:
            w = 1.0 / len(self._universe)
            for sym in self._universe:
                self.SetHoldings(sym, w)
        else:
            self.Liquidate()
