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

        weights = {
            "AAPL": 0.20,
            "MSFT": 0.20,
            "NVDA": 0.15,
            "GOOGL": 0.15,
            "AMZN": 0.15,
            "META": 0.10,
            "TSLA": 0.05,
        }
        self.weight_map = {}
        for t, w in weights.items():
            eq = self.AddEquity(t, Resolution.Daily)
            self.weight_map[eq.Symbol] = w

        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.atr = self.ATR(self.qqq, 14, MovingAverageType.Wilders, Resolution.Daily)

        self.regime_in = None
        self.SetWarmUp(40, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay("QQQ"),
            self.TimeRules.AfterMarketOpen("QQQ", 30),
            self.Rebalance,
        )

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
            for sym, w in self.weight_map.items():
                self.SetHoldings(sym, w)
        else:
            self.Liquidate()
