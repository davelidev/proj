from AlgorithmImports import *

class LeveragedGoldAndLongTermTreasuries(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        # Use leveraged ETFs for Gold and Long-Term Treasuries
        self.gold = self.AddEquity("UGL", Resolution.Daily).Symbol # 2x Gold
        self.bonds = self.AddEquity("TMF", Resolution.Daily).Symbol # 3x 20+ Year Treasury
        
        # Rebalance monthly on the first trading day
        self.Schedule.On(self.DateRules.MonthStart("SPY"), 
                         self.TimeRules.AfterMarketOpen("SPY", 30), 
                         self.Rebalance)

    def Rebalance(self):
        # Monthly rebalancing to 50/50 split
        self.SetHoldings(self.gold, 0.5)
        self.SetHoldings(self.bonds, 0.5)

    def OnData(self, data):
        if not self.Portfolio.Invested:
            self.SetHoldings(self.gold, 0.5)
            self.SetHoldings(self.bonds, 0.5)
