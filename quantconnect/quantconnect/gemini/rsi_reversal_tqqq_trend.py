from AlgorithmImports import *

class TQQQRSIReversalTrend(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.rsi = self.RSI(self.qqq, 2, MovingAverageType.Wilders, Resolution.Daily)
        self.sma = self.SMA(self.qqq, 200, Resolution.Daily)
        
        self.SetWarmUp(200)

    def OnData(self, data):
        if self.IsWarmingUp or not (self.rsi.IsReady and self.sma.IsReady): return
        
        rsi_val = self.rsi.Current.Value
        price = self.Securities[self.qqq].Price
        sma_val = self.sma.Current.Value
        
        # Entry: Oversold AND Trend is UP
        if rsi_val < 20 and price > sma_val:
            if not self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] TREND UP + OVERSOLD | RSI: {rsi_val:.2f}. Entering TQQQ.")
                self.SetHoldings(self.tqqq, 1.0)
        
        # Exit: Overbought OR Trend turns BEARISH
        elif rsi_val > 80 or price < sma_val:
            if self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] SIGNAL CLEAR (RSI > 80 or Price < SMA) | RSI: {rsi_val:.2f}. Exiting TQQQ.")
                self.Liquidate(self.tqqq)
