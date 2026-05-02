from AlgorithmImports import *

class EMAVIXHybrid(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.vix = self.AddData(CBOE, "VIX", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.ema_fast = self.EMA(self.tqqq, 9, Resolution.Daily)
        self.ema_slow = self.EMA(self.tqqq, 21, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq), 
                         self.TimeRules.AfterMarketOpen(self.tqqq, 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(21)

    def Rebalance(self):
        if not (self.ema_fast.IsReady and self.ema_slow.IsReady and self.Securities.ContainsKey(self.vix)): return
        
        fast = self.ema_fast.Current.Value
        slow = self.ema_slow.Current.Value
        vix_val = self.Securities[self.vix].Price
        
        # Bullish: EMA Cross UP AND No Panic (VIX < 25)
        if fast > slow and vix_val < 25:
            if not self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] SIGNAL ON: 9/21 EMA + VIX {vix_val:.2f}. Entering TQQQ.")
                self.SetHoldings(self.tqqq, 1.0)
                self.Liquidate(self.bil)
        # Bearish: EMA Cross DOWN OR VIX Panic
        elif fast < slow or vix_val > 25:
            if self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] SIGNAL OFF. EMA Cross or VIX {vix_val:.2f}. Exiting.")
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
