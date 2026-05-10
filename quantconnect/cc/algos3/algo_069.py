from System import *
from QuantConnect import *
from QuantConnect.Algorithm import *
from QuantConnect.Indicators import *
from collections import deque

class Algo069(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.AddEquity("TQQQ", Resolution.Daily)
        
        # dynamic universe: top 10 by market cap (all sectors)
        self.AddUniverse(self.CoarseSelectionFunction)
        
        self.basket = {}                # store all Symbols we trade
        self.symbol_data = {}           # indicator & history per Symbol
        self.selected_symbols = []      # updated by universe
        
        # indicator lookback period
        self.lookback = 14
        
    def CoarseSelectionFunction(self, coarse):
        # select top 10 by market cap
        sorted_by_mcap = sorted(
            [c for c in coarse if c.HasFundamentalData and c.MarketCap > 0],
            key=lambda c: c.MarketCap,
            reverse=True
        )
        top10 = sorted_by_mcap[:10]
        self.selected_symbols = [c.Symbol for c in top10]
        return self.selected_symbols
    
    def OnData(self, slice):
        # 1. Build the current basket (TQQQ always + universe symbols)
        tqqq = self.Symbol("TQQQ")
        new_basket = {tqqq: True}
        for sym in self.selected_symbols:
            new_basket[sym] = True
        
        # Remove symbols that left the basket
        old_symbols = set(self.basket.keys())
        new_symbols = set(new_basket.keys())
        for sym in old_symbols - new_symbols:
            if sym in self.symbol_data:
                del self.symbol_data[sym]
        self.basket = {sym: True for sym in new_symbols}
        
        # 2. Ensure indicator/history objects for all current basket symbols
        for sym in self.basket:
            if sym not in self.symbol_data:
                rsi = RelativeStrengthIndex(self.lookback)
                self.RegisterIndicator(sym, rsi, Resolution.Daily)
                self.symbol_data[sym] = {
                    "rsi": rsi,
                    "low": deque(maxlen=self.lookback+1),
                    "high": deque(maxlen=self.lookback+1),
                    "rsi_value": deque(maxlen=self.lookback+1),
                    "warmed_up": False
                }
        
        # 3. Update indicators and price history
        for sym in self.basket:
            if sym in slice and slice[sym] is not None:
                bar = slice[sym]
                data = self.symbol_data[sym]
                # update price history
                data["low"].append(bar.Low)
                data["high"].append(bar.High)
                # RSI is updated automatically by RegisterIndicator
                if data["rsi"].IsReady:
                    data["rsi_value"].append(data["rsi"].Current.Value)
                    if len(data["rsi_value"]) >= self.lookback + 1:
                        data["warmed_up"] = True
        
        # 4. Compute divergence signals
        signals = {}
        for sym in self.basket:
            data = self.symbol_data.get(sym)
            if data is None or not data["warmed_up"]:
                continue
            # get current and 14 bars back values
            low = data["low"]
            high = data["high"]
            rsi_vals = data["rsi_value"]
            if len(low) < self.lookback+1 or len(rsi_vals) < self.lookback+1:
                continue
            
            curr_low = low[-1]
            prev_low = low[-self.lookback-1]  # 14 days ago (0-indexed)
            curr_high = high[-1]
            prev_high = high[-self.lookback-1]
            curr_rsi = rsi_vals[-1]
            prev_rsi = rsi_vals[-self.lookback-1]
            
            # Bullish divergence: price lower low, RSI higher low
            if curr_low < prev_low and curr_rsi > prev_rsi:
                signals[sym] = 1
            # Bearish divergence: price higher high, RSI lower high
            elif curr_high > prev_high and curr_rsi < prev_rsi:
                signals[sym] = -1
            else:
                signals[sym] = 0
        
        # 5. Rebalance portfolio
        # Count active positions (non-zero signal)
        active = {sym: sig for sym, sig in signals.items() if sig != 0}
        num_active = len(active)
        
        if num_active == 0:
            # close all positions in basket
            for sym in self.basket:
                self.SetHoldings(sym, 0)
        else:
            target_weight = 1.0 / num_active
            for sym in self.basket:
                if sym in active:
                    self.SetHoldings(sym, target_weight * active[sym])
                else:
                    self.SetHoldings(sym, 0)
