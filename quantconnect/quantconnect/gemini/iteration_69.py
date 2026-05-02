from AlgorithmImports import *

class BearMarketBounce(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.Schedule.On(self.DateRules.MonthStart("TQQQ"), 
                         self.TimeRules.AfterMarketOpen("TQQQ", 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(252)

    def Rebalance(self):
        if self.IsWarmingUp: return
        
        hist = self.History(self.tqqq, 253, Resolution.Daily)
        if hist.empty or len(hist) < 252: return
        
        prices = hist['close'].values
        ret12m = (prices[-1] / prices[0]) - 1
        ret1m = (prices[-1] / prices[-22]) - 1
        
        if not self.Portfolio[self.tqqq].Invested:
            # Entry: 12m trend is negative (cyclical low) AND 1m is positive (bounce)
            if ret12m < 0 and ret1m > 0:
                self.SetHoldings(self.tqqq, 1.0)
                self.Liquidate(self.bil)
        else:
            # Exit: Momentum stalls (1m < 0) OR recovery is complete (12m > 0)
            if ret1m < 0 or ret12m > 0:
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
