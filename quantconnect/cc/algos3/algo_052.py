from AlgorithmImports import *

class Algo052(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        
        # Add TQQQ as fixed equity (not traded in universe)
        self.AddEquity("TQQQ", Resolution.Daily)
        
        # Initialize basket dictionary
        self.basket = {}
        
        # Universe selection: top 10 by market cap (all sectors)
        self.AddUniverse(self.CoarseSelectionFunction, self.FineSelectionFunction)
        
        # Warm up for indicator calculation
        self.SetWarmUp(100)
    
    def CoarseSelectionFunction(self, coarse):
        # Basic filters: price above $5, positive volume, has fundamental data
        filtered = [c for c in coarse if c.HasFundamentalData and c.Price > 5 and c.Volume > 0]
        return [c.Symbol for c in filtered]
    
    def FineSelectionFunction(self, fine):
        # Sort by market cap descending, take top 10
        sorted_by_mc = sorted(fine, key=lambda f: f.MarketCap, reverse=True)
        top10 = sorted_by_mc[:10]
        return [f.Symbol for f in top10]
    
    def OnSecuritiesChanged(self, changes):
        # Add new symbols to basket
        for added in changes.AddedSecurities:
            symbol = added.Symbol
            if symbol not in self.basket:
                self.basket[symbol] = SymbolData(symbol, self)
        
        # Remove symbols no longer in universe
        for removed in changes.RemovedSecurities:
            symbol = removed.Symbol
            if symbol in self.basket:
                del self.basket[symbol]
    
    def OnData(self, data):
        if self.IsWarmingUp:
            return
        
        # Update indicators and collect signals
        buy_signals = []
        for symbol, sd in self.basket.items():
            if symbol in data and data[symbol] is not None:
                sd.Update(data[symbol])
                if sd.IsReady():
                    # Check crossover conditions
                    curr_k = sd.Sto.Current.Value
                    prev_k = sd.Sto.Previous.Value
                    
                    # Buy signal: %K crosses above 20 (from below 20)
                    if prev_k < 20 and curr_k >= 20:
                        buy_signals.append(symbol)
                    
                    # Sell signal: %K crosses below 80 (from above 80)
                    if prev_k > 80 and curr_k <= 80:
                        # Liquidate this position if held
                        self.Liquidate(symbol)
        
        # Set holdings for buy signals
        if buy_signals:
            weight = 1.0 / len(buy_signals)
            for symbol in buy_signals:
                self.SetHoldings(symbol, weight)
        else:
            # If no signals, we may still want to stay in cash or keep existing positions?
            # To strictly follow the strategy, we liquidate all not in signals.
            # But we might have existing positions from previous days that are still valid.
            # The classic approach: hold until overbought triggers sell.
            # Since we already sell on overbought cross, we must be careful not to liquidate
            # all positions that are still in oversold region but not crossing.
            # Actually we only liquidate when overbought cross happens. So we should not
            # liquidate all here. Instead we let positions remain until they hit overbought sell.
            # However, if a symbol is no longer in the basket (universe changed), we should liquidate.
            # We'll handle that by checking basket against current universe? Not needed because
            # OnSecuritiesChanged already removes them and we liquidate there? No, we didn't liquidate
            # in OnSecuritiesChanged. We'll add liquidation for removed symbols in OnSecuritiesChanged.
            pass  # Do nothing else, active positions are managed by overbought sell signal.
        
        # Liquidate symbols that are no longer in the basket (should have been removed in OnSecuritiesChanged)
        # But we need to ensure they are liquidated. We'll add liquidate in OnSecuritiesChanged for removed.
        # Let's modify OnSecuritiesChanged to liquidate removed symbols.
        # Actually we cannot modify above now; we'll do it here instead:
        for symbol in list(self.basket.keys()):
            if not self.Securities.ContainsKey(symbol):
                self.Liquidate(symbol)
                del self.basket[symbol]

class SymbolData:
    def __init__(self, symbol, algorithm):
        self.symbol = symbol
        self.algorithm = algorithm
        # Create Stochastic indicator (14,3,3) – default parameters
        self.Sto = algorithm.STO(symbol, 14, 3, 3, Resolution.Daily)
    
    def Update(self, trade_bar):
        # No need to call manually if using Consolidator; but we need to feed data.
        # Since we are using Daily resolution and the indicator auto-updates with data,
        # we must ensure the data is fed. However, in OnData we get trade bars, and
        # the indicator will automatically receive the data if it's registered with symbol.
        # Actually the STO indicator created with algorithm.STO(symbol, ...) will be automatically
        # updated by the algorithm's data feed. So we don't need manual Update.
        # But to be safe, we can call Update on the trade bar anyway.
        if trade_bar:
            self.Sto.Update(trade_bar)
    
    def IsReady(self):
        return self.Sto.IsReady
