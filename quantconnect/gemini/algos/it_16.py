from AlgorithmImports import *

class VolScaledLeverage(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.vix = self.AddData(CBOE, "VIX", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.sma = self.SMA(self.qqq, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), 
                         self.TimeRules.AfterMarketOpen(self.qqq, 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if not (self.sma.IsReady and self.Securities.ContainsKey(self.vix)): return
        
        price = self.Securities[self.qqq].Price
        sma_val = self.sma.Current.Value
        vix_val = self.Securities[self.vix].Price
        
        # Binary Trend Gate
        if price < sma_val:
            target_weight = 0
        else:
            # Dynamic Vol Scaling
            if vix_val < 15: target_weight = 1.0
            elif vix_val < 20: target_weight = 0.8
            elif vix_val < 25: target_weight = 0.5
            elif vix_val < 30: target_weight = 0.2
            else: target_weight = 0
            
        current_w = self.Portfolio[self.tqqq].Quantity * self.Securities[self.tqqq].Price / self.Portfolio.TotalPortfolioValue
        
        if abs(target_weight - current_w) > 0.05:
            self.Log(f"[{self.Time}] REBALANCE: Target {target_weight:.1%} | VIX: {vix_val:.2f}")
            self.SetHoldings(self.tqqq, target_weight)
            self.SetHoldings(self.bil, 1.0 - target_weight)

    def OnData(self, data):
        pass
