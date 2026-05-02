from AlgorithmImports import *

class SOXLTrend(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.soxx = self.AddEquity("SOXX", Resolution.Daily).Symbol
        self.soxl = self.AddEquity("SOXL", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.sma = self.SMA(self.soxx, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.soxx), 
                         self.TimeRules.AfterMarketOpen(self.soxx, 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if not self.sma.IsReady: return
        
        price = self.Securities[self.soxx].Price
        sma_val = self.sma.Current.Value
        
        if price > sma_val:
            if not self.Portfolio[self.soxl].Invested:
                self.Log(f"[{self.Time}] SEMIS BULLISH. Entering SOXL.")
                self.Liquidate(self.bil)
                self.SetHoldings(self.soxl, 1.0)
        else:
            if not self.Portfolio[self.bil].Invested:
                self.Log(f"[{self.Time}] SEMIS BEARISH. Moving to Cash.")
                self.Liquidate(self.soxl)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
