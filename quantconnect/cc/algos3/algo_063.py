from AlgorithmImports import *

class Algo063(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        # Hard rule: Add TQQQ with Daily resolution
        self.AddEquity("TQQQ", Resolution.Daily)
        
        # Universe selection: top 10 by market cap across all sectors
        self.AddUniverse(self.CoarseSelectionFunction)
        
        # Basket to hold current universe symbols (dictionary, not list)
        self.basket = {}
        
        # Indicator storage
        self.macd = {}
        self.prev_macd = {}
        self.prev_signal = {}
        
        # Warm-up period for MACD
        self.SetWarmUp(26)  # MACD(12,26,9) needs 26 periods to be ready
        
    def CoarseSelectionFunction(self, coarse):
        # Filter stocks with fundamental data and positive price
        filtered = [c for c in coarse if c.HasFundamentalData and c.Price > 0 and c.MarketCap > 0]
        # Sort by market cap descending and take top 10
        sorted_by_mcap = sorted(filtered, key=lambda c: c.MarketCap, reverse=True)
        top10 = sorted_by_mcap[:10]
        return [c.Symbol for c in top10]
    
    def OnSecuritiesChanged(self, changes):
        # Remove symbols that are no longer in the universe
        for removed in changes.RemovedSecurities:
            symbol = removed.Symbol
            if symbol in self.basket:
                self.Liquidate(symbol)
                del self.basket[symbol]
            if symbol in self.macd:
                del self.macd[symbol]
            if symbol in self.prev_macd:
                del self.prev_macd[symbol]
            if symbol in self.prev_signal:
                del self.prev_signal[symbol]
        
        # Add new symbols
        for added in changes.AddedSecurities:
            symbol = added.Symbol
            if symbol not in self.basket:
                self.basket[symbol] = True  # mark as in basket
                # Create MACD indicator
                self.macd[symbol] = self.MACD(symbol, 12, 26, 9, MovingAverageType.Exponential, Resolution.Daily)
                # Initialize previous values as None
                self.prev_macd[symbol] = None
                self.prev_signal[symbol] = None
    
    def OnData(self, data):
        if self.IsWarmingUp:
            return
        
        # Process each symbol in the basket
        for symbol in list(self.basket.keys()):
            if not data.ContainsKey(symbol) or data[symbol] is None:
                continue
            
            # Update MACD indicator
            bar = data[symbol]
            self.macd[symbol].Update(bar.EndTime, bar.Close)
            
            # Check if indicator is ready
            if not self.macd[symbol].IsReady:
                continue
            
            macd_current = self.macd[symbol].Current.Value
            signal_current = self.macd[symbol].Signal.Current.Value
            
            # Retrieve previous values
            prev_macd = self.prev_macd[symbol]
            prev_signal = self.prev_signal[symbol]
            
            # Determine crossover
            if prev_macd is not None and prev_signal is not None:
                # MACD crosses above signal -> buy
                if macd_current > signal_current and prev_macd <= prev_signal:
                    # Equal weight allocation
                    weight = 1.0 / len(self.basket) if len(self.basket) > 0 else 0
                    self.SetHoldings(symbol, weight)
                    self.Debug(f"BUY {symbol} at {bar.Close:.2f}")
                # MACD crosses below signal -> sell
                elif macd_current < signal_current and prev_macd >= prev_signal:
                    self.SetHoldings(symbol, 0)
                    self.Debug(f"SELL {symbol} at {bar.Close:.2f}")
            
            # Update stored previous values
            self.prev_macd[symbol] = macd_current
            self.prev_signal[symbol] = signal_current
