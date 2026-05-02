from AlgorithmImports import *

class TrendStretchExit(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.sma = self.SMA(self.qqq, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), 
                         self.TimeRules.AfterMarketOpen(self.qqq, 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if not self.sma.IsReady: return
        
        price = self.Securities[self.qqq].Price
        sma_val = self.sma.Current.Value
        stretch = (price - sma_val) / sma_val if sma_val > 0 else 0
        
        if not self.Portfolio[self.tqqq].Invested:
            # Entry: Bullish Trend AND NOT Overextended
            if price > sma_val and stretch < 0.15:
                self.Log(f"[{self.Time}] TREND UP. Stretch {stretch:.1%}. Entering TQQQ.")
                self.SetHoldings(self.tqqq, 1.0)
                self.Liquidate(self.bil)
        else:
            # Exit: Bearish Trend OR Overextended (Blow-off Top)
            if price < sma_val or stretch > 0.20:
                self.Log(f"[{self.Time}] EXIT. Stretch {stretch:.1%} | Trend: {'UP' if price > sma_val else 'DOWN'}")
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
