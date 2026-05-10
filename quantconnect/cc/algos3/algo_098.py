from AlgorithmImports import *

class Algo098(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        # Add TQQQ with daily resolution
        self.symbol = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        
        # 20-day simple moving average of volume
        self.volumeSma = self.SMA(self.symbol, 20, Resolution.Daily, Field.Volume)
        
        # Warm up the indicator with the required history
        self.SetWarmUp(20)
    
    def OnData(self, data):
        if self.IsWarmingUp:
            return
        
        if not self.volumeSma.IsReady:
            return
        
        if not data.ContainsKey(self.symbol):
            return
        
        bar = data[self.symbol]
        if bar is None or bar.Volume == 0:
            return
        
        currentVolume = bar.Volume
        smaVolume = self.volumeSma.Current.Value
        
        # Volume confirmation: only buy when volume > 20-day moving average
        if currentVolume > smaVolume:
            self.SetHoldings(self.symbol, 1.0)   # 100% allocation (max weight ≤ 1.0)
        else:
            self.SetHoldings(self.symbol, 0.0)   # go to cash