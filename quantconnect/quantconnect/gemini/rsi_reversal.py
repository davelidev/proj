from AlgorithmImports import *

class RSIReversal(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.rsi = self.RSI(self.qqq, 2, MovingAverageType.Wilders, Resolution.Daily)
        
        self.SetWarmUp(10)

    def OnData(self, data):
        if self.IsWarmingUp or not self.rsi.IsReady: return
        
        rsi_val = self.rsi.Current.Value
        
        if rsi_val < 20:
            if not self.Portfolio[self.qqq].Invested:
                self.Log(f"[{self.Time}] OVERSOLD (RSI < 20) | RSI: {rsi_val:.2f}. Entering QQQ.")
                self.SetHoldings(self.qqq, 1.0)
        elif rsi_val > 80:
            if self.Portfolio[self.qqq].Invested:
                self.Log(f"[{self.Time}] OVERBOUGHT (RSI > 80) | RSI: {rsi_val:.2f}. Exiting QQQ.")
                self.Liquidate(self.qqq)
