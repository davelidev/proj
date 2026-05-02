from AlgorithmImports import *
import numpy as np

class LeveragedParity(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.assets = ["TQQQ", "SOXL", "TNA"]
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.symbols = {}
        for ticker in self.assets:
            self.symbols[ticker] = self.AddEquity(ticker, Resolution.Daily).Symbol
            
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.sma = self.SMA(self.qqq, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay("QQQ"), 
                         self.TimeRules.AfterMarketOpen("QQQ", 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if self.Time.weekday() != 0: return # Mondays
        if self.IsWarmingUp or not self.sma.IsReady: return
        
        price_q = self.Securities[self.qqq].Price
        sma_val = self.sma.Current.Value
        
        if price_q < sma_val:
            self.Liquidate()
            self.SetHoldings(self.bil, 1.0)
            return
            
        # Bullish: Inverse Volatility Weighting
        hist = self.History(list(self.symbols.values()), 22, Resolution.Daily)
        if hist.empty: return
        
        inv_vols = {}
        total_inv_vol = 0
        for ticker, symbol in self.symbols.items():
            if symbol in hist.index.get_level_values(0):
                returns = hist.loc[symbol]['close'].pct_change().dropna()
                std = np.std(returns)
                if std > 0:
                    inv_vols[symbol] = 1.0 / std
                    total_inv_vol += inv_vols[symbol]
        
        if total_inv_vol == 0: return
        
        # Calculate and execute weights
        for symbol, inv_vol in inv_vols.items():
            weight = inv_vol / total_inv_vol
            self.SetHoldings(symbol, weight)
            
        self.Liquidate(self.bil)

    def OnData(self, data):
        pass
