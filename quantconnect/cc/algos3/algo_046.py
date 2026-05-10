from QuantConnect import *
from QuantConnect.Algorithm import *
from QuantConnect.Data.UniverseSelection import *
from datetime import datetime
import numpy as np

class Algo046(QCAlgorithm):
    """Advanced Quant Signals daily trading algorithm using return dispersion."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        # Core holding (mandated)
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol

        # Universe settings
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelectionFunction)

        # Basket of universe symbols (NOT self.universe)
        self.basket = {}

    def CoarseSelectionFunction(self, coarse):
        """Select top 10 mega-cap stocks by market cap, excluding TQQQ."""
        # Filter out TQQQ and ensure data quality
        filtered = [c for c in coarse
                    if c.Symbol != self.tqqq
                    and c.MarketCap != 0
                    and c.Price > 0]

        # Sort by market cap descending, take top 10
        sorted_coarse = sorted(filtered, key=lambda c: c.MarketCap, reverse=True)
        top10 = sorted_coarse[:10]

        # Update basket dictionary (keys are symbols)
        self.basket = {c.Symbol: None for c in top10}

        # Return list of symbols for universe subscription
        return list(self.basket.keys())

    def OnData(self, slice):
        """Daily rebalance based on advanced quant signals."""
        # Combine universe symbols and TQQQ
        symbols = list(self.basket.keys()) + [self.tqqq]

        # Need at least 2 symbols to compute dispersion
        if len(symbols) < 2:
            return

        # Fetch historical close prices (21 days to have 20 returns, then use last 10)
        lookback = 21
        hist = self.History(symbols, lookback, Resolution.Daily)
        if hist.empty or 'close' not in hist:
            return

        # Unstack into DataFrame (columns = symbols)
        close = hist['close'].unstack(level=0)

        # Compute daily returns
        daily_returns = close.pct_change().dropna()

        # Use the most recent 10 trading days
        recent_returns = daily_returns.tail(10)
        if len(recent_returns) < 2:
            return

        # 1. Return dispersion (cross-sectional std of cumulative returns)
        cumulative_returns = (1 + recent_returns).prod() - 1
        dispersion = float(cumulative_returns.std())

        # Identify the leader (asset with highest cumulative return)
        leader = cumulative_returns.idxmax()

        # 2. Correlation signal: average pairwise correlation over the 10 days
        corr_matrix = recent_returns.corr()
        num_assets = len(corr_matrix)
        if num_assets > 1:
            # Sum off-diagonal correlations
            sum_corr = corr_matrix.sum().sum() - num_assets
            avg_corr = sum_corr / (num_assets * (num_assets - 1))
        else:
            avg_corr = 1.0

        # 3. Regime detection: volatility of equal-weight portfolio over 20 days
        portfolio_returns = daily_returns.tail(20).mean(axis=1)
        vol = float(portfolio_returns.std())
        high_vol = vol > 0.02  # daily vol > 2% considered high

        # 4. Seasonality: month of the year (adjust threshold in January)
        month = self.Time.month
        month_factor = 0.5 if month == 1 else 1.0

        # Base threshold for dispersion (5% cumulative dispersion)
        base_threshold = 0.05
        threshold = base_threshold * month_factor

        # Adjust threshold for correlation (lower threshold when correlations are low)
        if avg_corr < 0.3:
            threshold *= 0.8

        # Adjust threshold for high volatility regime (more likely to concentrate)
        if high_vol:
            threshold *= 0.9

        # Determine weights
        if dispersion > threshold:
            # Concentrate on leader: weight scales with how far dispersion exceeds threshold
            excess = min((dispersion - threshold) / 0.1, 1.0)  # cap at 1
            leader_weight = 0.5 + 0.3 * excess  # dynamic between 0.5 and 0.8
            remaining = 1.0 - leader_weight

            # Distribute remaining equally among other symbols
            others = [s for s in symbols if s != leader]
            if others:
                weight_other = remaining / len(others)
            else:
                weight_other = 0

            weights = {leader: leader_weight}
            for sym in others:
                weights[sym] = weight_other
        else:
            # Equal weight
            w = 1.0 / len(symbols)
            weights = {sym: w for sym in symbols}

        # Execute rebalance (SetHoldings handles selling unlisted symbols)
        for sym, weight in weights.items():
            self.SetHoldings(sym, weight)
