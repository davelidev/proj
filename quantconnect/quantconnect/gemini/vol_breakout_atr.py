from AlgorithmImports import *

class TQQQATRTrend(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        
        self.sma = self.SMA(self.qqq, 200, Resolution.Daily)
        self.atr = self.ATR(self.tqqq, 14, MovingAverageType.Wilders, Resolution.Daily)
        
        self.trailing_stop = 0
        self.invested = False
        
        self.SetWarmUp(200)

    def OnData(self, data):
        if self.IsWarmingUp or not (self.sma.IsReady and self.atr.IsReady): return
        
        price_qqq = self.Securities[self.qqq].Price
        price_tqqq = self.Securities[self.tqqq].Price
        sma_val = self.sma.Current.Value
        atr_val = self.atr.Current.Value
        
        if not self.invested:
            if price_qqq > sma_val:
                self.Log(f"[{self.Time}] TREND UP. Entering TQQQ.")
                self.SetHoldings(self.tqqq, 1.0)
                self.trailing_stop = price_tqqq - (2.5 * atr_val)
                self.invested = True
        else:
            # Update trailing stop
            new_stop = price_tqqq - (2.5 * atr_val)
            if new_stop > self.trailing_stop:
                self.trailing_stop = new_stop
            
            # Exit if price falls below stop OR trend flips
            if price_tqqq < self.trailing_stop or price_qqq < sma_val:
                self.Log(f"[{self.Time}] EXIT. Stop: {self.trailing_stop:.2f} | Price: {price_tqqq:.2f} | Trend: {'UP' if price_qqq > sma_val else 'DOWN'}")
                self.Liquidate(self.tqqq)
                self.invested = False
                self.trailing_stop = 0
