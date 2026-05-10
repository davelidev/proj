class Algo189(BaseSubAlgo):
    """
    Fama-French three-factor model: size (market cap), value (book-to-market), momentum (past 12m returns excl. last month).
    """

    def initialize(self):
        # Factor lookback parameters
        self.momentum_period = 252          # ~12 months of trading days
        self.momentum_skip = 21             # skip last month (21 days)
        self.value_lookback = None          # use latest book value
        self.target_number = 50             # number of stocks to hold long
        self.targets = {}                   # output: ticker -> weight

    def update_targets(self):
        # --- Data retrieval (assumed from base class) ---
        tickers = self.get_universe()       # list of ticker strings

        size_scores = {}
        value_scores = {}
        momentum_scores = {}

        for ticker in tickers:
            # 1. Size factor: negative log(market cap) → small caps score higher
            mcap = self.get_market_cap(ticker)
            if mcap > 0:
                size_scores[ticker] = -1.0 * mcap   # or use log(mcap)
            else:
                size_scores[ticker] = 0

            # 2. Value factor: book-to-market ratio
            bv = self.get_book_value(ticker)
            if mcap > 0:
                value_scores[ticker] = bv / mcap
            else:
                value_scores[ticker] = 0

            # 3. Momentum factor: return over [t-(12+1) months, t-1 month]
            lookback = self.momentum_period + self.momentum_skip
            prices = self.get_price_history(ticker, lookback)
            if len(prices) >= lookback:
                start_price = prices[0]
                end_price = prices[self.momentum_skip]      # price before skip period
                momentum_scores[ticker] = (end_price / start_price) - 1
            else:
                momentum_scores[ticker] = 0

        # --- Rank each factor (higher value -> higher rank, 0..N-1) ---
        def _rank(scores_dict):
            sorted_vals = sorted(scores_dict.values())
            rank_map = {v: i for i, v in enumerate(sorted_vals)}
            return {ticker: rank_map[scores_dict[ticker]] for ticker in scores_dict}

        size_ranks = _rank(size_scores)
        value_ranks = _rank(value_scores)
        momentum_ranks = _rank(momentum_scores)

        # --- Combine ranks (equal weight) ---
        combined = {}
        for t in tickers:
            combined[t] = size_ranks[t] + value_ranks[t] + momentum_ranks[t]

        # --- Select top N stocks ---
        sorted_tickers = sorted(combined, key=combined.get, reverse=True)
        selected = sorted_tickers[:self.target_number]

        # --- Assign equal weights to selected stocks ---
        weight = 1.0 / len(selected) if selected else 0
        self.targets = {ticker: weight for ticker in selected}
