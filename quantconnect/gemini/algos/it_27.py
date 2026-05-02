from AlgorithmImports import *

class MACDLeveraged(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.macd = self.MACD(self.tqqq, 12, 26, 9, MovingAverageType.Exponential, Resolution.Daily)
        self.sma = self.SMA(self.qqq, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq), 
                         self.TimeRules.AfterMarketOpen(self.tqqq, 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if not (self.macd.IsReady and self.sma.IsReady): return
        
        price_q = self.Securities[self.qqq].Price
        sma_val = self.sma.Current.Value
        macd_val = self.macd.Current.Value
        signal_val = self.macd.Signal.Current.Value
        
        # Bullish: Trend UP AND MACD > Signal (Positive Momentum)
        if price_q > sma_val and macd_val > signal_val:
            if not self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] MACD CROSS UP. Entering TQQQ.")
                self.Liquidate(self.bil)
                self.SetHoldings(self.tqqq, 1.0)
        # Bearish: Trend DOWN OR MACD < Signal (Momentum Stall)
        elif price_q < sma_val or macd_val < signal_val:
            if self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] MACD CROSS DOWN. Exiting.")
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
