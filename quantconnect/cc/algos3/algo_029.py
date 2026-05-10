from QuantConnect import *
from QuantConnect.Algorithm import *
from QuantConnect.Indicators import *
from QuantConnect.Data.UniverseSelection import *
from System.Collections.Generic import List
from datetime import timedelta

class SymbolData:
    """Holds price history and computes trendline signal for a single symbol."""
    def __init__(self, symbol, window_size=200):
        self.symbol = symbol
        self.window = RollingWindow[Decimal](window_size)
        self.pivot_window = 5  # lookback for pivot detection

    def update(self, bar):
        """Add a new TradeBar close to the window."""
        self.window.Add(bar.Close)

    def warm_up(self, history):
        """Pre-fill window with historical TradeBars."""
        for bar in history:
            self.window.Add(bar.Close)

    def is_ready(self, min_bars=50):
        """Check if enough data is available for signal computation."""
        return self.window.Count >= max(min_bars, 2 * self.pivot_window + 1)

    def _get_closes(self):
        """Return list of closes in chronological order (oldest first)."""
        return [self.window[i] for i in range(self.window.Count - 1, -1, -1)]

    def _find_pivots(self, closes):
        """
        Find pivot highs and lows using a rolling window.
        Returns (highs, lows) where each is a list of (index, price) tuples,
        sorted by index ascending.
        """
        highs = []
        lows = []
        n = len(closes)
        w = self.pivot_window
        for i in range(w, n - w):
            # Check if i is a local high
            if all(closes[i] >= closes[j] for j in range(i - w, i + w + 1) if j != i):
                highs.append((i, closes[i]))
            # Check if i is a local low
            if all(closes[i] <= closes[j] for j in range(i - w, i + w + 1) if j != i):
                lows.append((i, closes[i]))
        return highs, lows

    def get_signal(self):
        """
        Returns True if the most recent two pivot highs are ascending
        and the most recent two pivot lows are ascending.
        """
        closes = self._get_closes()
        highs, lows = self._find_pivots(closes)

        # Need at least 2 highs and 2 lows
        if len(highs) < 2 or len(lows) < 2:
            return False

        # Get the two most recent highs (by index, i.e. chronological order)
        last_two_highs = highs[-2:]   # oldest of the two first
        last_two_lows = lows[-2:]

        # Check ascending condition
        # Most recent (later) high/lows are at the end of the list
        return (last_two_highs[1][1] > last_two_highs[0][1] and
                last_two_lows[1][1] > last_two_lows[0][1])

class Algo029(QCAlgorithm):
    """Daily trading algorithm: trendline signal → long basket / TQQQ."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        # Primary asset
        self.AddEquity("TQQQ", Resolution.Daily)
        self.basket = {}  # symbol string -> SymbolData
        # Add TQQQ as part of basket for tracking
        tqqq_symbol = self.Symbol("TQQQ")
        self.basket["TQQQ"] = SymbolData(tqqq_symbol)

        # Universe selection: top 10 mega‑cap stocks
        self.AddUniverse(self.CoarseSelectionFunction)

        # Warm up with enough data for pivot detection
        self.SetWarmUp(100, Resolution.Daily)

    def CoarseSelectionFunction(self, coarse):
        """Select top 10 stocks by market cap."""
        filtered = [c for c in coarse if c.HasFundamentalData]
        sorted_by_mc = sorted(filtered, key=lambda c: c.MarketCap, reverse=True)
        return [c.Symbol for c in sorted_by_mc[:10]]

    def OnSecuritiesChanged(self, changes):
        """Handle additions/removals from the universe."""
        # Add new symbols
        added = [s.Symbol for s in changes.AddedSecurities
                 if s.Symbol.Value != "TQQQ"]   # exclude TQQQ (already handled)
        for symbol in added:
            if symbol.Value in self.basket:
                continue   # already present
            # Add the equity to the algorithm
            self.AddEquity(symbol.Value, Resolution.Daily)
            # Create data container and fill history
            data = SymbolData(symbol)
            history = self.History(symbol, 150, Resolution.Daily)
            if not history.empty:
                # History returns multi-index, iterate over rows
                for time, row in history.iterrows():
                    # We need to create a TradeBar-like object; use a simple bar
                    # Since we only store closes, just use the close value
                    data.window.Add(row["close"])
            self.basket[symbol.Value] = data

        # Remove symbols no longer in universe
        removed = [s.Symbol for s in changes.RemovedSecurities
                   if s.Symbol.Value != "TQQQ"]
        for symbol in removed:
            if symbol.Value in self.basket:
                self.Liquidate(symbol)
                del self.basket[symbol.Value]

    def OnData(self, data):
        """Daily rebalance: allocate to symbols with positive trendline signal."""
        if self.IsWarmingUp:
            return

        # Update all basket symbols with today's data
        for sym_str, sym_data in self.basket.items():
            if data.ContainsKey(sym_data.symbol):
                bar = data[sym_data.symbol]
                sym_data.update(bar)

        # Compute signals
        signals = {}
        for sym_str, sym_data in self.basket.items():
            if sym_data.is_ready():
                signals[sym_data.symbol] = sym_data.get_signal()
            else:
                signals[sym_data.symbol] = False

        # Count positive signals
        active_symbols = [sym for sym, sig in signals.items() if sig]
        num_active = len(active_symbols)

        # Set target weights
        if num_active > 0:
            target_weight = 1.0 / num_active
            for sym in signals:
                if signals[sym]:
                    self.SetHoldings(sym, target_weight)
                else:
                    self.SetHoldings(sym, 0)
        else:
            # No signal – liquidate all
            for sym in signals:
                self.SetHoldings(sym, 0)