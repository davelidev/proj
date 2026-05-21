from AlgorithmImports import *

class TQQQSMATrend(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol # Cash proxy
        
        # 200-day SMA on the underlying index (QQQ)
        self.sma = self.SMA(self.qqq, 200, Resolution.Daily)
        
        # Schedule the check daily
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), 
                         self.TimeRules.AfterMarketOpen(self.qqq, 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if not self.sma.IsReady: return
        
        price = self.Securities[self.qqq].Price
        sma_val = self.sma.Current.Value
        
        if price > sma_val:
            if not self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] TREND: BULLISH (QQQ > SMA200) | Price: {price:.2f} | SMA: {sma_val:.2f}")
                self.Liquidate(self.bil)
                self.SetHoldings(self.tqqq, 1.0)
        else:
            if not self.Portfolio[self.bil].Invested:
                self.Log(f"[{self.Time}] TREND: BEARISH (QQQ < SMA200) | Price: {price:.2f} | SMA: {sma_val:.2f}")
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
