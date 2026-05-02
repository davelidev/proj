from AlgorithmImports import *

class SectorMomentum(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        # 3x Leveraged Growth Assets
        self.assets = ["TQQQ", "SOXL", "WEBL"]
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.symbols = {}
        self.rsis = {}
        for ticker in self.assets:
            symbol = self.AddEquity(ticker, Resolution.Daily).Symbol
            self.symbols[ticker] = symbol
            self.rsis[symbol] = self.RSI(symbol, 14, MovingAverageType.Wilders, Resolution.Daily)
            
        self.Schedule.On(self.DateRules.EveryDay("TQQQ"), 
                         self.TimeRules.AfterMarketOpen("TQQQ", 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(30)

    def Rebalance(self):
        if self.Time.weekday() != 0: return # Mondays
        if self.IsWarmingUp: return
        
        # 1. Rank by 1-month ROC
        hist = self.History(list(self.symbols.values()), 22, Resolution.Daily)
        if hist.empty: return
        
        scores = {}
        for ticker, symbol in self.symbols.items():
            if symbol in hist.index.get_level_values(0):
                prices = hist.loc[symbol]['close'].values
                if len(prices) < 20: continue
                roc = (prices[-1] / prices[0]) - 1
                
                # Filter: Must have positive ROC AND RSI > 50
                if roc > 0 and self.rsis[symbol].Current.Value > 50:
                    scores[ticker] = roc
        
        if not scores:
            self.Log(f"[{self.Time}] NO LEADERSHIP. Moving to Cash.")
            self.Liquidate()
            self.SetHoldings(self.bil, 1.0)
            return
            
        # 2. Pick best performer
        best_ticker = max(scores, key=scores.get)
        self.Log(f"[{self.Time}] ROTATING TO {best_ticker} (ROC: {scores[best_ticker]:.1%})")
        
        if not self.Portfolio[self.symbols[best_ticker]].Invested:
            self.SetHoldings(self.symbols[best_ticker], 1.0)
            for t in self.assets:
                if t != best_ticker: self.Liquidate(self.symbols[t])
            self.Liquidate(self.bil)

    def OnData(self, data):
        pass
