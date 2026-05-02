from AlgorithmImports import *

class TripleSMATrend(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.sma20 = self.SMA(self.tqqq, 20, Resolution.Daily)
        self.sma50 = self.SMA(self.tqqq, 50, Resolution.Daily)
        self.sma200 = self.SMA(self.tqqq, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq), 
                         self.TimeRules.AfterMarketOpen(self.tqqq, 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if not (self.sma20.IsReady and self.sma50.IsReady and self.sma200.IsReady): return
        
        s20 = self.sma20.Current.Value
        s50 = self.sma50.Current.Value
        s200 = self.sma200.Current.Value
        
        if not self.Portfolio[self.tqqq].Invested:
            # Entry: Perfect Bullish Alignment
            if s20 > s50 and s50 > s200:
                self.Log(f"[{self.Time}] TRIPLE TREND ALIGNED. Entering TQQQ.")
                self.SetHoldings(self.tqqq, 1.0)
                self.Liquidate(self.bil)
        else:
            # Exit: Momentum Fades (20 crosses under 50) OR Trend Fails (50 under 200)
            if s20 < s50 or s50 < s200:
                self.Log(f"[{self.Time}] TRIPLE TREND BROKEN. Exiting.")
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
