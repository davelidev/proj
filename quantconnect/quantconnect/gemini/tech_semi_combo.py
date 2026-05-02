from AlgorithmImports import *

class TechSemiCombo(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.soxl = self.AddEquity("SOXL", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.sma = self.SMA(self.qqq, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), 
                         self.TimeRules.AfterMarketOpen(self.qqq, 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if not self.sma.IsReady: return
        
        price = self.Securities[self.qqq].Price
        sma_val = self.sma.Current.Value
        
        if price > sma_val:
            if not self.Portfolio[self.tqqq].Invested or not self.Portfolio[self.soxl].Invested:
                self.Log(f"[{self.Time}] TREND UP. Allocating 50/50 TQQQ/SOXL.")
                self.Liquidate(self.bil)
                self.SetHoldings(self.tqqq, 0.5)
                self.SetHoldings(self.soxl, 0.5)
        else:
            if not self.Portfolio[self.bil].Invested:
                self.Log(f"[{self.Time}] TREND DOWN. Moving to Cash.")
                self.Liquidate(self.tqqq)
                self.Liquidate(self.soxl)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
