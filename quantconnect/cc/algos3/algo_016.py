from QuantConnect import *
from QuantConnect.Algorithm import *
from QuantConnect.Indicators import *
from QuantConnect.Data.Fundamental import *
from datetime import datetime

class Algo016(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        
        # Add TQQQ (the only hardcoded ticker)
        tqqq = self.AddEquity('TQQQ', Resolution.Daily)
        
        # Basket to track all securities in the universe (including TQQQ)
        self.basket = {}
        self.indicators = {}
        
        # Add TQQQ to basket and set up its volume SMA indicator
        self.basket[tqqq.Symbol] = True
        self.indicators[tqqq.Symbol] = self.SMA(tqqq.Symbol, 20, Resolution.Daily, Field.Volume)
        
        # Dynamic universe: top 10 stocks by market cap (excluding TQQQ)
        self.AddUniverse(self.FundamentalFilter)
        
        # Warm-up period for indicators
        self.SetWarmUp(20, Resolution.Daily)
    
    def FundamentalFilter(self, fundamental):
        # fundamental: list of Fundamental objects
        # Filter to top 10 by market cap, excluding TQQQ
        sorted_by_mcap = sorted(fundamental, key=lambda f: f.MarketCap, reverse=True)
        top10 = sorted_by_mcap[:10]
        return [f.Symbol.Value for f in top10 if f.Symbol.Value != 'TQQQ']
    
    def OnSecuritiesChanged(self, changes):
        # Add newly selected securities to the basket and subscribe
        for added in changes.AddedSecurities:
            symbol = added.Symbol
            if symbol not in self.basket:
                # Subscribe to this security
                self.AddEquity(symbol, Resolution.Daily)
                self.basket[symbol] = True
                # Create 20-day volume SMA indicator
                self.indicators[symbol] = self.SMA(symbol, 20, Resolution.Daily, Field.Volume)
        
        # Remove securities that are no longer in the universe
        for removed in changes.RemovedSecurities:
            symbol = removed.Symbol
            if symbol in self.basket:
                self.Liquidate(symbol)
                del self.basket[symbol]
                if symbol in self.indicators:
                    del self.indicators[symbol]
    
    def OnData(self, data):
        if self.IsWarmingUp:
            return
        
        # Identify symbols that trigger the continuation signal
        signals = []
        for symbol in list(self.basket.keys()):
            if not data.ContainsKey(symbol):
                continue
            bar = data[symbol]
            if symbol not in self.indicators or not self.indicators[symbol].IsReady:
                continue
            volume_sma = self.indicators[symbol].Current.Value
            if bar.Close > bar.Open and bar.Volume > 1.2 * volume_sma:
                signals.append(symbol)
        
        # Determine target weights (equal weight among signals)
        if len(signals) > 0:
            weight = 1.0 / len(signals)
            for symbol in self.basket:
                if symbol in signals:
                    self.SetHoldings(symbol, weight)
                else:
                    self.SetHoldings(symbol, 0)
        else:
            # No signals, liquidate all positions
            for symbol in self.basket:
                self.Liquidate(symbol)
