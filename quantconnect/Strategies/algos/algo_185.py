class BaseSubAlgo:
    """Minimal base class for demonstration."""
    def __init__(self):
        self.prices = {}               # symbol -> list of prices (latest last)
        self.benchmark_prices = []     # list of benchmark prices (latest last)
        self.available_assets = []     # list of symbols
        self.target_weights = {}       # symbol -> weight (output)

class Algo185(BaseSubAlgo):
    """
    Treynor Index Strategy:
    Excess return per unit of systematic risk (beta).
    Select top assets by Treynor ratio and weight equally.
    """

    def initialize(self):
        """Set strategy parameters."""
        self.lookback = 60             # number of periods for return/beta calc
        self.risk_free_rate = 0.0      # annualized risk-free rate (simplified)
        self.top_n = 5                 # number of assets to hold
        self.min_periods = 20          # minimum data points required

    def update_targets(self):
        """Compute Treynor indices and update target weights."""
        if len(self.benchmark_prices) < self.lookback:
            return  # not enough data

        # Compute benchmark return over lookback period
        bm_prices = self.benchmark_prices[-self.lookback:]
        bm_returns = [(bm_prices[i] - bm_prices[i-1]) / bm_prices[i-1]
                      for i in range(1, len(bm_prices))]

        if len(bm_returns) < self.min_periods or sum(bm_returns) == 0:
            return

        treynor_scores = {}

        for symbol in self.available_assets:
            if symbol not in self.prices:
                continue
            prices = self.prices[symbol]
            if len(prices) < self.lookback:
                continue
            prices = prices[-self.lookback:]

            # Compute asset returns over same window
            asset_returns = [(prices[i] - prices[i-1]) / prices[i-1]
                             for i in range(1, len(prices))]
            if len(asset_returns) < self.min_periods:
                continue

            # Calculate mean excess return (simple average)
            avg_return = sum(asset_returns) / len(asset_returns)
            avg_bm_return = sum(bm_returns) / len(bm_returns)
            # Beta = Cov(Ri, Rm) / Var(Rm)
            # using basic statistics
            n = len(asset_returns)
            cov = sum((asset_returns[i] - avg_return) * (bm_returns[i] - avg_bm_return)
                      for i in range(n)) / n
            var_bm = sum((r - avg_bm_return)**2 for r in bm_returns) / n

            if var_bm == 0:
                beta = 0
            else:
                beta = cov / var_bm

            # Excess return (assume risk-free rate is 0 for simplicity)
            excess_return = avg_return - self.risk_free_rate
            if beta <= 0:
                continue  # avoid negative or zero beta assets
            treynor = excess_return / beta
            treynor_scores[symbol] = treynor

        if not treynor_scores:
            self.target_weights = {}
            return

        # Select top N symbols by Treynor score
        sorted_symbols = sorted(treynor_scores, key=treynor_scores.get, reverse=True)
        selected = sorted_symbols[:self.top_n]

        # Equal weight among selected
        weight = 1.0 / len(selected) if selected else 0.0
        self.target_weights = {sym: weight for sym in selected}
