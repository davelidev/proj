from AlgorithmImports import *
import numpy as np

class AdaptiveMomentum(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.roc = self.ROC(self.tqqq, 60, Resolution.Daily)
        self.std = self.STD(self.tqqq, 21, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq), 
                         self.TimeRules.AfterMarketOpen(self.tqqq, 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(60)

    def Rebalance(self):
        if not (self.roc.IsReady and self.std.IsReady): return
        
        price = float(self.Securities[self.tqqq].Price)
        mom = float(self.roc.Current.Value) / 100.0 # Convert from %
        vol = float(self.std.Current.Value) / price if price > 0 else 0
        annual_vol = vol * np.sqrt(252)
        
        # Adaptive Threshold: Bar = Volatility / 2
        # e.g. if annual vol is 60%, ROC must be > 30%
        threshold = annual_vol / 2.0
        
        if self.IsWarmingUp: return

        if not self.Portfolio[self.tqqq].Invested:
            if mom > threshold:
                self.SetHoldings(self.tqqq, 1.0)
                self.Liquidate(self.bil)
        else:
            if mom < 0: # Slower exit to allow for volatility
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
