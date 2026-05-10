class Algo041(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.AddEquity('TQQQ', Resolution.Daily)
        self.tqqq = self.Symbol('TQQQ')

        # Universe for dynamic mega-cap top-10
        self.AddUniverse(self.CoarseSelectionFunction)
        self.basket = {}                 # stores current universe symbols
        self.last_universe_update = None

        # Schedule rebalance before market open each day
        self.Schedule.On(self.DateRules.EveryDay(),
                         self.TimeRules.BeforeMarketOpen(),
                         self.Rebalance)

        # Cache for history to avoid repeated calls
        self.history_cache = {}

        # Regime detection: store SPY volatility percentile thresholds
        self.regime_percentile = 0.8     # high vol if above 80th percentile

    def CoarseSelectionFunction(self, coarse):
        # Filter for stocks with fundamental data
        filtered = [c for c in coarse if c.HasFundamentalData and c.Price > 5]
        # Sort by market cap descending, take top 10
        sorted_by_cap = sorted(filtered, key=lambda c: c.MarketCap, reverse=True)
        top10 = sorted_by_cap[:10]
        new_symbols = {c.Symbol for c in top10}

        # Remove symbols that left the universe
        for symbol in list(self.basket.keys()):
            if symbol not in new_symbols:
                self.Liquidate(symbol)
                del self.basket[symbol]

        # Add new symbols
        for symbol in new_symbols:
            if symbol not in self.basket:
                self.AddEquity(symbol, Resolution.Daily)
                self.basket[symbol] = symbol

        return list(new_symbols)

    def Rebalance(self):
        # Get all symbols including TQQQ
        all_symbols = list(self.basket.keys()) + [self.tqqq]
        if not all_symbols:
            return

        # Step 1: Compute overnight returns for each symbol
        overnight_returns = {}
        for symbol in all_symbols:
            hist = self.History(symbol, 2, Resolution.Daily)
            if hist.empty or len(hist) < 2:
                overnight_returns[symbol] = None
                continue
            # hist index: date ascending; most recent day is last row
            prev_close = hist['close'].iloc[-2]
            today_open = hist['open'].iloc[-1]
            if prev_close != 0:
                overnight = (today_open - prev_close) / prev_close
                overnight_returns[symbol] = overnight
            else:
                overnight_returns[symbol] = None

        # Filter symbols with overnight return < -2%
        short_candidates = [sym for sym, ret in overnight_returns.items()
                            if ret is not None and ret < -0.02]

        if not short_candidates:
            # No trades today
            return

        # Step 2: Advanced signals for each candidate
        # 2a: Market correlation (SPY)
        spy_history = self.History(['SPY'], 60, Resolution.Daily)
        spy_returns = None
        if not spy_history.empty and len(spy_history) >= 60:
            spy_close = spy_history['close'].unstack(level=0)['SPY']
            spy_returns = spy_close.pct_change().dropna()

        # 2b: Basket dispersion (returns standard deviation across symbols)
        # Use last 20 daily returns for all symbols in basket (exclude TQQQ)
        basket_syms = list(self.basket.keys())
        if basket_syms:
            basket_hist = self.History(basket_syms, 20, Resolution.Daily)
            if not basket_hist.empty:
                close_df = basket_hist['close'].unstack(level=0)
                returns_df = close_df.pct_change().dropna()
                if not returns_df.empty:
                    daily_dispersion = returns_df.std(axis=1).mean()
                else:
                    daily_dispersion = 0.0
            else:
                daily_dispersion = 0.0
        else:
            daily_dispersion = 0.0

        # 2c: Seasonality (month effect - average return for current month over past 5 years)
        current_month = self.Time.month
        # Get history for each symbol for past 5 years of the same month
        season_scores = {}
        for sym in short_candidates:
            hist = self.History(sym, 5 * 252, Resolution.Daily)
            if hist.empty:
                season_scores[sym] = 0.0
                continue
            close = hist['close']
            returns = close.pct_change().dropna()
            # Filter returns only for the current month
            month_returns = returns[returns.index.month == current_month]
            if len(month_returns) > 0:
                avg_month_return = month_returns.mean()
                # Score: negative average means historically bearish month -> higher reversion probability?
                # We'll use: if month is historically bearish (negative avg), increase conviction
                # Higher score when month avg return is negative
                season_scores[sym] = -avg_month_return  # positive if month is bearish
            else:
                season_scores[sym] = 0.0

        # 2d: Regime detection based on SPY 20-day realized volatility
        reg_vol = 0.0
        if spy_history is not None and not spy_history.empty:
            spy_close = spy_history['close'].unstack(level=0)['SPY']
            spy_returns = spy_close.pct_change().dropna()
            recent_vol = spy_returns.iloc[-20:].std() * np.sqrt(252)
            # Compare to historical volatility from past 2 years
            hist_spy = self.History(['SPY'], 2*252, Resolution.Daily)
            if not hist_spy.empty:
                spy_close_hist = hist_spy['close'].unstack(level=0)['SPY']
                spy_ret_hist = spy_close_hist.pct_change().dropna()
                hist_vol = spy_ret_hist.rolling(20).std() * np.sqrt(252)
                threshold = hist_vol.quantile(self.regime_percentile)
                if recent_vol > threshold:
                    reg_vol = 1.0  # high volatility regime
                else:
                    reg_vol = 0.0  # normal/low volatility

        # Step 3: Compute conviction score for each candidate
        conv_scores = {}
        for sym in short_candidates:
            # Correlation with SPY (use last 60 days)
            corr = 0.0
            if spy_returns is not None:
                sym_hist = self.History(sym, 60, Resolution.Daily)
                if not sym_hist.empty and len(sym_hist) >= 60:
                    sym_close = sym_hist['close']
                    sym_ret = sym_close.pct_change().dropna()
                    # align returns
                    common_dates = sym_ret.index.intersection(spy_returns.index)
                    if len(common_dates) > 20:
                        sym_aligned = sym_ret.loc[common_dates]
                        spy_aligned = spy_returns.loc[common_dates]
                        corr = np.corrcoef(sym_aligned, spy_aligned)[0,1]
            # Correlation score: lower is better for reversion (low beta means mean reversion)
            corr_score = 1 - abs(corr)  # higher when correlation is low

            # Dispersion score: if overall market dispersion is high, mean reversion stronger
            disp_score = min(daily_dispersion / 0.02, 1.0)  # normalize

            # Seasonality score
            season_score = min(max(season_scores.get(sym, 0.0), -1.0), 1.0)   # clip
            season_score = (season_score + 1.0) / 2.0   # map to [0,1]

            # Regime adjustment: if high volatility, reduce conviction (higher risk)
            regime_penalty = 0.2 * reg_vol

            # Combine
            conviction = 0.5 * corr_score + 0.3 * disp_score + 0.2 * season_score - regime_penalty
            conv_scores[sym] = max(conviction, 0.01)  # ensure positive

        # Step 4: Dynamic sizing - normalize so total absolute weight <= 1
        total_conv = sum(conv_scores.values())
        if total_conv == 0:
            return

        target_weights = {}
        for sym, score in conv_scores.items():
            # Proportional weight, cap at 1.0 per symbol
            weight = (score / total_conv) * 1.0   # since we only short, total abs = 1
            weight = min(weight, 1.0)
            target_weights[sym] = -weight        # short positions

        # Step 5: Apply holdings
        for sym, weight in target_weights.items():
            self.SetHoldings(sym, weight)

        # Liquidate positions that are not in targets (if we previously had them)
        for sym in self.Portfolio.Keys:
            if sym.Value in target_weights:
                continue
            # only liquidate if we have a position and it's not in current short candidates
            if self.Portfolio[sym].Invested:
                self.SetHoldings(sym, 0)
