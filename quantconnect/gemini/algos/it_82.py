from AlgorithmImports import *
import numpy as np

class AdaptiveLeverage(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        # Assets
        self.tech_3x = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bond_3x = self.AddEquity("TMF", Resolution.Daily).Symbol
        self.tech_1x = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.bond_1x = self.AddEquity("AGG", Resolution.Daily).Symbol
        
        self.Schedule.On(self.DateRules.EveryDay("TQQQ"), 
                         self.TimeRules.AfterMarketOpen("TQQQ", 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(30)

    def Rebalance(self):
        if self.Time.weekday() != 0: return # Mondays
        if self.IsWarmingUp: return
        
        hist = self.History([self.tech_1x, self.bond_1x], 30, Resolution.Daily)
        if hist.empty: return
        
        try:
            q_ret = hist.loc[self.tech_1x]['close'].pct_change().dropna()
            a_ret = hist.loc[self.bond_1x]['close'].pct_change().dropna()
            correlation = q_ret.corr(a_ret)
        except:
            correlation = 1.0
            
        if correlation < 0:
            # Hedging works: High Leverage
            self.Log(f"[{self.Time}] CORR {correlation:.2f}. Switching to 3X LEVERAGE.")
            self.SetHoldings(self.tech_3x, 0.5)
            self.SetHoldings(self.bond_3x, 0.5)
            self.Liquidate(self.tech_1x)
            self.Liquidate(self.bond_1x)
        else:
            # Hedging fails: Low Leverage
            self.Log(f"[{self.Time}] CORR {correlation:.2f}. Switching to 1X LEVERAGE.")
            self.SetHoldings(self.tech_1x, 0.5)
            self.SetHoldings(self.bond_1x, 0.5)
            self.Liquidate(self.tech_3x)
            self.Liquidate(self.bond_3x)

    def OnData(self, data):
        pass
