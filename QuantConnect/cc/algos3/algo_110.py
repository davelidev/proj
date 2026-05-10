class Algo110(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.AddEquity("TQQQ", Resolution.Daily)

    def OnData(self, data):
        if not data.ContainsKey("TQQQ"):
            return
        bar = data["TQQQ"]
        if bar is None:
            return
        high = bar.High
        low = bar.Low
        close = bar.Close
        day_range = high - low
        if day_range <= 0:
            self.Liquidate("TQQQ")
            return
        threshold = low + 0.75 * day_range
        if close >= threshold:
            self.SetHoldings("TQQQ", 1.0)
        else:
            self.Liquidate("TQQQ")