from System import *
from QuantConnect import *
from QuantConnect.Algorithm import *
from QuantConnect.Data.UniverseSelection import *
from QuantConnect.Indicators import *

class Algo021(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.SetWarmUp(21, Resolution.Daily)
        
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily)
        self.AddUniverse(self.CoarseSelectionFunction)
        
        self.basket = {}
        
        # Initialize TQQQ indicators
        sma_tqqq = self.SMA(self.tqqq.Symbol, 20, Resolution.Daily, Field.Close)
        median_vol_tqqq = self.MEDIAN(self.tqqq.Symbol, 20, Resolution.Daily, Field.Volume)
        self.basket[self.tqqq.Symbol] = {"sma": sma_tqqq, "median": median_vol_tqqq}
        
        # Warm up TQQQ indicators
        self.WarmUpIndicator(self.tqqq.Symbol, sma_tqqq, 21, Resolution.Daily)
        self.WarmUpIndicator(self.tqqq.Symbol, median_vol_tqqq, 21, Resolution.Daily)
    
    def CoarseSelectionFunction(self, coarse):
        # Filter stocks with price > $1 and fundamental data, sort by market cap descending, take top 10
        filtered = [c for c in coarse if c.HasFundamentalData and c.Price > 1]
        sorted_by_cap = sorted(filtered, key=lambda c: c.MarketCap, reverse=True)
        return [c.Symbol for c in sorted_by_cap[:10]]
    
    def OnSecuritiesChanged(self, changes):
        for added in changes.AddedSecurities:
            symbol = added.Symbol
            if symbol not in self.basket:
                # Initialize indicators
                sma = self.SMA(symbol, 20, Resolution.Daily, Field.Close)
                median_vol = self.MEDIAN(symbol, 20, Resolution.Daily, Field.Volume)
                self.basket[symbol] = {"sma": sma, "median": median_vol}
                
                # Warm up indicators with historical data
                self.WarmUpIndicator(symbol, sma, 21, Resolution.Daily)
                self.WarmUpIndicator(symbol, median_vol, 21, Resolution.Daily)
        
        for removed in changes.RemovedSecurities:
            symbol = removed.Symbol
            if symbol in self.basket:
                # Liquidate position and remove from basket
                self.Liquidate(symbol)
                del self.basket[symbol]
    
    def OnData(self, data):
        if self.IsWarmingUp:
            return
        
        # Compute signals
        signals = {}
        for symbol, indicators in self.basket.items():
            if data.ContainsKey(symbol) and indicators["sma"].IsReady and indicators["median"].IsReady:
                price = data[symbol].Close
                volume = data[symbol].Volume
                sma_val = indicators["sma"].Current.Value
                median_vol_val = indicators["median"].Current.Value
                
                if price > sma_val * 1.1 and volume > 1.5 * median_vol_val:
                    signals[symbol] = True
                else:
                    signals[symbol] = False
        
        num_long = sum(1 for v in signals.values() if v)
        
        if num_long == 0:
            # No signals: liquidate all positions
            for symbol in self.basket:
                self.SetHoldings(symbol, 0)
        else:
            weight = 1.0 / num_long
            for symbol, is_long in signals.items():
                target_weight = weight if is_long else 0
                self.SetHoldings(symbol, target_weight)