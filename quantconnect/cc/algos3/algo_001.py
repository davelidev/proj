from datetime import datetime
from QuantConnect import *
from QuantConnect.Algorithm import *
from QuantConnect.Indicators import *
from QuantConnect.Data.UniverseSelection import *
import math

class Algo001(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.SetWarmUp(100)  # ensure indicators are ready
        
        self.AddEquity('TQQQ', Resolution.Daily)
        self.basket = {}
        
        self.AddUniverse(self.CoarseSelectionFunction)
        
        # Indicators for TQQQ
        self.roc = self.ROC('TQQQ', 1, Resolution.Daily)
        self.std = self.STD(self.roc, 20, Resolution.Daily)   # 20-day std of daily returns
        self.rs = self.RSI('TQQQ', 5, Resolution.Daily)
        
    def CoarseSelectionFunction(self, coarse):
        # Filter stocks with fundamental data and positive price
        filtered = [c for c in coarse if c.HasFundamentalData and c.Price > 0]
        sorted_by_mcap = sorted(filtered, key=lambda c: c.MarketCap, reverse=True)
        top10 = [c.Symbol for c in sorted_by_mcap[:10]]
        # Update basket with new symbols
        self.basket = {symbol: 0.0 for symbol in top10}
        return top10
    
    def OnData(self, data):
        if self.IsWarmingUp:
            return
        if not (self.roc.IsReady and self.std.IsReady and self.rs.IsReady):
            return
        
        # Annualized vol in percent (sqrt(252) for daily data)
        vol = self.std.Current.Value * math.sqrt(252)
        rsi = self.rs.Current.Value
        
        signal = None
        if rsi < 30 and vol < 25:
            signal = 'long'
        elif rsi > 70 and vol < 25:
            signal = 'short'
        
        # No trade if no signal or empty basket
        if signal is None or len(self.basket) == 0:
            return
        
        # Equal weight across basket, sum of absolute weights = 1
        weight = 1.0 / len(self.basket)
        if signal == 'short':
            weight = -weight
        
        # Set target weights in the basket dict
        for symbol in self.basket:
            self.basket[symbol] = weight
        
        self.SetHoldings(self.basket)
