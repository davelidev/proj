from AlgorithmImports import *

class EMACrossTrend(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        
        self.ema_fast = self.EMA(self.tqqq, 9, Resolution.Daily)
        self.ema_slow = self.EMA(self.tqqq, 21, Resolution.Daily)
        self.sma_gate = self.SMA(self.qqq, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq), 
                         self.TimeRules.AfterMarketOpen(self.tqqq, 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if not (self.ema_fast.IsReady and self.ema_slow.IsReady and self.sma_gate.IsReady): return
        
        price_qqq = self.Securities[self.qqq].Price
        sma_val = self.sma_gate.Current.Value
        fast = self.ema_fast.Current.Value
        slow = self.ema_slow.Current.Value
        
        # Bullish: EMA Cross UP AND above 200 SMA
        if fast > slow and price_qqq > sma_val:
            if not self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] SIGNAL UP: 9EMA > 21EMA + Bull Gate. Entering TQQQ.")
                self.SetHoldings(self.tqqq, 1.0)
        # Bearish: EMA Cross DOWN OR below 200 SMA
        elif fast < slow or price_qqq < sma_val:
            if self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] SIGNAL DOWN: EMA Cross or Bear Gate. Exiting.")
                self.Liquidate(self.tqqq)

    def OnData(self, data):
        pass
