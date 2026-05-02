from AlgorithmImports import *

class MomentumAcceleration(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.roc = self.ROC(self.tqqq, 20, Resolution.Daily)
        self.roc_window = RollingWindow[float](11) # To calculate 10-day ROC of ROC
        
        self.SetWarmUp(40)

    def OnData(self, data):
        if not self.roc.IsReady: return
        
        # Update window daily
        self.roc_window.Add(self.roc.Current.Value)
        
        if self.IsWarmingUp or not self.roc_window.IsReady: return
        
        # Acceleration = ROC of ROC over 10 days
        # current_roc / previous_roc - 1
        current_roc = self.roc_window[0]
        prev_roc = self.roc_window[10]
        
        # Handle zero/small prev_roc for stability
        acceleration = (current_roc - prev_roc) if abs(prev_roc) > 0.001 else 0
        
        # 1. Trading Logic
        if not self.Portfolio[self.tqqq].Invested:
            # Entry: ROC positive AND Acceleration positive
            if current_roc > 0 and acceleration > 0:
                self.SetHoldings(self.tqqq, 1.0)
                self.Liquidate(self.bil)
        else:
            # Exit: Acceleration turns negative (slowing down)
            if acceleration < 0:
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)
