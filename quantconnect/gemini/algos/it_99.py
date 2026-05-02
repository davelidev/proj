from AlgorithmImports import *

class TripleLockRotation(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.assets = ["TQQQ", "SOXL"]
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.symbols = {}
        for ticker in self.assets:
            self.symbols[ticker] = self.AddEquity(ticker, Resolution.Daily).Symbol
            
        self.sma_qqq = self.SMA(self.qqq, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.MonthStart("QQQ"), 
                         self.TimeRules.AfterMarketOpen("QQQ", 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma_qqq.IsReady: return
        
        hist = self.History(list(self.symbols.values()) + [self.qqq], 64, Resolution.Daily)
        if hist.empty: return
        
        try:
            q_prices = hist.loc[self.qqq]['close'].values
            q_ret = (q_prices[-1] / q_prices[0]) - 1
            
            passing_candidates = {}
            for ticker, symbol in self.symbols.items():
                if symbol in hist.index.get_level_values(0):
                    prices = hist.loc[symbol]['close'].values
                    asset_ret = (prices[-1] / prices[0]) - 1
                    
                    # Triple Lock: 1) Abs Mom > 0, 2) Rel Mom > 0, 3) Trend UP
                    if asset_ret > 0 and asset_ret > q_ret and self.Securities[symbol].Price > self.sma_qqq.Current.Value:
                        passing_candidates[ticker] = asset_ret - q_ret
        except:
            return
            
        if not passing_candidates:
            self.Log(f"[{self.Time}] NO ASSETS PASSED TRIPLE LOCK. Moving to Cash.")
            self.Liquidate()
            self.SetHoldings(self.bil, 1.0)
            return
            
        # Pick asset with highest relative alpha
        best_ticker = max(passing_candidates, key=passing_candidates.get)
        self.Log(f"[{self.Time}] TRIPLE LOCK ON: {best_ticker}. Rotating in.")
        
        if not self.Portfolio[self.symbols[best_ticker]].Invested:
            self.SetHoldings(self.symbols[best_ticker], 1.0)
            for t, s in self.symbols.items():
                if s != best_ticker: self.Liquidate(s)
            self.Liquidate(self.bil)

    def OnData(self, data):
        pass
