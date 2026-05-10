class Algo153(BaseSubAlgo):
    """
    Counter-trend strategy using RSI divergence fading.
    Detects bullish/bearish divergences between price and RSI and enters
    positions in the direction opposite to the prevailing trend (fade).
    """

    def initialize(self):
        """Initialize parameters and data structures."""
        # RSI period
        self.rsi_period = 14
        # Lookback window for detecting swing highs/lows (in bars)
        self.swing_window = 5
        # Minimum number of bars between divergent pivots
        self.min_gap = 5

        # Store historical prices and RSI values per symbol
        self.history = {}  # symbol -> dict with 'close', 'rsi', 'high', 'low'

        # Keep track of last detected divergence signals (to avoid re-entry)
        self.last_signal = {}  # symbol -> 'bullish' or 'bearish' or None

    def update_targets(self):
        """
        Update trading targets based on RSI divergence detection.
        Called on each bar.
        """
        for symbol in self.symbols:
            # Ensure we have enough data
            if symbol not in self.history:
                self.history[symbol] = {
                    'close': [],
                    'high': [],
                    'low': [],
                    'rsi': []
                }

            # Fetch current bar (assume self.data[symbol] has OHLC)
            bar = self.data[symbol]
            close = bar.close
            high = bar.high
            low = bar.low

            # Update historical lists
            self.history[symbol]['close'].append(close)
            self.history[symbol]['high'].append(high)
            self.history[symbol]['low'].append(low)

            # Compute RSI if we have enough data
            closes = self.history[symbol]['close']
            if len(closes) > self.rsi_period:
                rsi_value = self._compute_rsi(closes[-self.rsi_period-1:], self.rsi_period)
                self.history[symbol]['rsi'].append(rsi_value)
            else:
                # Not enough data yet
                continue

            # Need at least two full RSI periods and some extra bars for pivots
            if len(closes) < self.rsi_period + self.swing_window * 2 + self.min_gap:
                continue

            # Detect divergence
            signal = self._check_divergence(symbol)

            # Set target based on signal (counter‑trend fade)
            if signal == 'bullish_divergence':
                # Price making lower low, RSI making higher low → upward reversal expected
                # Counter‑trend: go long
                self.set_target(symbol, 1.0)  # 100% long
                self.last_signal[symbol] = 'bullish'
            elif signal == 'bearish_divergence':
                # Price making higher high, RSI making lower high → downward reversal expected
                # Counter‑trend: go short
                self.set_target(symbol, -1.0)  # 100% short
                self.last_signal[symbol] = 'bearish'
            else:
                # No clear new divergence – if we had a signal maintain it? Or go flat.
                # Let's hold current position unless a new opposite signal appears.
                # For simplicity, we keep the previous target (if any) unchanged.
                # If you want to exit, set target to 0.
                pass

    def _compute_rsi(self, prices, period):
        """
        Compute RSI for a list of prices (last element is current).
        Uses Wilder's smoothing method.
        """
        if len(prices) < period + 1:
            return None

        # First average gain/loss over initial period
        gains = []
        losses = []
        for i in range(1, period + 1):
            diff = prices[i] - prices[i-1]
            gains.append(max(diff, 0))
            losses.append(max(-diff, 0))
        avg_gain = sum(gains) / period
        avg_loss = sum(losses) / period

        # Then smooth for the rest of the prices (if any)
        for i in range(period + 1, len(prices)):
            diff = prices[i] - prices[i-1]
            gain = max(diff, 0)
            loss = max(-diff, 0)
            avg_gain = (avg_gain * (period - 1) + gain) / period
            avg_loss = (avg_loss * (period - 1) + loss) / period

        if avg_loss == 0:
            return 100.0
        rs = avg_gain / avg_loss
        return 100.0 - (100.0 / (1.0 + rs))

    def _check_divergence(self, symbol):
        """
        Check for RSI divergence on the given symbol.
        Returns 'bullish_divergence', 'bearish_divergence', or None.
        """
        data = self.history[symbol]
        closes = data['close']
        highs = data['high']
        lows = data['low']
        rsis = data['rsi']

        # Find the most recent swing high and swing low (using high/low prices)
        # We'll use a simple approach: look back `swing_window` bars for local extremes
        n = len(closes)
        if n < self.swing_window * 2 + self.min_gap:
            return None

        # Index of last bar (current)
        cur_idx = n - 1

        # Find last swing high (a bar higher than its left and right neighbors within window)
        last_high_idx = None
        last_high_price = None
        for i in range(cur_idx - self.swing_window, cur_idx - self.min_gap):
            if i < self.swing_window:
                continue
            left = highs[i - self.swing_window:i]
            right = highs[i+1:i+1+self.swing_window]
            if highs[i] > max(left) and highs[i] > max(right):
                last_high_idx = i
                last_high_price = highs[i]
                break

        # Find last swing low
        last_low_idx = None
        last_low_price = None
        for i in range(cur_idx - self.swing_window, cur_idx - self.min_gap):
            if i < self.swing_window:
                continue
            left = lows[i - self.swing_window:i]
            right = lows[i+1:i+1+self.swing_window]
            if lows[i] < min(left) and lows[i] < min(right):
                last_low_idx = i
                last_low_price = lows[i]
                break

        if last_high_idx is None or last_low_idx is None:
            return None

        # Get RSI values at those pivot points
        try:
            rsi_at_last_high = rsis[last_high_idx]
            rsi_at_last_low = rsis[last_low_idx]
        except IndexError:
            return None

        # Current RSI and price
        current_close = closes[-1]
        current_rsi = rsis[-1]
        current_high = highs[-1]
        current_low = lows[-1]

        # --- Bearish Divergence ---
        # Price makes higher high, but RSI makes lower high
        # Compare current high with last swing high
        if current_high > last_high_price and current_rsi < rsi_at_last_high:
            # Also ensure we haven't already acted on this divergence
            if self.last_signal.get(symbol) != 'bearish':
                return 'bearish_divergence'

        # --- Bullish Divergence ---
        # Price makes lower low, but RSI makes higher low
        if current_low < last_low_price and current_rsi > rsi_at_last_low:
            if self.last_signal.get(symbol) != 'bullish':
                return 'bullish_divergence'

        return None
