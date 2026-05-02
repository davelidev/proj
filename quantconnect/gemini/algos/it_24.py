from AlgorithmImports import *

class ExtremeRSIDip(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.rsi = self.RSI(self.qqq, 2, MovingAverageType.Wilders, Resolution.Daily)
        
        self.SetWarmUp(10)

    def OnData(self, data):
        if self.IsWarmingUp or not self.rsi.IsReady: return
        
        rsi_val = self.rsi.Current.Value
        
        # Entry: Extreme Oversold
        if rsi_val < 15:
            if not self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] EXTREME OVERSOLD | RSI: {rsi_val:.2f}. Entering TQQQ.")
                self.SetHoldings(self.tqqq, 1.0)
        
        # Exit: Early Recovery
        elif rsi_val > 70:
            if self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] RECOVERY | RSI: {rsi_val:.2f}. Exiting TQQQ.")
                self.Liquidate(self.tqqq)
