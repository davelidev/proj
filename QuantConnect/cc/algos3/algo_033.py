from AlgorithmImports import *


class Algo033(QCAlgorithm):
    """Mega-7 EW + SPY 50-day Z-Score Regime Cash Gate.

    Z = (SPY_close - SMA50) / STD50; hold Mega-7 EW when Z > 0, else cash.
    """

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)


        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self._Sel)
        self.sma50 = self.SMA(self.spy, 50, Resolution.Daily)
        self.std50 = self.STD(self.spy, 50, Resolution.Daily)

        self.regime_in = None
        self.SetWarmUp(70, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay("SPY"),
            self.TimeRules.AfterMarketOpen("SPY", 30),
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
        if not (self.sma50.IsReady and self.std50.IsReady):
            return

        price = self.Securities[self.spy].Price
        if price <= 0:
            return
        std_v = self.std50.Current.Value
        if std_v <= 0:
            return
        z = (price - self.sma50.Current.Value) / std_v

        new_regime = z > 0.0
        if new_regime == self.regime_in:
            return
        self.regime_in = new_regime

        if new_regime:
            w = 1.0 / len(self._universe)
            for sym in self._universe:
                self.SetHoldings(sym, w)
        else:
            self.Liquidate()
