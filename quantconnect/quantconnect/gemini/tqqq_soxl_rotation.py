from AlgorithmImports import *

class TQQQSOXLRotation(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.assets = {"TQQQ": "QQQ", "SOXL": "SOXX"}
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.symbols = {}
        self.benchmarks = {}
        for ticker, bench in self.assets.items():
            self.symbols[ticker] = self.AddEquity(ticker, Resolution.Daily).Symbol
            self.benchmarks[bench] = self.AddEquity(bench, Resolution.Daily).Symbol
            
        self.sma_gate = self.SMA(self.benchmarks["QQQ"], 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay("QQQ"), 
                         self.TimeRules.AfterMarketOpen("QQQ", 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if self.Time.weekday() != 0: return # Mondays
        if self.IsWarmingUp or not self.sma_gate.IsReady: return
        
        price_q = self.Securities[self.benchmarks["QQQ"]].Price
        sma_val = self.sma_gate.Current.Value
        
        if price_q < sma_val:
            self.Log(f"[{self.Time}] MARKET BEARISH. Moving to Cash.")
            self.Liquidate()
            self.SetHoldings(self.bil, 1.0)
            return
            
        # Market Bullish, pick best performer by 1-month ROC
        hist = self.History(list(self.benchmarks.values()), 22, Resolution.Daily)
        if hist.empty: return
        
        roc_scores = {}
        for bench, symbol in self.benchmarks.items():
            if symbol in hist.index.get_level_values(0):
                prices = hist.loc[symbol]['close'].values
                roc_scores[bench] = (prices[-1] / prices[0]) - 1
        
        if not roc_scores: return
        
        # Find ticker corresponding to best benchmark
        best_bench = max(roc_scores, key=roc_scores.get)
        best_ticker = [k for k, v in self.assets.items() if v == best_bench][0]
        
        self.Log(f"[{self.Time}] TECH TREND UP. Rotating to {best_ticker} (ROC: {roc_scores[best_bench]:.1%})")
        
        if not self.Portfolio[self.symbols[best_ticker]].Invested:
            self.SetHoldings(self.symbols[best_ticker], 1.0)
            for t in self.assets:
                if t != best_ticker: self.Liquidate(self.symbols[t])
            self.Liquidate(self.bil)

    def OnData(self, data):
        pass
