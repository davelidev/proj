from AlgorithmImports import *

class HighConvictionBreakout(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.assets = ["TQQQ", "SOXL"]
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.symbols = {}
        self.highs = {}
        self.rsis = {}
        self.smas = {}
        
        for ticker in self.assets:
            symbol = self.AddEquity(ticker, Resolution.Daily).Symbol
            self.symbols[ticker] = symbol
            self.highs[symbol] = self.MAX(symbol, 60, Resolution.Daily)
            self.rsis[symbol] = self.RSI(symbol, 14, MovingAverageType.Wilders, Resolution.Daily)
            self.smas[symbol] = self.SMA(symbol, 20, Resolution.Daily)
            
        self.Schedule.On(self.DateRules.EveryDay("BIL"), 
                         self.TimeRules.AfterMarketOpen("BIL", 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(60)

    def Rebalance(self):
        if self.IsWarmingUp: return
        
        # 1. Check for Breakout Candidates
        candidates = []
        for ticker, symbol in self.symbols.items():
            if not (self.highs[symbol].IsReady and self.rsis[symbol].IsReady): continue
            
            price = self.Securities[symbol].Price
            high_val = self.highs[symbol].Current.Value
            rsi_val = self.rsis[symbol].Current.Value
            
            # Entry: Near high (within 1%) AND healthy RSI (not overbought)
            if price >= high_val * 0.99 and 50 < rsi_val < 70:
                candidates.append((ticker, symbol, rsi_val))
        
        if not candidates:
            # Check for Exit if invested
            if self.Portfolio.Invested:
                for symbol in self.Portfolio.Keys:
                    if symbol == self.bil: continue
                    price = self.Securities[symbol].Price
                    # Exit: Trend breaks (below 20 SMA) OR RSI is high (overbought)
                    if price < self.smas[symbol].Current.Value or self.rsis[symbol].Current.Value > 85:
                        self.Liquidate(symbol)
                        self.SetHoldings(self.bil, 1.0)
            return
            
        # 2. Pick best candidate by highest RSI (most momentum)
        best_ticker, best_symbol, _ = max(candidates, key=lambda x: x[2])
        
        if not self.Portfolio[best_symbol].Invested:
            self.Log(f"[{self.Time}] BREAKOUT: {best_ticker}. Entering.")
            self.SetHoldings(best_symbol, 1.0)
            for t, s in self.symbols.items():
                if s != best_symbol: self.Liquidate(s)
            self.Liquidate(self.bil)

    def OnData(self, data):
        pass
