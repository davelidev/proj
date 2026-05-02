from AlgorithmImports import *

class TQQQSMA50(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.sma = self.SMA(self.tqqq, 50, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq), 
                         self.TimeRules.AfterMarketOpen(self.tqqq, 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(50)

    def Rebalance(self):
        if not self.sma.IsReady: return
        
        price = self.Securities[self.tqqq].Price
        sma_val = self.sma.Current.Value
        
        if price > sma_val:
            if not self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] TREND UP (SMA50). Entering TQQQ.")
                self.Liquidate(self.bil)
                self.SetHoldings(self.tqqq, 1.0)
        else:
            if not self.Portfolio[self.bil].Invested:
                self.Log(f"[{self.Time}] TREND DOWN (SMA50). Moving to Cash.")
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
