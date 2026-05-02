from AlgorithmImports import *

class VolCompressionTrend(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.sma = self.SMA(self.qqq, 200, Resolution.Daily)
        self.atr = self.ATR(self.tqqq, 14, MovingAverageType.Wilders, Resolution.Daily)
        self.atr_window = RollingWindow[float](60)
        
        self.SetWarmUp(200)

    def OnData(self, data):
        if not self.atr.IsReady: return
        
        # Add to window daily
        self.atr_window.Add(self.atr.Current.Value)
        
        if self.IsWarmingUp or not (self.sma.IsReady and self.atr_window.IsReady): return
        
        price_q = self.Securities[self.qqq].Price
        sma_val = self.sma.Current.Value
        
        atr_val = self.atr.Current.Value
        min_atr = min(self.atr_window)
        
        if not self.Portfolio[self.tqqq].Invested:
            # Entry: Trend is UP AND Volatility is at a 60-day low
            if price_q > sma_val and atr_val <= min_atr:
                self.SetHoldings(self.tqqq, 1.0)
                self.Liquidate(self.bil)
        else:
            # Exit: Trend breaks
            if price_q < sma_val:
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)
