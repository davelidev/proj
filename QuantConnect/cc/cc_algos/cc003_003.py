from AlgorithmImports import *
import numpy as np

class VolRatioTrend(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.sma = self.SMA(self.qqq, 200, Resolution.Daily)
        self.std_short = self.STD(self.qqq, 10, Resolution.Daily)
        self.std_long = self.STD(self.qqq, 60, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), 
                         self.TimeRules.AfterMarketOpen(self.qqq, 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if not (self.sma.IsReady and self.std_short.IsReady and self.std_long.IsReady): return
        
        price_q = self.Securities[self.qqq].Price
        sma_val = self.sma.Current.Value
        ratio = self.std_short.Current.Value / self.std_long.Current.Value if self.std_long.Current.Value > 0 else 1.0
        
        # Bullish: Trend UP AND Vol is not Spiking (Ratio < 1.2)
        if price_q > sma_val and ratio < 1.2:
            if not self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] SIGNAL ON. Trend UP + Vol Ratio {ratio:.2f}. Entering TQQQ.")
                self.SetHoldings(self.tqqq, 1.0)
                self.Liquidate(self.bil)
        else:
            if self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] SIGNAL OFF. Trend DOWN or Vol Ratio {ratio:.2f}. Exiting.")
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
