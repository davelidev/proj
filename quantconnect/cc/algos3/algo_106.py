from AlgorithmImports import *

class Algo106(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.symbol = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        
        self.rsi = self.RSI(self.symbol, 14, MovingAverageType.Wilders, Resolution.Daily)
        self.sma = self.SMA(self.symbol, 50, Resolution.Daily)
        
        self.SetWarmUp(50)

    def OnData(self, data):
        if self.IsWarmingUp:
            return
        
        if not data.ContainsKey(self.symbol):
            return
        
        rsi_value = self.rsi.Current.Value
        sma_value = self.sma.Current.Value
        close = data[self.symbol].Close
        
        if rsi_value > 50 and close > sma_value:
            self.SetHoldings(self.symbol, 1.0)
        else:
            self.SetHoldings(self.symbol, 0)