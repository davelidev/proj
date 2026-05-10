from AlgorithmImports import *

class Algo017(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        
        # Add TQQQ (hardcoded exception)
        self.AddEquity('TQQQ', Resolution.Daily)
        
        # Universe selection: top 10 by market cap
        self.AddUniverse(self.CoarseFilter)
        
        # Basket to track holdings and indicators
        self.basket = {}
        
        # Initialize TQQQ in basket
        self.AddToBasket('TQQQ')
        # Warm up TQQQ indicators
        self.WarmUpBasket('TQQQ')
        
    def CoarseFilter(self, coarse):
        # Filter stocks with fundamental data and sort by market cap descending
        sorted_coarse = sorted([c for c in coarse if c.HasFundamentalData],
                               key=lambda c: c.MarketCap, reverse=True)
        top10 = [c.Symbol for c in sorted_coarse[:10] if c.Symbol.Value != 'TQQQ']
        return top10
    
    def OnSecuritiesChanged(self, changes):
        # Add new symbols to basket
        for added in changes.AddedSecurities:
            if added.Symbol.Value not in self.basket:
                self.AddToBasket(added.Symbol)
                self.WarmUpBasket(added.Symbol)
        # Remove symbols no longer in universe
        for removed in changes.RemovedSecurities:
            if removed.Symbol.Value in self.basket:
                self.Liquidate(removed.Symbol)
                del self.basket[removed.Symbol.Value]
    
    def AddToBasket(self, symbol):
        # Create indicator and close history
        self.basket[symbol] = {
            'sma': SimpleMovingAverage(20),
            'prev': None,   # yesterday's close
            'prev_prev': None # day before yesterday's close
        }
    
    def WarmUpBasket(self, symbol):
        # Request 22 bars to warm up SMA (20) and get last 2 closes
        history = self.History(symbol, 22, Resolution.Daily)
        if not history.empty:
            closes = history['close'].values
            # Update SMA with first 20 bars
            for i in range(min(20, len(closes))):
                self.basket[symbol]['sma'].Update(history.index[i][1], closes[i])
            # Set last two closes
            if len(closes) >= 2:
                self.basket[symbol]['prev'] = closes[-2]
            if len(closes) >= 1:
                self.basket[symbol]['prev_prev'] = closes[-1] if len(closes) >= 2 else None
                # The most recent close is set in OnData
    
    def OnData(self, data):
        # Update all basket symbols with daily data
        for sym_str, info in self.basket.items():
            symbol = Symbol.Create(sym_str, SecurityType.Equity, Market.USA)
            if data.ContainsKey(symbol):
                bar = data[symbol]
                # Update SMA
                info['sma'].Update(bar.EndTime, bar.Close)
                # Update close history
                info['prev_prev'] = info['prev']
                info['prev'] = bar.Close
        
        # Compute signals
        signals = {}
        for sym_str, info in self.basket.items():
            symbol = Symbol.Create(sym_str, SecurityType.Equity, Market.USA)
            if not data.ContainsKey(symbol):
                continue
            bar = data[symbol]
            # Check signal conditions
            if (info['prev_prev'] is not None and
                info['prev'] is not None and
                info['sma'].IsReady and
                bar.Close < info['prev'] and
                info['prev'] < info['prev_prev'] and
                bar.Close > info['sma'].Current.Value):
                signals[sym_str] = True
            else:
                signals[sym_str] = False
        
        # Determine weights (equal weight among signals)
        signal_count = sum(1 for v in signals.values() if v)
        if signal_count > 0:
            weight = 1.0 / signal_count
        else:
            weight = 0.0
        
        # Set holdings for all basket symbols
        for sym_str in self.basket:
            symbol = Symbol.Create(sym_str, SecurityType.Equity, Market.USA)
            if signals.get(sym_str, False) and signal_count > 0:
                self.SetHoldings(symbol, weight)
            else:
                # Only set to 0 if we have a position to avoid extra orders
                if self.Portfolio[symbol].Invested:
                    self.SetHoldings(symbol, 0.0)
