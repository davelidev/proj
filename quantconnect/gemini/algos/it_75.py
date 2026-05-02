from AlgorithmImports import *

class HighHighRotation(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.assets = ["TQQQ", "SOXL", "QQQ"]
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.symbols = {}
        self.highs = {}
        self.obvs = {}
        
        for ticker in self.assets:
            symbol = self.AddEquity(ticker, Resolution.Daily).Symbol
            self.symbols[ticker] = symbol
            self.highs[symbol] = self.MAX(symbol, 20, Resolution.Daily)
            self.obvs[symbol] = self.OBV(symbol, Resolution.Daily)
            
        self.Schedule.On(self.DateRules.EveryDay("QQQ"), 
                         self.TimeRules.AfterMarketOpen("QQQ", 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(20)

    def Rebalance(self):
        if self.IsWarmingUp: return
        
        breakout_candidates = []
        for ticker, symbol in self.symbols.items():
            price = self.Securities[symbol].Price
            if price >= self.highs[symbol].Current.Value:
                # Calculate 20-day OBV ROC
                hist_obv = self.History(symbol, 21, Resolution.Daily)
                if not hist_obv.empty:
                    # Manually calculate OBV ROC since we can't easily get hist indicators
                    obv_growth = float(self.obvs[symbol].Current.Value)
                    breakout_candidates.append((ticker, symbol, obv_growth))
        
        if not breakout_candidates:
            # If nothing is breaking out and we are invested, check for 10-day low exit
            if self.Portfolio.Invested:
                for symbol in self.Portfolio.Keys:
                    if symbol == self.bil: continue
                    hist_low = self.History(symbol, 10, Resolution.Daily)
                    if not hist_low.empty:
                        min_low = hist_low['low'].min()
                        if self.Securities[symbol].Price < min_low:
                            self.Liquidate(symbol)
                            self.SetHoldings(self.bil, 1.0)
            return
            
        # Pick best candidate by OBV value (simple volume flow proxy)
        best_ticker, best_symbol, _ = max(breakout_candidates, key=lambda x: x[2])
        
        if not self.Portfolio[best_symbol].Invested:
            self.Log(f"[{self.Time}] BREAKOUT: {best_ticker}. Rotating in.")
            self.SetHoldings(best_symbol, 1.0)
            for t, s in self.symbols.items():
                if s != best_symbol: self.Liquidate(s)
            self.Liquidate(self.bil)

    def OnData(self, data):
        pass
