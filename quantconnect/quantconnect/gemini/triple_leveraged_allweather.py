from AlgorithmImports import *

class LeveragedAllWeather(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.tmf = self.AddEquity("TMF", Resolution.Daily).Symbol # 3x Bonds
        self.ugl = self.AddEquity("UGL", Resolution.Daily).Symbol # 2x Gold
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.sma = self.SMA(self.qqq, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay("QQQ"), 
                         self.TimeRules.AfterMarketOpen("QQQ", 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if not self.sma.IsReady: return
        
        price_q = self.Securities[self.qqq].Price
        sma_val = self.sma.Current.Value
        
        if price_q > sma_val:
            # Bullish Trend: Diversified Leveraged Allocation
            if not self.Portfolio.Invested:
                self.Log(f"[{self.Time}] BULL REGIME. Allocating to All-Weather Basket.")
                self.Liquidate(self.bil)
                self.SetHoldings(self.tqqq, 0.33)
                self.SetHoldings(self.tmf, 0.33)
                self.SetHoldings(self.ugl, 0.34)
        else:
            # Bearish Trend: Move to Cash
            if self.Portfolio[self.tqqq].Invested or self.Portfolio[self.tmf].Invested or self.Portfolio[self.ugl].Invested:
                self.Log(f"[{self.Time}] BEAR REGIME. Moving to Cash.")
                self.Liquidate()
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
