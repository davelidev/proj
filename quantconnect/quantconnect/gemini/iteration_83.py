from AlgorithmImports import *
import numpy as np

class VolCappedTrend(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.sma = self.SMA(self.qqq, 200, Resolution.Daily)
        self.std = self.STD(self.tqqq, 21, Resolution.Daily)
        
        self.vol_cap = 0.50 # 50% Annual Vol Cap
        
        self.Schedule.On(self.DateRules.EveryDay("QQQ"), 
                         self.TimeRules.AfterMarketOpen("QQQ", 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if not (self.sma.IsReady and self.std.IsReady): return
        
        price_q = float(self.Securities[self.qqq].Price)
        price_t = float(self.Securities[self.tqqq].Price)
        sma_val = float(self.sma.Current.Value)
        
        # Realized Annual Vol
        vol = float(self.std.Current.Value) / price_t if price_t > 0 else 0
        annual_vol = vol * np.sqrt(252)
        
        if self.IsWarmingUp: return

        # Signal: Trend UP AND Volatility BELOW CAP
        if price_q > sma_val and annual_vol < self.vol_cap:
            if not self.Portfolio[self.tqqq].Invested:
                self.SetHoldings(self.tqqq, 1.0)
                self.Liquidate(self.bil)
        else:
            if self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
