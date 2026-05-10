from AlgorithmImports import *
from collections import defaultdict
import numpy as np
import pandas as pd

class Algo086(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        # Universe settings: daily resolution
        self.UniverseSettings.Resolution = Resolution.Daily
        self.UniverseSettings.DataNormalizationMode = DataNormalizationMode.Adjusted
        
        # Add coarse universe to select liquid stocks
        self.AddUniverse(self.CoarseFilter)
        
        # Schedule rebalancing on first trading day of each month
        self.Schedule.On(self.DateRules.MonthStart(), self.TimeRules.AfterMarketOpen(), self.Rebalance)
        
        # Dictionary to hold symbol data (not strictly needed if we use history each time)
        self._symbols = []
        
    def CoarseFilter(self, coarse):
        # Filter stocks with sufficient liquidity and price
        filtered = [c for c in coarse if c.HasFundamentalData and c.Price > 5 and c.DollarVolume > 1000000]
        # Sort by dollar volume and take top 500
        sorted_by_volume = sorted(filtered, key=lambda x: x.DollarVolume, reverse=True)
        top = [c.Symbol for c in sorted_by_volume[:500]]
        self._symbols = top
        return top
    
    def Rebalance(self):
        symbols = self._symbols
        if len(symbols) == 0:
            return
        
        # Request history for all symbols: need at least 64 days for 63d momentum, use 65 to be safe
        history = self.History(symbols, 65, Resolution.Daily)
        if history.empty:
            return
        
        # Group by symbol
        hist_by_symbol = {}
        for symbol in symbols:
            try:
                df = history.loc[symbol] if isinstance(history.index, pd.MultiIndex) else history
                if isinstance(history.index, pd.MultiIndex):
                    df = history.xs(symbol, level=0)
                else:
                    df = history
                # Need to ensure we have enough data
                if len(df) < 64:
                    continue
                hist_by_symbol[symbol] = df['close']
            except:
                continue
        
        selected = []
        momentum_scores = []
        
        for symbol, close in hist_by_symbol.items():
            # Compute 21-day and 63-day momentum as percentage change
            mom21 = close.pct_change(21).iloc[-1]
            mom63 = close.pct_change(63).iloc[-1]
            if np.isnan(mom21) or np.isnan(mom63):
                continue
            # Momentum acceleration: 21d > 63d
            if mom21 > mom63:
                selected.append(symbol)
                momentum_scores.append(mom21)  # could use momentum for weighting
        
        if len(selected) == 0:
            return
        
        # Equal weight among selected stocks, total weight <= 1.0
        weight = 1.0 / len(selected)
        if weight > 1.0:
            weight = 1.0  # per asset cap, but with many assets this won't happen
        
        # Liquidate any current holdings not in selected
        for symbol in self.Portfolio.Keys:
            if self.Portfolio[symbol].Invested and symbol not in selected:
                self.SetHoldings(symbol, 0)
        
        # Set target weights
        for symbol in selected:
            self.SetHoldings(symbol, weight)  # SetHoldings will handle leverage automatically, we ensure sum <= 1
