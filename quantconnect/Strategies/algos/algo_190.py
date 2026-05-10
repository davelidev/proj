class Algo190(BaseSubAlgo):
    """
    Carhart 4-Factor Strategy – Momentum Addition.
    Implements a multi‑factor allocation that overweights assets with positive momentum.
    """

    def initialize(self):
        # --- Factor model parameters ---
        self.momentum_lookback = 252 * 12      # 12 months of daily data
        self.momentum_skip = 21                # skip last month (21 trading days)
        self.factor_exposure = {
            'market': 1.0,
            'size': 0.0,       # neutral SMB
            'value': 0.0,      # neutral HML
            'momentum': 0.3    # target momentum factor loading
        }
        # Rebalance every 21 trading days (≈ monthly)
        self.rebalance_freq = 21
        self.days_since_rebalance = 0

        # Placeholder for target weights (security → weight)
        self.target_weights = {}

    def update_targets(self, data):
        """
        Update target portfolio weights using Carhart momentum signal.

        Parameters
        ----------
        data : dict
            Expected to contain:
            - 'securities': list of security identifiers
            - 'returns': dict {security: list of daily returns} (most recent last)
            - 'factor_loadings': dict {security: dict} (optional, for completeness)
        """
        securities = data.get('securities', [])
        returns = data.get('returns', {})

        # Count how many returns are needed
        req_len = self.momentum_lookback + self.momentum_skip

        # Compute raw momentum score (cumulative return over lookback, excluding last month)
        momentum_scores = {}
        for sec in securities:
            r = returns.get(sec, [])
            if len(r) >= req_len:
                # Sum daily returns from [ -lookback : -skip ]
                mom_return = sum(r[-self.momentum_lookback : -self.momentum_skip])
            else:
                mom_return = 0.0
            momentum_scores[sec] = mom_return

        # Convert scores to weights: rank normalisation / softmax (example: linear scaling)
        # Here we simply assign equal weight, then tilt proportionally to momentum
        n = len(securities)
        if n == 0:
            self.target_weights = {}
            return

        base_weight = 1.0 / n
        max_abs_mom = max(abs(s) for s in momentum_scores.values()) or 1.0

        total_weight = 0.0
        raw_weights = {}
        for sec in securities:
            # Tilt: add a fraction proportional to normalised momentum
            tilt = (momentum_scores[sec] / max_abs_mom) * 0.1  # max 10% deviation
            w = base_weight + tilt
            raw_weights[sec] = max(w, 0.0)   # no shorting
            total_weight += raw_weights[sec]

        # Normalise so weights sum to 1
        self.target_weights = {
            sec: w / total_weight for sec, w in raw_weights.items()
        }

        # Optionally enforce target factor exposures (omitted for brevity)
        # In a full implementation you would regress returns on factors and neutralise.
