from AlgorithmImports import *

class TechGoldRotation(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.ugl = self.AddEquity("UGL", Resolution.Daily).Symbol # 2x Gold
        
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
            if not self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] BULL REGIME. Rotating to TQQQ.")
                self.Liquidate(self.ugl)
                self.SetHoldings(self.tqqq, 1.0)
        else:
            if not self.Portfolio[self.ugl].Invested:
                self.Log(f"[{self.Time}] BEAR REGIME. Rotating to UGL (2x Gold).")
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.ugl, 1.0)

    def OnData(self, data):
        pass
