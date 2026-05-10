class Algo101(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.AddEquity("TQQQ", Resolution.Daily)
        self.bb = BollingerBands(20, 2, MovingAverageType.Simple)
        self.RegisterIndicator("TQQQ", self.bb, Resolution.Daily)

    def OnData(self, data):
        if not self.bb.IsReady:
            return
        security = self.Securities["TQQQ"]
        price = security.Close
        lower = self.bb.LowerBand.Current.Value
        upper = self.bb.UpperBand.Current.Value
        if upper == lower:
            return
        percentB = (price - lower) / (upper - lower)
        if percentB < 0.2 and not self.Portfolio["TQQQ"].Invested:
            self.SetHoldings("TQQQ", 1.0)
        elif percentB > 0.8 and self.Portfolio["TQQQ"].Invested:
            self.Liquidate("TQQQ")