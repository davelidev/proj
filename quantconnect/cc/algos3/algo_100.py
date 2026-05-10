from AlgorithmImports import *

class Algo100(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.trendWindow = 252  # one trading year
        self.SetWarmup(self.trendWindow)

    def OnData(self, data):
        if self.IsWarmingUp:
            return

        history = self.History(self.tqqq, self.trendWindow, Resolution.Daily)
        if history.empty:
            return
        
        closes = history.loc[self.tqqq]['close'].values
        if len(closes) < self.trendWindow:
            return
        
        x = np.arange(len(closes))
        slope, intercept = np.polyfit(x, closes, 1)
        
        current_price = self.Securities[self.tqqq].Price
        trendline_today = slope * len(closes) + intercept
        
        if current_price > trendline_today:
            self.SetHoldings(self.tqqq, 1.0)
        else:
            self.SetHoldings(self.tqqq, 0)