from AlgorithmImports import *

class UltraLeveragedRotation(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.assets = ["TQQQ", "SOXL", "TNA"]
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.symbols = {}
        for ticker in self.assets:
            self.symbols[ticker] = self.AddEquity(ticker, Resolution.Daily).Symbol
            
        self.sma = self.SMA(self.qqq, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.MonthStart("QQQ"), 
                         self.TimeRules.AfterMarketOpen("QQQ", 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma.IsReady: return
        
        price_qqq = self.Securities[self.qqq].Price
        sma_val = self.sma.Current.Value
        
        if price_qqq < sma_val:
            self.Log(f"[{self.Time}] MARKET BEARISH. Moving to Cash.")
            self.Liquidate()
            self.SetHoldings(self.bil, 1.0)
            return
            
        # Market Bullish, pick best 3x ETF by 3-month momentum
        hist = self.History(list(self.symbols.values()), 64, Resolution.Daily)
        if hist.empty: return
        
        momentum_scores = {}
        for ticker, symbol in self.symbols.items():
            if symbol in hist.index.get_level_values(0):
                prices = hist.loc[symbol]['close'].values
                momentum_scores[ticker] = (prices[-1] / prices[0]) - 1
        
        if not momentum_scores: return
        
        best_ticker = max(momentum_scores, key=momentum_scores.get)
        self.Log(f"[{self.Time}] ROTATING TO LEADER: {best_ticker} (3m ROC: {momentum_scores[best_ticker]:.1%})")
        
        if not self.Portfolio[self.symbols[best_ticker]].Invested:
            self.SetHoldings(self.symbols[best_ticker], 1.0)
            for t in self.assets:
                if t != best_ticker: self.Liquidate(self.symbols[t])
            self.Liquidate(self.bil)

    def OnData(self, data):
        pass
