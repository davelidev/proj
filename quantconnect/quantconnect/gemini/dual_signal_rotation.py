from AlgorithmImports import *

class DualSignalRotation(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.assets = ["TQQQ", "SOXL", "TECL"]
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.symbols = {}
        for ticker in self.assets:
            self.symbols[ticker] = self.AddEquity(ticker, Resolution.Daily).Symbol
            
        self.sma = self.SMA(self.qqq, 200, Resolution.Daily)
        self.rsi = {t: self.RSI(self.symbols[t], 14, MovingAverageType.Wilders, Resolution.Daily) for t in self.assets}
        
        # Weekly rebalance on Monday
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), 
                         self.TimeRules.AfterMarketOpen(self.qqq, 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if self.Time.weekday() != 0: return # Only Mondays
        if self.IsWarmingUp or not self.sma.IsReady: return
        
        price_qqq = self.Securities[self.qqq].Price
        sma_val = self.sma.Current.Value
        
        if price_qqq < sma_val:
            self.Log(f"[{self.Time}] TREND DOWN. Moving to Cash.")
            self.Liquidate()
            self.SetHoldings(self.bil, 1.0)
            return
            
        # Trend is UP, pick best performer by RSI
        rsi_scores = {t: self.rsi[t].Current.Value for t in self.assets if self.rsi[t].IsReady}
        if not rsi_scores: return
        
        best_ticker = max(rsi_scores, key=rsi_scores.get)
        self.Log(f"[{self.Time}] TREND UP. Rotating to {best_ticker} (RSI: {rsi_scores[best_ticker]:.2f})")
        
        if not self.Portfolio[self.symbols[best_ticker]].Invested:
            self.SetHoldings(self.symbols[best_ticker], 1.0)
            for t in self.assets:
                if t != best_ticker: self.Liquidate(self.symbols[t])
            self.Liquidate(self.bil)

    def OnData(self, data):
        pass
