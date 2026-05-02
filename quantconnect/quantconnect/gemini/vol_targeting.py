from AlgorithmImports import *
import numpy as np

class VolTargeting(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.tlt = self.AddEquity("TLT", Resolution.Daily).Symbol
        
        self.target_vol = 0.20 # 20% Annual Vol Target
        
        # Schedule weekly rebalance
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq), 
                         self.TimeRules.AfterMarketOpen(self.tqqq, 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(30)

    def Rebalance(self):
        if self.Time.weekday() != 0: return # Mondays
        if self.IsWarmingUp: return
        
        hist = self.History(self.tqqq, 22, Resolution.Daily)
        if hist.empty: return
        
        returns = hist['close'].pct_change().dropna()
        if len(returns) < 20: return
        
        # Realized Annual Volatility
        daily_vol = np.std(returns)
        annual_vol = daily_vol * np.sqrt(252)
        
        if annual_vol == 0: return
        
        # Weight = Target Vol / Realized Vol
        tqqq_weight = self.target_vol / annual_vol
        tqqq_weight = min(1.0, tqqq_weight) # Cap at 100%
        tlt_weight = 1.0 - tqqq_weight
        
        self.Log(f"[{self.Time}] VOL TARGETING. Realized Vol: {annual_vol:.1%}. TQQQ: {tqqq_weight:.1%}. TLT: {tlt_weight:.1%}")
        self.SetHoldings(self.tqqq, tqqq_weight)
        self.SetHoldings(self.tlt, tlt_weight)

    def OnData(self, data):
        pass
