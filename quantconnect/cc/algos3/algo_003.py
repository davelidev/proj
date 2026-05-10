from AlgorithmImports import *
from collections import deque

class Algo003(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        # Always add TQQQ
        self.tqqq = self.AddEquity('TQQQ', Resolution.Daily).Symbol

        # Basket dict: symbol -> { 'atr': ATR indicator, 'highs': deque, 'lows': deque }
        self.basket = {}
        self.InitSymbol(self.tqqq)

        # Universe for top-10 market cap stocks
        self.AddUniverse(self.CoarseSelectionFunction, self.FineSelectionFunction)

    def CoarseSelectionFunction(self, coarse):
        # Basic liquidity filter
        return [c.Symbol for c in coarse if c.HasFundamentalData and c.AdjustedPrice > 5]

    def FineSelectionFunction(self, fine):
        # Sort by market cap descending and take top 10
        sorted_fine = sorted(fine, key=lambda f: f.MarketCap, reverse=True)
        top10 = [f.Symbol for f in sorted_fine[:10]]
        return top10

    def OnSecuritiesChanged(self, changes):
        # Add new symbols
        for added in changes.AddedSecurities:
            sym = added.Symbol
            if sym not in self.basket:
                self.InitSymbol(sym)
        # Remove old symbols (liquidate first)
        for removed in changes.RemovedSecurities:
            sym = removed.Symbol
            if sym in self.basket:
                self.SetHoldings(sym, 0)
                del self.basket[sym]

    def InitSymbol(self, symbol):
        atr = self.ATR(symbol, 14, Resolution.Daily)
        highs = deque(maxlen=20)
        lows = deque(maxlen=20)
        self.basket[symbol] = {
            'atr': atr,
            'highs': highs,
            'lows': lows
        }

    def OnData(self, data):
        # Update rolling highs/lows and ATR
        for sym, info in self.basket.items():
            if data.ContainsKey(sym) and data[sym] is not None:
                bar = data[sym]
                if bar.Close != 0:
                    info['highs'].append(bar.High)
                    info['lows'].append(bar.Low)

        # Compute signals
        signals = {}
        for sym, info in self.basket.items():
            if len(info['highs']) >= 20 and info['atr'].IsReady:
                if data.ContainsKey(sym) and data[sym] is not None:
                    bar = data[sym]
                    high_max = max(info['highs'])
                    low_min = min(info['lows'])
                    atr_val = info['atr'].Current.Value
                    if bar.Close > high_max + 1.5 * atr_val:
                        signals[sym] = 1   # long
                    elif bar.Close < low_min - 1.5 * atr_val:
                        signals[sym] = -1  # short
                    else:
                        signals[sym] = 0
            else:
                signals[sym] = 0

        # Determine active signals
        active = {sym: dir for sym, dir in signals.items() if dir != 0}
        total = len(active)
        if total > 0:
            weight = 1.0 / total
            for sym, dir in active.items():
                self.SetHoldings(sym, dir * weight)
        else:
            # No signals -> flat
            for sym in self.basket:
                self.SetHoldings(sym, 0)
