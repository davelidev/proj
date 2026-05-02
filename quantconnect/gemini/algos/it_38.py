from AlgorithmImports import *

class TQQQGoldBondRotation(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.assets = ["TQQQ", "GLD", "TLT"]
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.symbols = {}
        for ticker in self.assets:
            self.symbols[ticker] = self.AddEquity(ticker, Resolution.Daily).Symbol
            
        self.Schedule.On(self.DateRules.EveryDay("TQQQ"), 
                         self.TimeRules.AfterMarketOpen("TQQQ", 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(22)

    def Rebalance(self):
        if self.Time.weekday() != 0: return # Mondays
        if self.IsWarmingUp: return
        
        hist = self.History(list(self.symbols.values()), 22, Resolution.Daily)
        if hist.empty: return
        
        momentum_scores = {}
        for ticker, symbol in self.symbols.items():
            if symbol in hist.index.get_level_values(0):
                prices = hist.loc[symbol]['close'].values
                momentum_scores[ticker] = (prices[-1] / prices[0]) - 1
        
        if not momentum_scores: return
        
        best_ticker = max(momentum_scores, key=momentum_scores.get)
        best_score = momentum_scores[best_ticker]
        
        # Signal: Best performer must have positive momentum
        if best_score > 0:
            self.Log(f"[{self.Time}] ROTATING TO {best_ticker} (Score: {best_score:.1%})")
            if not self.Portfolio[self.symbols[best_ticker]].Invested:
                self.SetHoldings(self.symbols[best_ticker], 1.0)
                for t in self.assets:
                    if t != best_ticker: self.Liquidate(self.symbols[t])
                self.Liquidate(self.bil)
        else:
            self.Log(f"[{self.Time}] NO POSITIVE MOMENTUM. Moving to Cash.")
            self.Liquidate()
            self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
