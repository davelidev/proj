from AlgorithmImports import *

class TrendVIXScaling(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.vix = self.AddData(CBOE, "VIX", Resolution.Daily).Symbol
        
        self.sma = self.SMA(self.qqq, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), 
                         self.TimeRules.AfterMarketOpen(self.qqq, 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if not (self.sma.IsReady and self.Securities.ContainsKey(self.vix)): return
        
        price_q = self.Securities[self.qqq].Price
        sma_val = self.sma.Current.Value
        vix_val = self.Securities[self.vix].Price
        
        # Base Trend Filter
        if price_q < sma_val:
            target_weight = 0
        else:
            # Dynamic Scaling based on VIX
            # 30 is the 'Panic' threshold. 20 is 'Normal'.
            # Weight = (30 - VIX) / 10
            target_weight = (30 - vix_val) / 10.0
            target_weight = max(0.0, min(1.0, target_weight))
            
        current_w = self.Portfolio[self.tqqq].Quantity * self.Securities[self.tqqq].Price / self.Portfolio.TotalPortfolioValue
        
        if abs(target_weight - current_w) > 0.05:
            self.Log(f"[{self.Time}] TREND UP. Scaling weight to {target_weight:.1%} (VIX: {vix_val:.2f})")
            self.SetHoldings(self.tqqq, target_weight)

    def OnData(self, data):
        pass
