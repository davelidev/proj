from AlgorithmImports import *
import numpy as np

class SectorArb(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.soxl = self.AddEquity("SOXL", Resolution.Daily).Symbol
        
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq), 
                         self.TimeRules.AfterMarketOpen(self.tqqq, 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(30)

    def Rebalance(self):
        if self.Time.weekday() != 0: return # Mondays
        if self.IsWarmingUp: return
        
        hist = self.History([self.tqqq, self.soxl], 22, Resolution.Daily)
        if hist.empty: return
        
        try:
            t_ret = hist.loc[self.tqqq]['close'].pct_change().dropna()
            s_ret = hist.loc[self.soxl]['close'].pct_change().dropna()
            correlation = t_ret.corr(s_ret)
        except:
            return
            
        if correlation > 0.85:
            # High correlation, check for divergence
            t_total_ret = (hist.loc[self.tqqq]['close'][-1] / hist.loc[self.tqqq]['close'][0]) - 1
            s_total_ret = (hist.loc[self.soxl]['close'][-1] / hist.loc[self.soxl]['close'][0]) - 1
            
            diff = t_total_ret - s_total_ret
            
            if diff > 0.05:
                # TQQQ lead, SOXL laggard: Short leader, Long laggard
                self.SetHoldings(self.tqqq, -0.5)
                self.SetHoldings(self.soxl, 0.5)
            elif diff < -0.05:
                # SOXL lead, TQQQ laggard: Long leader, Short laggard
                self.SetHoldings(self.tqqq, 0.5)
                self.SetHoldings(self.soxl, -0.5)
            elif abs(diff) < 0.01:
                # Convergence reached
                self.Liquidate()
        else:
            # Correlation broke down
            self.Liquidate()

    def OnData(self, data):
        pass
