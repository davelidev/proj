from AlgorithmImports import *

class SectorRotation(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.cyclical = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.defensive = self.AddEquity("XLU", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        
        self.Schedule.On(self.DateRules.MonthStart("SPY"), 
                         self.TimeRules.AfterMarketOpen("SPY", 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(22)

    def Rebalance(self):
        if self.IsWarmingUp: return
        
        hist = self.History([self.qqq, self.defensive], 22, Resolution.Daily)
        if hist.empty: return
        
        try:
            q_prices = hist.loc[self.qqq]['close'].values
            d_prices = hist.loc[self.defensive]['close'].values
            q_roc = (q_prices[-1] / q_prices[0]) - 1
            d_roc = (d_prices[-1] / d_prices[0]) - 1
        except:
            return
            
        if q_roc > d_roc:
            if not self.Portfolio[self.cyclical].Invested:
                self.Log(f"[{self.Time}] RISK ON (QQQ > XLU). Rotating to TQQQ.")
                self.Liquidate(self.defensive)
                self.SetHoldings(self.cyclical, 1.0)
        else:
            if not self.Portfolio[self.defensive].Invested:
                self.Log(f"[{self.Time}] RISK OFF (XLU > QQQ). Rotating to Utilities.")
                self.Liquidate(self.cyclical)
                self.SetHoldings(self.defensive, 1.0)

    def OnData(self, data):
        pass
