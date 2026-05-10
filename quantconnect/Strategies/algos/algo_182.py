class Algo182(BaseSubAlgo):
    """
    Sharpe maximization strategy: selects assets with the highest Sharpe ratio.
    Inherits from BaseSubAlgo (assumed to provide self.symbols and self.historical_data).
    """

    def initialize(self):
        """
        Set up strategy parameters.
        """
        # Lookback period for Sharpe calculation (e.g., 252 trading days)
        self.lookback = 252
        # Number of top assets to hold
        self.top_n = 5
        # Risk-free rate (annualized, e.g., 0.03 for 3%)
        self.risk_free_rate = 0.03

    def update_targets(self):
        """
        Compute Sharpe ratios for each symbol and set target allocations.
        """
        # Retrieve latest available historical data for all symbols
        # Assumes self.historical_data is a dict: {symbol: list/array of prices or returns}
        # Here we assume it contains daily close prices in chronological order.
        # We'll use the last 'lookback' days for calculation.
        
        sharpe_ratios = {}
        for symbol, prices in self.historical_data.items():
            if len(prices) < self.lookback + 1:
                continue  # not enough data

            # Use the most recent 'lookback' daily returns
            recent_prices = prices[-self.lookback-1:]  # need one extra for return calc
            returns = [(recent_prices[i+1] / recent_prices[i]) - 1 for i in range(len(recent_prices)-1)]

            # Calculate mean and std of daily returns
            mean_daily_return = sum(returns) / len(returns)
            variance = sum((r - mean_daily_return) ** 2 for r in returns) / len(returns)
            std_daily_return = variance ** 0.5

            if std_daily_return == 0:
                sharpe_ratios[symbol] = 0
            else:
                # Annualized Sharpe: (mean_daily * 252 - risk_free_rate) / (std_daily * sqrt(252))
                annualized_mean = mean_daily_return * 252
                annualized_std = std_daily_return * (252 ** 0.5)
                sharpe = (annualized_mean - self.risk_free_rate) / annualized_std
                sharpe_ratios[symbol] = sharpe

        # Sort by Sharpe descending and select top N
        sorted_symbols = sorted(sharpe_ratios, key=sharpe_ratios.get, reverse=True)
        selected = sorted_symbols[:self.top_n]

        # Create equal‑weight targets (fractions sum to 1)
        if selected:
            weight = 1.0 / len(selected)
            targets = {sym: weight for sym in selected}
        else:
            targets = {}

        # Store target weights (assumes BaseSubAlgo has self.targets or similar attribute)
        self.targets = targets
