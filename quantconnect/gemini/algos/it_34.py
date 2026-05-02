from AlgorithmImports import *

class TrendRSIExit(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.sma = self.SMA(self.qqq, 200, Resolution.Daily)
        self.rsi = self.RSI(self.tqqq, 2, MovingAverageType.Wilders, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), 
                         self.TimeRules.AfterMarketOpen(self.qqq, 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if not (self.sma.IsReady and self.rsi.IsReady): return
        
        price_q = self.Securities[self.qqq].Price
        sma_val = self.sma.Current.Value
        rsi_val = self.rsi.Current.Value
        
        if not self.Portfolio[self.tqqq].Invested:
            # Entry: Trend is UP
            if price_q > sma_val:
                self.Log(f"[{self.Time}] TREND UP. Entering TQQQ.")
                self.SetHoldings(self.tqqq, 1.0)
                self.Liquidate(self.bil)
        else:
            # Exit: Overextended OR Trend Failure
            if rsi_val > 90 or price_q < sma_val:
                self.Log(f"[{self.Time}] EXIT. RSI: {rsi_val:.2f} | Trend: {'UP' if price_q > sma_val else 'DOWN'}")
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
