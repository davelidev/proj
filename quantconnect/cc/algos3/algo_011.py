from AlgorithmImports import *

class Algo011(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        
        self.AddEquity('TQQQ', Resolution.Daily)
        
        # Universe selection: top 10 by market cap
        self.AddUniverse(self.CoarseSelectionFunction)
        
        self.basket = {}           # symbol -> target weight (placeholder)
        self.maximum = {}          # symbol -> Maximum indicator (10 periods)
        self.roc = {}              # symbol -> RateOfChange indicator (5 periods)
        self._selectedSymbols = [] # latest selection from universe
        
        self.SetWarmUp(10, Resolution.Daily)
    
    def CoarseSelectionFunction(self, coarse):
        # Filter stocks with fundamentals and positive price/market cap
        sorted_by_market_cap = sorted(
            [c for c in coarse if c.HasFundamentalData and c.AdjustedPrice > 0 and c.MarketCap > 0],
            key=lambda c: c.MarketCap,
            reverse=True
        )
        top10 = [c.Symbol for c in sorted_by_market_cap[:10]]
        self._selectedSymbols = top10
        return top10
    
    def OnData(self, data):
        if self.IsWarmingUp:
            return
        
        # Determine which symbols have entered or left the basket
        selected = set(self._selectedSymbols)
        current = set(self.basket.keys())
        to_add = selected - current
        to_remove = current - selected
        
        # Remove symbols that are no longer in the top 10
        for symbol in to_remove:
            self.Liquidate(symbol)
            del self.basket[symbol]
            del self.maximum[symbol]
            del self.roc[symbol]
        
        # Add new symbols
        for symbol in to_add:
            # Create indicators
            max_ind = Maximum(10)
            roc_ind = RateOfChange(5)
            
            # Warm-up with historical data
            history = self.History(symbol, 10, Resolution.Daily)
            if not history.empty:
                # History may have multi-index; use loc for the symbol
                try:
                    hist_series = history.loc[symbol]
                except KeyError:
                    hist_series = history  # fallback if not multi-index
                for time, row in hist_series.iterrows():
                    max_ind.Update(time, row['close'])
                    roc_ind.Update(time, row['close'])
            
            self.maximum[symbol] = max_ind
            self.roc[symbol] = roc_ind
            self.basket[symbol] = 0.0  # placeholder
        
        # Update indicators with current bar and compute signals
        n = len(self.basket)
        if n == 0:
            return
        
        for symbol in list(self.basket.keys()):
            bar = data.Bars.GetValue(symbol)
            if bar is None:
                continue
            
            # Update indicators with today's bar
            self.maximum[symbol].Update(bar.EndTime, bar.Close)
            self.roc[symbol].Update(bar.EndTime, bar.Close)
            
            # Check if indicators are ready
            if not self.maximum[symbol].IsReady or not self.roc[symbol].IsReady:
                continue
            
            # Signal conditions
            highest_close = bar.Close >= self.maximum[symbol].Current.Value
            momentum_positive = self.roc[symbol].Current.Value > 0.0
            
            if highest_close and momentum_positive:
                target_weight = 1.0 / n
            else:
                target_weight = -1.0 / n
            
            self.basket[symbol] = target_weight
        
        # Apply target holdings (no leverage, weights sum to 1.0 in absolute terms)
        for symbol, weight in self.basket.items():
            self.SetHoldings(symbol, weight)
