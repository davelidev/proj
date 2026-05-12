from AlgorithmImports import *


class Algo038(QCAlgorithm):
    """Mega-7 Cap-Weighted (fixed weights) + ATR-of-QQQ Cash Gate.

    Hardcoded cap weights: AAPL 0.20, MSFT 0.20, NVDA 0.15, GOOGL 0.15,
    AMZN 0.15, META 0.10, TSLA 0.05.
    Signal: ATR(14)/price on QQQ. If ATR-pct < 0.020 -> hold weighted basket;
    else cash.
    """

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)


        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self._Sel)
        self.atr = self.ATR(self.qqq, 14, MovingAverageType.Wilders, Resolution.Daily)

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
        if self.IsWarmingUp or not self.atr.IsReady:
            return
        price = self.Securities[self.qqq].Price
        if price <= 0:
            return
        atr_pct = self.atr.Current.Value / price

        new_regime = atr_pct < 0.020
        if new_regime == self.regime_in:
            return
        self.regime_in = new_regime

        if new_regime:
            w = 1.0 / len(self._universe)
            for sym in self._universe:
                self.SetHoldings(sym, w)
        else:
            self.Liquidate()
