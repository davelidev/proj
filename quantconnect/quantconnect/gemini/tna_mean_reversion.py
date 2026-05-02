from AlgorithmImports import *

class TNAMeanReversion(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.iwm = self.AddEquity("IWM", Resolution.Daily).Symbol
        self.tna = self.AddEquity("TNA", Resolution.Daily).Symbol
        self.rsi = self.RSI(self.iwm, 2, MovingAverageType.Wilders, Resolution.Daily)
        
        self.SetWarmUp(10)

    def OnData(self, data):
        if self.IsWarmingUp or not self.rsi.IsReady: return
        
        rsi_val = self.rsi.Current.Value
        
        if rsi_val < 20:
            if not self.Portfolio[self.tna].Invested:
                self.Log(f"[{self.Time}] IWM OVERSOLD | RSI: {rsi_val:.2f}. Entering TNA.")
                self.SetHoldings(self.tna, 1.0)
        elif rsi_val > 80:
            if self.Portfolio[self.tna].Invested:
                self.Log(f"[{self.Time}] IWM OVERBOUGHT | RSI: {rsi_val:.2f}. Exiting TNA.")
                self.Liquidate(self.tna)
