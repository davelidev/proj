class BaseSubAlgo:
    """
    Base class for sub-algorithms.
    Provides a template for initialize() and update_targets().
    """
    def __init__(self):
        self.symbols = []
        self.market_symbol = None
        self.lookback = 252  # typical number of trading days
        self.history = {}    # dict: symbol -> list of historical prices
        self.target_weights = {}

    def initialize(self):
        """Override to set up algorithm parameters."""
        raise NotImplementedError

    def update_targets(self):
        """Override to compute and return target weights."""
        raise NotImplementedError


class Algo135(BaseSubAlgo):
    """
    Beta scaling strategy: weight positions by inverse beta to market.
    Target weight for each symbol is proportional to 1/beta.
    """

    def initialize(self):
        """
        Set up trading universe and market benchmark.
        Must be called before update_targets.
        """
        # Example universe: a few stocks and the market (e.g., SPY)
        self.symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'META']
        self.market_symbol = 'SPY'
        self.lookback = 252  # use 1 year of trading days for beta

        # Pre-populate history with enough data (empty lists)
        for sym in self.symbols + [self.market_symbol]:
            self.history[sym] = []

    def _compute_returns(self, prices):
        """Calculate daily returns from a list of prices."""
        returns = []
        for i in range(1, len(prices)):
            if prices[i-1] != 0:
                returns.append((prices[i] - prices[i-1]) / prices[i-1])
            else:
                returns.append(0.0)
        return returns

    def _mean(self, data):
        """Arithmetic mean of a list."""
        return sum(data) / len(data) if data else 0.0

    def _covariance(self, x, y):
        """Compute covariance between two equal-length lists."""
        if len(x) != len(y) or len(x) == 0:
            return 0.0
        mean_x = self._mean(x)
        mean_y = self._mean(y)
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        return cov / len(x)

    def _variance(self, x):
        """Compute variance of a list."""
        if len(x) == 0:
            return 0.0
        mean_x = self._mean(x)
        var = sum((xi - mean_x) ** 2 for xi in x)
        return var / len(x)

    def _beta(self, asset_returns, market_returns):
        """
        Compute beta = Cov(asset_returns, market_returns) / Var(market_returns).
        Returns 1.0 if market variance is zero to avoid division by zero.
        """
        market_var = self._variance(market_returns)
        if market_var == 0:
            return 1.0
        cov = self._covariance(asset_returns, market_returns)
        return cov / market_var

    def update_targets(self):
        """
        Calculate target weights based on inverse beta scaling.
        Assumes sufficient price history exists in self.history.
        """
        # Ensure we have enough data for lookback period
        min_length = self.lookback + 1  # need at least lookback+1 prices for returns
        if any(len(self.history[sym]) < min_length for sym in self.symbols + [self.market_symbol]):
            # Not enough data; keep previous targets or set equal weights
            n = len(self.symbols)
            if n > 0:
                self.target_weights = {sym: 1.0 / n for sym in self.symbols}
            return

        # Extract returns for the last lookback days (most recent lookback periods)
        # For simplicity, use the last 'lookback' price changes
        market_prices = self.history[self.market_symbol][-self.lookback-1:]  # last lookback+1 prices
        market_returns = self._compute_returns(market_prices)

        betas = {}
        for sym in self.symbols:
            asset_prices = self.history[sym][-self.lookback-1:]
            asset_returns = self._compute_returns(asset_prices)
            beta = self._beta(asset_returns, market_returns)
            betas[sym] = beta

        # Compute inverse beta weights
        inv_betas = {}
        for sym, beta in betas.items():
            if beta == 0:
                # Avoid division by zero; assign a very high weight (capped)
                inv_betas[sym] = 1e6
            else:
                inv_betas[sym] = 1.0 / beta

        # Normalize weights to sum to 1.0
        total_inv_beta = sum(inv_betas.values())
        if total_inv_beta > 0:
            for sym in self.symbols:
                self.target_weights[sym] = inv_betas[sym] / total_inv_beta
        else:
            # Fallback to equal weights
            n = len(self.symbols)
            self.target_weights = {sym: 1.0 / n for sym in self.symbols}

        return self.target_weights
