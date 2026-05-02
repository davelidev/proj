from AlgorithmImports import *

class VIXTactical(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.vix = self.AddData(CBOE, "VIX", Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        # Schedule the check daily
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq), 
                         self.TimeRules.AfterMarketOpen(self.tqqq, 30), 
                         self.Rebalance)

    def Rebalance(self):
        if not self.Securities.ContainsKey(self.vix): return
        
        vix_val = self.Securities[self.vix].Price
        
        if vix_val > 25:
            if not self.Portfolio[self.bil].Invested:
                self.Log(f"[{self.Time}] PANIC (VIX > 25) | VIX: {vix_val:.2f}. Moving to Cash.")
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)
        elif vix_val < 20:
            if not self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] CALM (VIX < 20) | VIX: {vix_val:.2f}. Moving to TQQQ.")
                self.Liquidate(self.bil)
                self.SetHoldings(self.tqqq, 1.0)
        # If between 20 and 25, we hold our current position (hysteresis)

    def OnData(self, data):
        pass
