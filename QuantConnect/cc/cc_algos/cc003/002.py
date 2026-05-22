from AlgorithmImports import *

class TrendVolHybrid(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.vix = self.AddData(CBOE, "VIX", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.sma = self.SMA(self.qqq, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), 
                         self.TimeRules.AfterMarketOpen(self.qqq, 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if not (self.sma.IsReady and self.Securities.ContainsKey(self.vix)): return
        
        price_q = self.Securities[self.qqq].Price
        sma_val = self.sma.Current.Value
        vix_val = self.Securities[self.vix].Price
        
        # Signal: Trend is UP AND No Panic
        if price_q > sma_val and vix_val < 30:
            if not self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] SIGNAL ON: Trend UP + VIX Low. Entering TQQQ.")
                self.Liquidate(self.bil)
                self.SetHoldings(self.tqqq, 1.0)
        else:
            if self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] SIGNAL OFF: Trend DOWN or VIX Panic. Exiting.")
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
