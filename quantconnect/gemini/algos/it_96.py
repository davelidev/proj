from AlgorithmImports import *
import numpy as np

class VolumeWeightedRotation(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.assets = ["TQQQ", "SOXL", "UGL", "TLT"]
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.symbols = {}
        self.vol_smas = {}
        
        for ticker in self.assets:
            symbol = self.AddEquity(ticker, Resolution.Daily).Symbol
            self.symbols[ticker] = symbol
            self.vol_smas[symbol] = self.SMA(symbol, 20, Resolution.Daily, Field.Volume)
            
        self.Schedule.On(self.DateRules.MonthStart("TQQQ"), 
                         self.TimeRules.AfterMarketOpen("TQQQ", 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(64)

    def Rebalance(self):
        if self.IsWarmingUp: return
        
        hist = self.History(list(self.symbols.values()), 64, Resolution.Daily)
        if hist.empty: return
        
        scores = {}
        for ticker, symbol in self.symbols.items():
            if symbol in hist.index.get_level_values(0):
                prices = hist.loc[symbol]['close'].values
                if len(prices) < 60: continue
                
                # ROC (Return)
                return_val = (prices[-1] / prices[0]) - 1
                
                # Volume Intensity
                current_vol = float(self.Securities[symbol].Volume)
                avg_vol = float(self.vol_smas[symbol].Current.Value)
                intensity = current_vol / avg_vol if avg_vol > 0 else 1.0
                
                # Score = Return * Intensity
                if return_val > 0:
                    scores[ticker] = return_val * intensity
        
        if not scores:
            self.Log(f"[{self.Time}] NO CONVINCING TRENDS. Moving to Cash.")
            self.Liquidate()
            self.SetHoldings(self.bil, 1.0)
            return
            
        best_ticker = max(scores, key=scores.get)
        self.Log(f"[{self.Time}] ROTATING TO {best_ticker} (VW-Score: {scores[best_ticker]:.2f})")
        
        if not self.Portfolio[self.symbols[best_ticker]].Invested:
            self.SetHoldings(self.symbols[best_ticker], 1.0)
            for t, s in self.symbols.items():
                if s != best_ticker: self.Liquidate(s)
            self.Liquidate(self.bil)

    def OnData(self, data):
        pass
