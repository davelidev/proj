from AlgorithmImports import *


class Algo032(QCAlgorithm):
    """Mega-5 EW + RSI(14)-on-QQQ Regime Cash Gate.

    Hold Mega-5 equal-weight when QQQ RSI(14) > 50; cash otherwise.
    """

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        basket = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN"]
        self.basket_symbols = []
        for t in basket:
            eq = self.AddEquity(t, Resolution.Daily)
            self.basket_symbols.append(eq.Symbol)

        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.rsi = self.RSI(self.qqq, 14, MovingAverageType.Wilders, Resolution.Daily)

        self.regime_in = None
        self.SetWarmUp(40, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay("QQQ"),
            self.TimeRules.AfterMarketOpen("QQQ", 30),
            self.Rebalance,
        )

    def Rebalance(self):
        if self.IsWarmingUp or not self.rsi.IsReady:
            return

        new_regime = self.rsi.Current.Value > 50.0
        if new_regime == self.regime_in:
            return
        self.regime_in = new_regime

        if new_regime:
            w = 1.0 / len(self.basket_symbols)
            for sym in self.basket_symbols:
                self.SetHoldings(sym, w)
        else:
            self.Liquidate()
