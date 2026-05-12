from AlgorithmImports import *


class Algo032(QCAlgorithm):
    """Mega-5 EW + RSI(14)-on-QQQ Regime Cash Gate.

    Hold Mega-5 equal-weight when QQQ RSI(14) > 50; cash otherwise.
    """

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)


        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self._Sel)
        self.rsi = self.RSI(self.qqq, 14, MovingAverageType.Wilders, Resolution.Daily)

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
        if self.IsWarmingUp or not self.rsi.IsReady:
            return

        new_regime = self.rsi.Current.Value > 50.0
        if new_regime == self.regime_in:
            return
        self.regime_in = new_regime

        if new_regime:
            w = 1.0 / len(self._universe)
            for sym in self._universe:
                self.SetHoldings(sym, w)
        else:
            self.Liquidate()
