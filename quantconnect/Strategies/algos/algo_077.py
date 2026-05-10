class Algo077(BaseSubAlgo):
    """
    Strategy: Top-3 sectors by momentum, only if basket volatility < 30%.
    Allocates equally to the top 3 sector ETFs when the equally-weighted
    basket of those sectors has annualized volatility below 30%.
    Otherwise, holds cash (all weights set to 0).
    """
    def initialize(self):
        # List of common US sector ETFs
        sectors = [
            "XLB",  # Materials
            "XLE",  # Energy
            "XLF",  # Financials
            "XLI",  # Industrials
            "XLK",  # Technology
            "XLP",  # Consumer Staples
            "XLRE", # Real Estate
            "XLU",  # Utilities
            "XLV",  # Health Care
            "XLY",  # Consumer Discretionary
        ]
        for sym in sectors:
            self.AddEquity(sym)

    def update_targets(self):
        # Lookback periods
        MOMENTUM_DAYS = 20
        VOL_LOOKBACK_DAYS = 252

        # 1. Collect prices and compute momentum for each sector
        sector_data = {}  # symbol -> {price, hist}
        for sym in self.Securities:
            security = self.Securities[sym]
            # Get historical close prices (list of float)
            hist = self.History(sym, MOMENTUM_DAYS, "close")
            if hist is None or len(hist) < MOMENTUM_DAYS:
                continue
            # Current price is last element
            current_price = hist[-1]
            past_price = hist[0]
            momentum = (current_price - past_price) / past_price
            sector_data[sym] = {
                "momentum": momentum,
                "price_hist": hist  # full history for vol calculation
            }

        if len(sector_data) < 3:
            self.targets = {}
            return

        # 2. Sort by momentum descending, take top 3
        sorted_sectors = sorted(
            sector_data.items(),
            key=lambda x: x[1]["momentum"],
            reverse=True
        )
        top3 = [sym for sym, _ in sorted_sectors[:3]]

        # 3. Compute basket volatility
        # Gather daily returns for each of the top 3 over VOL_LOOKBACK_DAYS
        # Need enough history: at least VOL_LOOKBACK_DAYS+1 for returns
        vol_hist_len = VOL_LOOKBACK_DAYS + 1
        returns_list = {sym: [] for sym in top3}
        for sym in top3:
            # Get longer history from the same data, but may need separate call
            # If we don't have enough, fallback to shorter
            long_hist = self.History(sym, vol_hist_len, "close")
            if long_hist is None or len(long_hist) < vol_hist_len:
                # Not enough data, skip vol calculation (vol assumed high)
                self.targets = {}
                return
            for i in range(1, len(long_hist)):
                ret = (long_hist[i] - long_hist[i-1]) / long_hist[i-1]
                returns_list[sym].append(ret)

        # Daily portfolio returns (equal weight among top3)
        portfolio_returns = []
        for i in range(len(returns_list[top3[0]])):
            daily_ret = 0.0
            for sym in top3:
                daily_ret += returns_list[sym][i]
            portfolio_returns.append(daily_ret / 3.0)

        # Compute standard deviation (population sample)
        mean_ret = sum(portfolio_returns) / len(portfolio_returns)
        variance = sum((r - mean_ret)**2 for r in portfolio_returns) / len(portfolio_returns)
        daily_vol = variance ** 0.5
        annualized_vol = daily_vol * (252 ** 0.5)

        # 4. Set targets
        if annualized_vol < 0.30:
            weight = 1.0 / 3
            self.targets = {sym: weight for sym in top3}
        else:
            # Vol too high – go to cash (zero weights)
            self.targets = {}
