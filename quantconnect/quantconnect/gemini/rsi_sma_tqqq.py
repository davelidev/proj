from AlgorithmImports import *

class RSISMATQQQ(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.rsi = self.RSI(self.tqqq, 2, MovingAverageType.Wilders, Resolution.Daily)
        self.sma = self.SMA(self.tqqq, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq), 
                         self.TimeRules.AfterMarketOpen(self.tqqq, 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if not (self.rsi.IsReady and self.sma.IsReady): return
        
        price = self.Securities[self.tqqq].Price
        sma_val = self.sma.Current.Value
        rsi_val = self.rsi.Current.Value
        
        if not self.Portfolio[self.tqqq].Invested:
            # Entry: Bull Trend AND Short-term Pullback
            if price > sma_val and rsi_val < 30:
                self.Log(f"[{self.Time}] DIP BUY. Price > SMA200 and RSI2 < 30. Entering TQQQ.")
                self.SetHoldings(self.tqqq, 1.0)
        else:
            # Exit: Bounce back OR Trend Failure
            if rsi_val > 70 or price < sma_val:
                self.Log(f"[{self.Time}] TAKE PROFIT/EXIT. RSI: {rsi_val:.2f}. Exiting TQQQ.")
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
