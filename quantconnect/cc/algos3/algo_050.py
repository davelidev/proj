class Algo050(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        # Core asset
        self.tqqq = self.AddEquity('TQQQ', Resolution.Daily).Symbol

        # Dynamic universe: top 10 mega‑cap stocks
        self.AddUniverse(self.CoarseSelectionFunction, self.FineSelectionFunction)
        self.UniverseSettings.Resolution = Resolution.Daily

        # Store basket symbols (excluding TQQQ)
        self.basket = {}      # symbol -> None (placeholder)
        self.symbols = []     # list of active basket symbols

        # Warm up to let indicators stabilise
        self.SetWarmup(200, Resolution.Daily)

        # Storage for correlation indicators and daily returns
        self.corr_indicators = {}      # symbol -> Correlation(60)
        self.returns_roc = {}          # symbol -> RateOfChange(1)

        # Seasonality cache
        self.month_avg_ret = None      # pre‑computed average return per month

    # ---------------------------------------------------------------
    # Universe selection
    # ---------------------------------------------------------------
    def CoarseSelectionFunction(self, coarse):
        if self.Time.date() < datetime(2014, 1, 1).date():
            return []
        # Filter for fundamental data and reasonable price
        filtered = [c for c in coarse if c.HasFundamentalData and c.Price > 5]
        # Get top 10 by market cap
        sorted_coarse = sorted(filtered, key=lambda c: c.MarketCap, reverse=True)
        return [c.Symbol for c in sorted_coarse[:10]]

    def FineSelectionFunction(self, fine):
        # No further filtering needed
        return [f.Symbol for f in fine]

    # ---------------------------------------------------------------
    # Securities changed – update basket and indicators
    # ---------------------------------------------------------------
    def OnSecuritiesChanged(self, changes):
        # Remove obsolete symbols
        for symbol in changes.RemovedSecurities:
            if symbol in self.basket:
                del self.basket[symbol]
                if symbol in self.corr_indicators:
                    del self.corr_indicators[symbol]
                if symbol in self.returns_roc:
                    del self.returns_roc[symbol]

        # Add new symbols
        for symbol in changes.AddedSecurities:
            # Only consider equity symbols (exclude TQQQ itself)
            if symbol.Value == 'TQQQ':
                continue
            self.basket[symbol] = None
            self.symbols.append(symbol)

            # Create indicators – Correlation needs two inputs (TQQQ and basket stock)
            self.corr_indicators[symbol] = Correlation(60)
            self.returns_roc[symbol] = RateOfChange(1)

    # ---------------------------------------------------------------
    # Daily rebalance
    # ---------------------------------------------------------------
    def OnData(self, data):
        # Wait until warmup is finished
        if self.IsWarmingUp:
            return

        # 1. Compute HMA regime for TQQQ
        hma_value = self.compute_HMA(self.tqqq, 50)
        current_price = self.Securities[self.tqqq].Close
        if hma_value == 0:
            return

        # Slope of HMA over last 5 days (proxy)
        hma_prev = self.compute_HMA(self.tqqq, 50, lookback=5)
        slope = (hma_value - hma_prev) / 5.0

        # Regime classification
        if current_price > hma_value and slope > 0:
            regime = 'bull'
        elif current_price < hma_value and slope < 0:
            regime = 'bear'
        else:
            regime = 'choppy'

        # 2. Base exposure per regime
        base_exposure = {
            'bull': 0.9,
            'bear': 0.2,
            'choppy': 0.5
        }.get(regime, 0.5)

        # 3. Advanced quant signals
        #   3a. Correlation signal
        avg_corr = self.compute_avg_correlation()
        corr_penalty = 0  # adjust if correlations are extreme
        if avg_corr is not None:
            # If correlations are very high (>0.8) or very low (<0.2), reduce exposure
            if avg_corr > 0.8 or avg_corr < 0.2:
                corr_penalty = -0.1

        #   3b. Dispersion signal (cross‑sectional std of returns)
        dispersion = self.compute_dispersion()
        disp_penalty = 0
        if dispersion is not None:
            # High dispersion -> uncertain market -> reduce exposure
            if dispersion > 0.02:  # 2% daily dispersion
                disp_penalty = -0.15
            elif dispersion < 0.005:
                disp_penalty = 0.05  # very low dispersion can be benign

        #   3c. Seasonality signal (month effect)
        season_adj = self.compute_seasonality()
        if season_adj is None:
            season_adj = 0

        # 4. Final weight (clamped between 0 and 1)
        final_weight = base_exposure + corr_penalty + disp_penalty + season_adj
        final_weight = max(0.0, min(1.0, final_weight))

        # 5. Rebalance TQQQ
        self.SetHoldings(self.tqqq, final_weight)

        # Optionally log
        self.Debug(f"Date: {self.Time.date()}, Regime: {regime}, Base: {base_exposure:.2f}, "
                   f"Corr: {avg_corr:.2f}, Disp: {dispersion:.4f}, Season: {season_adj:.2f}, "
                   f"Weight: {final_weight:.2f}")

    # ---------------------------------------------------------------
    # Helper functions
    # ---------------------------------------------------------------
    def compute_HMA(self, symbol, period, lookback=0):
        """Compute Hull Moving Average using built-in WMA indicators.
           Returns the HMA value at the current time (or lookback days ago)."""
        # Fetch the required price history
        # Need period + sqrt(period) data points for HMA
        needed = int(period + np.sqrt(period)) + lookback + 5
        history = self.History([symbol], needed, Resolution.Daily)
        if history.empty:
            return 0
        closes = history.loc[symbol].close.values
        if len(closes) < needed:
            return 0

        # Use the last N points (including lookback offset)
        end = len(closes) - lookback
        start = end - int(period + np.sqrt(period)) - 1
        if start < 0:
            return 0
        prices = closes[start:end]

        # Compute WMAs using numpy (or can use QC's RollingWindow + WMA indicator manually)
        # We'll implement a simple WMA function
        def wma(p, n):
            weights = np.arange(1, n+1)
            return np.dot(p[-n:], weights) / weights.sum()

        half = int(period / 2)
        sqrt_n = int(np.sqrt(period))

        wma_half = wma(prices, half)
        wma_full = wma(prices, period)
        raw_hma = 2 * wma_half - wma_full

        # WMA of raw_hma over sqrt_n periods
        # Need prices for raw_hma: we need a series of raw_hma values over last sqrt_n days
        # Better approach: compute raw_hma for each point in the last sqrt_n days
        # For simplicity, compute HMA directly using the formula on the whole series
        # Alternative: use the known method: HMA = WMA(2*WMA(price, n/2) - WMA(price, n), sqrt(n))
        # We'll compute the 2*WMA(n/2) - WMA(n) series first
        # We'll use a list of prices and compute sliding WMAs
        wma_half_series = []
        wma_full_series = []
        # Need at least period points before computing
        for i in range(period-1, len(prices)):
            seg = prices[i-period+1:i+1]
            wma_full_series.append(wma(seg, period))
            half_seg = prices[i-half+1:i+1]
            wma_half_series.append(wma(half_seg, half))

        raw = [2*h - f for h, f in zip(wma_half_series, wma_full_series)]
        # Now compute WMA of raw over sqrt_n
        if len(raw) < sqrt_n:
            return 0
        hma_vals = []
        for i in range(sqrt_n-1, len(raw)):
            seg = raw[i-sqrt_n+1:i+1]
            hma_vals.append(wma(seg, sqrt_n))

        if not hma_vals:
            return 0
        # We want the most recent HMA value
        return hma_vals[-1]

    def compute_avg_correlation(self):
        """Average of rolling correlations between TQQQ and basket stocks."""
        if len(self.symbols) == 0:
            return None
        # We need to update correlation indicators each day.
        # Instead of storing indicators continuously, we compute fresh from history each day.
        # Use 60-day window.
        start = self.Time - timedelta(60)
        # Get history for TQQQ and all basket stocks
        symbols = [self.tqqq] + self.symbols
        history = self.History(symbols, 60, Resolution.Daily)
        if history.empty:
            return None
        # Pivot to get close prices for each symbol
        closes = history['close'].unstack(level=0)
        if closes.empty:
            return None
        # Compute daily returns
        returns = closes.pct_change().dropna()
        if len(returns) < 2:
            return None
        tqqq_ret = returns[self.tqqq]
        corrs = []
        for sym in self.symbols:
            if sym in returns.columns:
                corr = tqqq_ret.corr(returns[sym])
                if not np.isnan(corr):
                    corrs.append(corr)
        if len(corrs) == 0:
            return None
        return np.mean(corrs)

    def compute_dispersion(self):
        """Cross-sectional standard deviation of daily returns for basket stocks."""
        if len(self.symbols) < 2:
            return None
        # Get one day of returns for all basket stocks
        history = self.History(self.symbols, 2, Resolution.Daily)
        if history.empty:
            return None
        # Compute daily returns for each symbol
        returns = {}
        for sym in self.symbols:
            try:
                prices = history.loc[sym, 'close'].values
                if len(prices) >= 2:
                    ret = (prices[-1] - prices[-2]) / prices[-2]
                    returns[sym] = ret
            except:
                continue
        if len(returns) < 2:
            return None
        rets = list(returns.values())
        return np.std(rets)

    def compute_seasonality(self):
        """Average monthly return for TQQQ (all years) for the current month."""
        if self.month_avg_ret is None:
            self.month_avg_ret = {}
            # Pre‑compute average returns per month from start to current
            start = self.StartDate
            end = self.EndDate
            # Use all available history for TQQQ
            history = self.History(self.tqqq, start, end, Resolution.Daily)
            if not history.empty:
                df = history['close'].to_frame()
                df['month'] = df.index.get_level_values('time').month
                monthly_ret = df.groupby('month')['close'].apply(
                    lambda x: (x.iloc[-1] - x.iloc[0]) / x.iloc[0]
                )
                self.month_avg_ret = monthly_ret.to_dict()
        curr_month = self.Time.month
        if curr_month in self.month_avg_ret:
            # If average return is negative, reduce exposure, else increase slightly
            avg_ret = self.month_avg_ret[curr_month]
            if avg_ret < -0.02:
                return -0.05
            elif avg_ret > 0.02:
                return 0.05
        return 0
