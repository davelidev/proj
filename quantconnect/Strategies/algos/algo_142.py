class Algo142(BaseSubAlgo):
    """
    Strategy: Select assets whose signals have the highest Information Coefficient (IC).
    IC is computed as the rolling correlation between predicted signals and subsequent returns.
    """

    def initialize(self):
        """
        Set strategy parameters and initialize data structures.
        """
        # Number of top assets to select based on IC
        self.top_n = 20

        # Lookback window for IC calculation (number of periods)
        self.lookback = 60

        # Minimum number of observations required to compute a valid IC
        self.min_obs = 20

        # Dictionary to store historical signals and returns for each asset.
        # Format: {asset: {'signals': [float], 'returns': [float]}} (ordered list, oldest first)
        self.history = {asset: {'signals': [], 'returns': []} for asset in self.assets}

    def update_targets(self):
        """
        For each asset, compute the IC (Pearson correlation) between recent signals and forward returns.
        Select the top_n assets with the highest IC and set them as targets.
        """
        ic_scores = {}

        for asset in self.assets:
            # Get current signal (e.g., predicted return or factor value)
            current_signal = self.get_current_signal(asset)

            # Get the return for the next period (would be known only after one period, but we assume it's available
            # in a backtesting context; here we store it as realized return for the current period)
            # In real implementation, we would shift returns: signal[t] vs return[t+1]
            # For simplicity, we assume self.get_period_return(asset) gives the return for the period just ended.
            current_return = self.get_period_return(asset)

            # Append to history
            hist = self.history[asset]
            hist['signals'].append(current_signal)
            hist['returns'].append(current_return)

            # Trim history to lookback
            if len(hist['signals']) > self.lookback:
                hist['signals'].pop(0)
                hist['returns'].pop(0)

            # Compute IC if enough observations
            if len(hist['signals']) >= self.min_obs:
                signals = hist['signals']
                returns = hist['returns']
                n = len(signals)

                # Manual Pearson correlation calculation
                mean_signal = sum(signals) / n
                mean_return = sum(returns) / n

                cov = sum((s - mean_signal) * (r - mean_return) for s, r in zip(signals, returns))
                var_signal = sum((s - mean_signal) ** 2 for s in signals)
                var_return = sum((r - mean_return) ** 2 for r in returns)

                # Avoid division by zero
                if var_signal > 0 and var_return > 0:
                    ic = cov / ((var_signal * var_return) ** 0.5)
                else:
                    ic = 0.0

                ic_scores[asset] = ic
            else:
                ic_scores[asset] = 0.0  # Not enough data, treat as low IC

        # Sort assets by IC descending and select top_n
        sorted_assets = sorted(ic_scores.items(), key=lambda x: x[1], reverse=True)
        self.targets = [asset for asset, _ in sorted_assets[:self.top_n]]

    # ==========================================
    # Placeholder methods – to be supplied by the framework or overridden.
    # They represent the interface this algorithm expects from the base class.
    # ==========================================
    def get_current_signal(self, asset):
        """
        This method should return the latest predicted signal (e.g., factor value, model score).
        In practice, this would be defined by the base class or the user.
        """
        raise NotImplementedError("Subclass must implement get_current_signal")

    def get_period_return(self, asset):
        """
        This method should return the realized return for the current period.
        In backtesting, this might be the return of the asset over the same period the signal was generated.
        """
        raise NotImplementedError("Subclass must implement get_period_return")
