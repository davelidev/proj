from AlgorithmImports import *
import numpy as np

class HighVolRSIRotation(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.assets = ["TQQQ", "SOXL"]
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.symbols = {}
        self.rsis = {}
        self.stds = {}
        
        for ticker in self.assets:
            symbol = self.AddEquity(ticker, Resolution.Daily).Symbol
            self.symbols[ticker] = symbol
            self.rsis[symbol] = self.RSI(symbol, 2, MovingAverageType.Wilders, Resolution.Daily)
            self.stds[symbol] = self.STD(symbol, 21, Resolution.Daily)
            
        self.SetWarmUp(30)

    def OnData(self, data):
        if self.IsWarmingUp: return
        
        dip_candidates = []
        for ticker, symbol in self.symbols.items():
            if not self.rsis[symbol].IsReady or not self.stds[symbol].IsReady: continue
            
            if self.rsis[symbol].Current.Value < 25:
                # Add to candidate list with current vol
                dip_candidates.append((ticker, symbol, self.stds[symbol].Current.Value))
        
        if not dip_candidates:
            # Check for exit if invested
            if self.Portfolio.Invested:
                for symbol in self.Portfolio.Keys:
                    if symbol == self.bil: continue
                    if self.rsis[symbol].IsReady and self.rsis[symbol].Current.Value > 75:
                        self.Liquidate(symbol)
                        self.SetHoldings(self.bil, 1.0)
            return
            
        # Pick asset with HIGHEST volatility among those in a dip
        best_ticker, best_symbol, _ = max(dip_candidates, key=lambda x: x[2])
        
        if not self.Portfolio[best_symbol].Invested:
            self.Log(f"[{self.Time}] DOUBLE DIP. Selecting highest vol leader: {best_ticker}.")
            self.SetHoldings(best_symbol, 1.0)
            for t, s in self.symbols.items():
                if s != best_symbol: self.Liquidate(s)
            self.Liquidate(self.bil)
