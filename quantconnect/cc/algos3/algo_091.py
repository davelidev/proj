from AlgorithmImports import *

class Algo091(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.symbol = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.rsi = self.RSI(self.symbol, 2, MovingAverageType.Simple, Resolution.Daily)
        
    def OnData(self, data):
        if not self.rsi.IsReady:
            return
        
        rsi_value = self.rsi.Current.Value
        
        if rsi_value < 30 and not self.Portfolio.Invested:
            self.SetHoldings(self.symbol, 1.0)
        elif rsi_value > 70 and self.Portfolio.Invested:
            self.Liquidate(self.symbol)