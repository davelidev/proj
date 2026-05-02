from AlgorithmImports import *
import numpy as np

class AccelerationRotation(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.assets = ["TQQQ", "SOXL"]
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.symbols = {}
        self.roc_windows = {}
        self.rocs = {}
        
        for ticker in self.assets:
            symbol = self.AddEquity(ticker, Resolution.Daily).Symbol
            self.symbols[ticker] = symbol
            self.rocs[symbol] = self.ROC(symbol, 20, Resolution.Daily)
            self.roc_windows[symbol] = RollingWindow[float](11)
            
        self.Schedule.On(self.DateRules.EveryDay("BIL"), 
                         self.TimeRules.AfterMarketOpen("BIL", 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(40)

    def Rebalance(self):
        # Update windows daily
        for symbol in self.symbols.values():
            if self.rocs[symbol].IsReady:
                self.roc_windows[symbol].Add(self.rocs[symbol].Current.Value)
        
        if self.Time.weekday() != 0: return # Only Mondays
        if self.IsWarmingUp: return
        
        scores = {}
        for ticker, symbol in self.symbols.items():
            if self.roc_windows[symbol].IsReady:
                current_roc = self.roc_windows[symbol][0]
                prev_roc = self.roc_windows[symbol][10]
                acceleration = current_roc - prev_roc
                
                # Filter: Must have positive absolute ROC AND positive acceleration
                if current_roc > 0 and acceleration > 0:
                    scores[ticker] = acceleration
        
        if not scores:
            self.Log(f"[{self.Time}] NO ACCELERATING TRENDS. Moving to Cash.")
            self.Liquidate()
            self.SetHoldings(self.bil, 1.0)
            return
            
        # Pick best performer
        best_ticker = max(scores, key=scores.get)
        self.Log(f"[{self.Time}] ROTATING TO {best_ticker} (Accel: {scores[best_ticker]:.1f})")
        
        if not self.Portfolio[self.symbols[best_ticker]].Invested:
            self.SetHoldings(self.symbols[best_ticker], 1.0)
            for t, s in self.symbols.items():
                if s != best_ticker: self.Liquidate(s)
            self.Liquidate(self.bil)

    def OnData(self, data):
        pass
