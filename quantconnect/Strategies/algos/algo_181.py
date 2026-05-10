class Algo181(BaseSubAlgo):
    """
    Risk-parity strategy: weights are proportional to inverse volatility.
    """

    def initialize(self):
        """
        Initialize the algorithm. Set parameters for volatility estimation.
        """
        self.volatility_window = 20  # lookback period for rolling volatility
        self.price_history = {}      # dict: symbol -> list of recent prices

    def update_targets(self):
        """
        Compute and set portfolio target weights based on inverse volatility.
        Assumes self.symbols contains the list of trading symbols.
        Updates self.target_weights (dict: symbol -> weight).
        """
        symbols = self.symbols
        if not symbols:
            self.target_weights = {}
            return

        # Compute volatility for each symbol using the latest available prices
        volatilities = {}
        for sym in symbols:
            prices = self.price_history.get(sym, [])
            if len(prices) < self.volatility_window + 1:
                # Not enough data: fall back to equal weight? Here we treat as high vol.
                volatilities[sym] = float('inf')
            else:
                # Use last 'volatility_window' returns (simple returns)
                recent = prices[-self.volatility_window - 1:]
                returns = [(recent[i] - recent[i-1]) / recent[i-1] for i in range(1, len(recent))]
                mean = sum(returns) / len(returns)
                variance = sum((r - mean)**2 for r in returns) / len(returns)
                volatilities[sym] = variance ** 0.5

        # Compute inverse volatility weights
        inv_vol = {}
        total_inv = 0.0
        for sym in symbols:
            vol = volatilities[sym]
            if vol == 0 or vol == float('inf'):
                inv = 0.0
            else:
                inv = 1.0 / vol
            inv_vol[sym] = inv
            total_inv += inv

        # Normalize to sum to 1
        if total_inv == 0:
            # Fallback: equal weight
            weight = 1.0 / len(symbols)
            self.target_weights = {sym: weight for sym in symbols}
        else:
            self.target_weights = {sym: inv_vol[sym] / total_inv for sym in symbols}
