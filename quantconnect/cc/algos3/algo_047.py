#region imports
from AlgorithmImports import *
#endregion

class Algo047(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        
        self.tqqq = self.AddEquity('TQQQ', Resolution.Daily).Symbol
        self.basket = {}  # dictionary to store data for universe symbols
        
        # Universe selection: top-10 mega cap stocks
        self.AddUniverse(self.CoarseSelectionFunction)
        
        # Parameters
        self.momentum_period = 252
        self.acceleration_period = 21
        self.corr_window = 60
        self.disp_window = 60
        self.seasonality_years = 5
        
        # For regime detection we use a simple volatility threshold
        self.volatility_window = 60
        
        # Rebalance daily
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.BeforeMarketClose('TQQQ'), self.Rebalance)
        
    def CoarseSelectionFunction(self, coarse):
        # Filter stocks with fundamental data and positive market cap
        filtered = [c for c in coarse if c.HasFundamentalData and c.MarketCap > 0]
        # Sort by market cap descending and take top 10
        sorted_by_cap = sorted(filtered, key=lambda c: c.MarketCap, reverse=True)
        top10 = sorted_by_cap[:10]
        
        # Update basket: remove old symbols not in new universe, add new ones
        new_symbols = {c.Symbol for c in top10}
        old_symbols = set(self.basket.keys())
        for sym in old_symbols - new_symbols:
            # Liquidate if we have holdings (handled in Rebalance)
            self.basket.pop(sym)
        for sym in new_symbols - old_symbols:
            self.basket[sym] = {}  # placeholder
        
        return [c.Symbol for c in top10]
    
    def Rebalance(self):
        # Gather all symbols to trade (universe + TQQQ)
        all_symbols = list(self.basket.keys()) + [self.tqqq]
        if len(all_symbols) == 0:
            return
        
        # Get historical close prices for all symbols
        history_df = self.History(all_symbols, max(self.momentum_period + self.acceleration_period, 252+21), Resolution.Daily)
        if history_df.empty:
            return
        
        # Unstack to get symbols as columns
        close = history_df['close'].unstack(level=0)
        # Drop symbols with insufficient data
        close = close.dropna(axis=1, thresh=len(close)*0.8)
        all_symbols = [s for s in all_symbols if s in close.columns]
        if not all_symbols:
            return
        
        # Compute signals for each symbol
        signals = {}
        for symbol in all_symbols:
            try:
                prices = close[symbol]
                # 1. Momentum acceleration (2nd derivative)
                mom = (prices.iloc[-1] / prices.iloc[-self.momentum_period]) - 1
                mom_prev = (prices.iloc[-1 - self.acceleration_period] / prices.iloc[-self.momentum_period - self.acceleration_period]) - 1
                acceleration = mom - mom_prev
                
                # Normalize acceleration to [0,1] using z-score? Use rank among symbols later.
                # For now, keep raw
                acc_signal = acceleration
                
                # 2. Correlation signal (average pairwise correlation of returns among universe)
                # Use daily returns over corr_window
                rets = prices.pct_change().dropna()
                if len(rets) >= self.corr_window:
                    rets_series = rets.iloc[-self.corr_window:]
                    # Compute correlation with other symbols in universe (excluding itself)
                    other_symbols = [s for s in all_symbols if s != symbol and s != self.tqqq and s in close.columns]
                    if other_symbols:
                        other_rets = close[other_symbols].pct_change().dropna()
                        # Align dates
                        common_dates = rets_series.index.intersection(other_rets.index)
                        if len(common_dates) >= 20:
                            corr_matrix = rets_series[common_dates].corr(other_rets[common_dates])
                            if isinstance(corr_matrix, pd.DataFrame):
                                avg_corr = corr_matrix.mean().mean()
                            else:
                                avg_corr = 0.5  # fallback
                        else:
                            avg_corr = 0.5
                    else:
                        avg_corr = 0.5
                else:
                    avg_corr = 0.5
                
                # 3. Dispersion signal (cross-sectional std of returns across all universe symbols)
                # Compute daily returns for all universe symbols over disp_window
                universe_symbols = [s for s in all_symbols if s != self.tqqq and s in close.columns]
                if universe_symbols:
                    all_rets = close[universe_symbols].pct_change().dropna()
                    if len(all_rets) >= self.disp_window:
                        recent_rets = all_rets.iloc[-self.disp_window:]
                        # Cross-sectional std each day, then average
                        daily_cs_std = recent_rets.std(axis=1)
                        avg_dispersion = daily_cs_std.mean()
                        # Normalize: high dispersion = more stock-specific risk, reduce position sizes
                    else:
                        avg_dispersion = 0.02
                else:
                    avg_dispersion = 0.02
                
                # 4. Seasonality effect: average return for current month over past years
                # Use historical monthly returns for this symbol
                today = self.Time
                current_month = today.month
                # Get monthly returns from prices (first of each month)
                monthly = prices.resample('M').last()
                monthly_returns = monthly.pct_change().dropna()
                # Filter by month
                same_month_rets = monthly_returns[monthly_returns.index.month == current_month]
                if len(same_month_rets) >= 1:
                    avg_monthly_ret = same_month_rets.mean()
                else:
                    avg_monthly_ret = 0.0
                # Normalize seasonality signal: positive average return -> boost
                
                # 5. Regime detection: volatility regime (high vol = reduce exposure)
                # Compute 60-day volatility of daily returns
                rets = prices.pct_change().dropna()
                if len(rets) >= self.volatility_window:
                    vol = rets.iloc[-self.volatility_window:].std() * np.sqrt(252)
                else:
                    vol = 0.2
                # Simple threshold: if vol > 30% annualized, reduce overall sizing
                vol_factor = max(0, 1 - (vol - 0.2) / 0.3) if vol > 0.2 else 1.0
                vol_factor = np.clip(vol_factor, 0.1, 1.0)
                
                # Combine signals into a raw score
                # Higher acceleration, lower correlation, lower dispersion, positive seasonality, lower vol
                # Normalize raw components then combine
                # We'll just use a simple weighted sum
                raw_score = (
                    acc_signal * 10  # scale acceleration
                    - avg_corr * 2   # penalize high correlation
                    - avg_dispersion * 20  # penalize high dispersion
                    + avg_monthly_ret * 5  # reward positive seasonality
                )
                # Apply volatility factor dynamically
                raw_score *= vol_factor
                
                signals[symbol] = raw_score
            except Exception as e:
                # If any error, skip
                continue
        
        if not signals:
            return
        
        # Convert to series and normalize to weights (long only, no leverage)
        signal_series = pd.Series(signals)
        # Keep only positive signals
        signal_series = signal_series[signal_series > 0]
        if signal_series.empty:
            # No positive signals -> liquidate
            for sym in all_symbols:
                self.Liquidate(sym)
            return
        
        # Normalize weights so sum <= 1 (no leverage)
        weights = signal_series / signal_series.sum()
        # Cap individual weight at 1 (already <1 because sum over >1 symbol)
        weights = weights.clip(upper=1.0)
        # Adjust to ensure sum <= 1 (if any clipped, redistribute)
        total = weights.sum()
        if total > 1:
            weights = weights / total
        
        # Execute trades
        for symbol, weight in weights.items():
            self.SetHoldings(symbol, weight)
        
        # Liquidate symbols not in signals (i.e., negative or zero signal)
        held = self.Portfolio.Keys
        for sym in held:
            if sym not in signals or signals[sym] <= 0:
                self.Liquidate(sym)
