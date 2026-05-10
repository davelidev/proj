class Algo132(BaseSubAlgo):
    """
    Volatility-adjusted RSI strategy:
    Scale RSI overbought/oversold thresholds based on recent volatility.
    """

    def initialize(self):
        """Set strategy parameters."""
        # RSI period
        self.rsi_period = 14
        # Volatility calculation period (for standard deviation of returns)
        self.vol_period = 20
        # Base RSI levels (without vol adjustment)
        self.base_rsi_overbought = 70
        self.base_rsi_oversold = 30
        # How strongly the bands react to volatility changes
        self.vol_scaling_factor = 0.5
        # Baseline volatility (expected daily standard deviation)
        self.baseline_vol = 0.01
        # Ensure we have enough data before generating signals
        self.min_data_length = max(self.rsi_period, self.vol_period) + 1
        # Signal placeholder
        self.signal = 0

    def update_targets(self):
        """
        Calculate RSI and volatility, adjust thresholds, and set a signal.
        Requires self.prices to be a list of recent closing prices (newest last).
        Sets self.signal to 1 (buy), -1 (sell), or 0 (neutral).
        """
        prices = self.prices
        if len(prices) < self.min_data_length:
            return

        # Compute daily returns
        returns = []
        for i in range(1, len(prices)):
            if prices[i-1] == 0:
                return  # avoid division by zero
            returns.append((prices[i] - prices[i-1]) / prices[i-1])

        # Recent volatility (standard deviation of returns over vol_period)
        recent_returns = returns[-self.vol_period:]
        mean_r = sum(recent_returns) / len(recent_returns)
        variance = sum((r - mean_r) ** 2 for r in recent_returns) / len(recent_returns)
        vol = variance ** 0.5

        # RSI calculation using the last rsi_period + 1 prices
        rsi_prices = prices[-(self.rsi_period + 1):]
        gains = []
        losses = []
        for i in range(1, len(rsi_prices)):
            diff = rsi_prices[i] - rsi_prices[i-1]
            if diff > 0:
                gains.append(diff)
                losses.append(0.0)
            else:
                gains.append(0.0)
                losses.append(abs(diff))

        avg_gain = sum(gains[-self.rsi_period:]) / self.rsi_period
        avg_loss = sum(losses[-self.rsi_period:]) / self.rsi_period

        if avg_loss == 0:
            rsi = 100.0
        else:
            rs = avg_gain / avg_loss
            rsi = 100.0 - (100.0 / (1.0 + rs))

        # Adjust RSI thresholds based on volatility deviation from baseline
        if self.baseline_vol == 0:
            vol_factor = 0.0
        else:
            vol_factor = self.vol_scaling_factor * (vol - self.baseline_vol) / self.baseline_vol

        overbought = self.base_rsi_overbought * (1.0 + vol_factor)
        oversold   = self.base_rsi_oversold * (1.0 - vol_factor)

        # Clamp thresholds to reasonable ranges
        overbought = min(overbought, 90.0)
        oversold   = max(oversold, 10.0)

        # Generate signal
        if rsi > overbought:
            self.signal = -1
        elif rsi < oversold:
            self.signal = 1
        else:
            self.signal = 0
