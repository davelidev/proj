from AlgorithmImports import *
import numpy as np

class VolCompressionTrend(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.sma = self.SMA(self.tqqq, 200, Resolution.Daily)
        self.std_short = self.STD(self.tqqq, 10, Resolution.Daily)
        self.std_long = self.STD(self.tqqq, 60, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay("TQQQ"), 
                         self.TimeRules.AfterMarketOpen("TQQQ", 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if self.Time.weekday() != 0: return # Mondays
        if self.IsWarmingUp or not (self.sma.IsReady and self.std_short.IsReady and self.std_long.IsReady): return
        
        price = float(self.Securities[self.tqqq].Price)
        sma_val = float(self.sma.Current.Value)
        
        # Volatility Ratio: Short / Long
        vol_ratio = self.std_short.Current.Value / self.std_long.Current.Value if self.std_long.Current.Value > 0 else 1.0
        
        if self.IsWarmingUp: return

        # Signal: Trend UP AND Volatility COMPRESSING (Ratio < 0.9)
        if price > sma_val and vol_ratio < 0.9:
            if not self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] SIGNAL ON: Trend UP + Vol Ratio {vol_ratio:.2f}. Entering.")
                self.SetHoldings(self.tqqq, 1.0)
                self.Liquidate(self.bil)
        else:
            # Slower exit to avoid noise
            if price < sma_val or vol_ratio > 1.2:
                if self.Portfolio[self.tqqq].Invested:
                    self.Log(f"[{self.Time}] SIGNAL OFF: Trend DOWN or Vol Spike {vol_ratio:.2f}. Exiting.")
                    self.Liquidate(self.tqqq)
                    self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
