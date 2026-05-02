from AlgorithmImports import *

class AdaptiveTrend(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        
        self.sma_fast = self.SMA(self.qqq, 50, Resolution.Daily)
        self.sma_slow = self.SMA(self.qqq, 200, Resolution.Daily)
        self.std = self.STD(self.qqq, 20, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), 
                         self.TimeRules.AfterMarketOpen(self.qqq, 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if not (self.sma_fast.IsReady and self.sma_slow.IsReady and self.std.IsReady): return
        
        price = self.Securities[self.qqq].Price
        std_val = self.std.Current.Value
        
        # Adaptive Logic: High volatility -> use fast SMA, Low volatility -> use slow SMA
        # Threshold: roughly 2% daily move (252^0.5 * daily_std)
        is_volatile = std_val > (price * 0.015) 
        
        target_sma = self.sma_fast.Current.Value if is_volatile else self.sma_slow.Current.Value
        
        if price > target_sma:
            if not self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] BULLISH (Volatile: {is_volatile}). Entering TQQQ.")
                self.SetHoldings(self.tqqq, 1.0)
        else:
            if self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] BEARISH (Volatile: {is_volatile}). Exiting TQQQ.")
                self.Liquidate(self.tqqq)

    def OnData(self, data):
        pass
