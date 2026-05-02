from AlgorithmImports import *

class SMACrossTQQQ(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.sma_fast = self.SMA(self.tqqq, 50, Resolution.Daily)
        self.sma_slow = self.SMA(self.tqqq, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq), 
                         self.TimeRules.AfterMarketOpen(self.tqqq, 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if not (self.sma_fast.IsReady and self.sma_slow.IsReady): return
        
        fast = self.sma_fast.Current.Value
        slow = self.sma_slow.Current.Value
        
        if fast > slow:
            if not self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] GOLDEN CROSS (50SMA > 200SMA). Entering TQQQ.")
                self.Liquidate(self.bil)
                self.SetHoldings(self.tqqq, 1.0)
        else:
            if not self.Portfolio[self.bil].Invested:
                self.Log(f"[{self.Time}] DEATH CROSS (50SMA < 200SMA). Moving to Cash.")
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
