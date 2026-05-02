from AlgorithmImports import *

class BBTrendReversion(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        
        self.bb = self.BB(self.tqqq, 20, 2, MovingAverageType.Simple, Resolution.Daily)
        self.sma = self.SMA(self.qqq, 200, Resolution.Daily)
        
        self.SetWarmUp(200)

    def OnData(self, data):
        if not (self.bb.IsReady and self.sma.IsReady): return
        
        price = self.Securities[self.tqqq].Price
        q_price = self.Securities[self.qqq].Price
        sma_val = self.sma.Current.Value
        lower = self.bb.LowerBand.Current.Value
        upper = self.bb.UpperBand.Current.Value
        
        if self.IsWarmingUp: return

        if not self.Portfolio[self.tqqq].Invested:
            # Entry: Touch Lower Band AND Trend is Bullish
            if price <= lower and q_price > sma_val:
                self.SetHoldings(self.tqqq, 1.0)
        else:
            # Exit: Touch Upper Band OR Trend turns Bearish
            if price >= upper or q_price < sma_val:
                self.Liquidate(self.tqqq)
