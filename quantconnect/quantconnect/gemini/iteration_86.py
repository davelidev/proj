from AlgorithmImports import *
import numpy as np

class AsymmetricVolTarget(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.sma = self.SMA(self.tqqq, 200, Resolution.Daily)
        self.std = self.STD(self.tqqq, 21, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay("TQQQ"), 
                         self.TimeRules.AfterMarketOpen("TQQQ", 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if self.Time.weekday() != 0: return # Mondays
        if self.IsWarmingUp or not (self.sma.IsReady and self.std.IsReady): return
        
        price = float(self.Securities[self.tqqq].Price)
        sma_val = float(self.sma.Current.Value)
        
        # Current Realized Vol
        vol = float(self.std.Current.Value) / price if price > 0 else 0
        annual_vol = vol * np.sqrt(252)
        if annual_vol == 0: return
        
        # 1. Determine Target Volatility based on Trend
        if price > sma_val:
            target_vol = 0.30 # Bullish Risk Budget
        else:
            target_vol = 0.10 # Bearish Risk Budget
            
        # 2. Calculate TQQQ Weight
        tqqq_weight = target_vol / annual_vol
        tqqq_weight = min(1.0, tqqq_weight) # Cap at 100%
        
        # 3. Execution
        self.Log(f"[{self.Time}] TREND {'UP' if price > sma_val else 'DOWN'}. Vol {annual_vol:.1%}. Target {tqqq_weight:.1%}.")
        self.SetHoldings(self.tqqq, tqqq_weight)
        self.SetHoldings(self.bil, 1.0 - tqqq_weight)

    def OnData(self, data):
        pass
