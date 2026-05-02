from AlgorithmImports import *

class SeasonalRotation(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        # Schedule rebalance monthly
        self.Schedule.On(self.DateRules.MonthStart("TQQQ"), 
                         self.TimeRules.AfterMarketOpen("TQQQ", 30), 
                         self.Rebalance)

    def Rebalance(self):
        month = self.Time.month
        
        # 'In' from November (11) to April (4)
        if month >= 11 or month <= 4:
            if not self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] SEASONAL IN. Entering TQQQ.")
                self.Liquidate(self.bil)
                self.SetHoldings(self.tqqq, 1.0)
        else:
            if not self.Portfolio[self.bil].Invested:
                self.Log(f"[{self.Time}] SEASONAL OUT. Moving to Cash.")
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
