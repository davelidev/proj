from AlgorithmImports import *

class FinalLeveragedAlpha(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.sma_fast = self.SMA(self.tqqq, 50, Resolution.Daily)
        self.sma_slow = self.SMA(self.tqqq, 200, Resolution.Daily)
        self.rsi = self.RSI(self.tqqq, 2, MovingAverageType.Wilders, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq), 
                         self.TimeRules.AfterMarketOpen(self.tqqq, 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if not (self.sma_fast.IsReady and self.sma_slow.IsReady and self.rsi.IsReady): return
        
        fast = self.sma_fast.Current.Value
        slow = self.sma_slow.Current.Value
        rsi_val = self.rsi.Current.Value
        
        if not self.Portfolio[self.tqqq].Invested:
            # Entry: Golden Cross AND RSI Dip
            if fast > slow and rsi_val < 40:
                self.Log(f"[{self.Time}] SIGNAL ON: Golden Cross + RSI Dip {rsi_val:.2f}. Entering.")
                self.SetHoldings(self.tqqq, 1.0)
                self.Liquidate(self.bil)
        else:
            # Exit: Death Cross OR RSI Overextended
            if fast < slow or rsi_val > 80:
                self.Log(f"[{self.Time}] SIGNAL OFF: Cross or RSI High {rsi_val:.2f}. Exiting.")
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
