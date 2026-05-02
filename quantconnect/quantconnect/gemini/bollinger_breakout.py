from AlgorithmImports import *

class BollingerBreakout(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        
        self.bb = self.BB(self.qqq, 20, 2, MovingAverageType.Simple, Resolution.Daily)
        self.sma = self.SMA(self.qqq, 200, Resolution.Daily)
        
        self.SetWarmUp(200)

    def OnData(self, data):
        if self.IsWarmingUp or not (self.bb.IsReady and self.sma.IsReady): return
        
        price = self.Securities[self.qqq].Price
        upper = self.bb.UpperBand.Current.Value
        middle = self.bb.MiddleBand.Current.Value
        sma_val = self.sma.Current.Value
        
        if not self.Portfolio[self.tqqq].Invested:
            # Entry: Breakout Above Upper Band AND Trend is UP
            if price > upper and price > sma_val:
                self.Log(f"[{self.Time}] BREAKOUT. Entering TQQQ.")
                self.SetHoldings(self.tqqq, 1.0)
        else:
            # Exit: Fall back to Middle Band OR Trend turns BEARISH
            if price < middle or price < sma_val:
                self.Log(f"[{self.Time}] BREAKDOWN. Exiting TQQQ.")
                self.Liquidate(self.tqqq)
