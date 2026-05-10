from QuantConnect import *
from QuantConnect.Data.UniverseSelection import *
from QuantConnect.Indicators import *
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class Algo045(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        # Add TQQQ manually (only hardcoded ticker allowed)
        self.tqqq = self.AddEquity('TQQQ', Resolution.Daily).Symbol

        # Universe settings for daily resolution
        self.UniverseSettings.Resolution = Resolution.Daily

        # Coarse universe for top 10 mega‑cap stocks
        self.AddUniverse(self.CoarseSelectionFunction)

        # Basket dictionary (required)
        self.basket = {}

        # Parameters
        self.corr_window = 60
        self.corr_threshold = 0.4
        self.vol_window = 20
        self.regime_window = 500
        self.seasonality_window = 252  # 12-month return as annual seasonality

        # Regime indicator: use TQQQ 200-day SMA
        self.sma = self.SMA(self.tqqq, 200, Resolution.Daily)

        # For storing monthly seasonality (compute once per symbol)
        self.monthly_returns = {}  # symbol -> dict of month -> average return

    def CoarseSelectionFunction(self, coarse):
        # Select top 10 stocks by market cap (excluding TQQQ which is added separately)
        sorted_coarse = sorted(
            [c for c in coarse if c.MarketCap > 0 and c.Symbol != self.tqqq],
            key=lambda c: c.MarketCap,
            reverse=True
        )
        top10 = [c.Symbol for c in sorted_coarse[:10]]
        return top10

    def OnData(self, data):
        # Update basket with current universe symbols and TQQQ
        if not self.basket:
            # On first data, get symbols from universe
            # self.basket will be populated after universe selection
            return

        # Get symbols from universe (list of selected symbols stored in object)
        if not hasattr(self, '_selected_symbols'):
            return
        symbols = list(set(self._selected_symbols + [self.tqqq]))

        # Build basket as dictionary
        self.basket = {sym: None for sym in symbols}

        # Ensure we have enough data to compute signals
        if len(self.basket) < 2:
            return

        # Get historical close prices for all symbols (extend window to max needed)
        max_window = max(self.corr_window, self.vol_window, self.seasonality_window,
                         self.regime_window) + 10
        history = self.History(list(self.basket.keys()), max_window, Resolution.Daily)
        if history.empty:
            return

        close = history['close'].unstack(level=0)
        # Drop symbols with insufficient data
        close = close.dropna(axis=1, how='any')
        if close.empty:
            return

        # Compute daily returns
        returns = close.pct_change().dropna()

        # Filter returns to the required windows
        recent_returns = returns.iloc[-self.corr_window:]
        recent_vol_returns = returns.iloc[-self.vol_window:]
        recent_season_returns = returns.iloc[-self.seasonality_window:]

        # -------------------------------------------------------------
        # 1. Correlation signal
        # -------------------------------------------------------------
        if len(recent_returns) < self.corr_window:
            avg_corr = 0.5  # default
        else:
            corr_matrix = recent_returns.corr()
            upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
            avg_corr = upper.stack().mean()
            if np.isnan(avg_corr):
                avg_corr = 0.5

        # -------------------------------------------------------------
        # 2. Dispersion signal (cross‑sectional standard deviation of returns)
        # -------------------------------------------------------------
        if recent_vol_returns.empty:
            dispersion = 0.01
        else:
            # Daily cross‑sectional standard deviation, then average over window
            cross_sectional_std = recent_vol_returns.std(axis=1)
            dispersion = cross_sectional_std.mean() if not cross_sectional_std.empty else 0.01

        # -------------------------------------------------------------
        # 3. Seasonality signal (trailing 12‑month return per symbol)
        # -------------------------------------------------------------
        seasonality_scores = {}
        for sym in self.basket:
            if sym in recent_season_returns.columns and not recent_season_returns[sym].empty:
                # 12-month cumulative return
                seasonality_scores[sym] = (1 + recent_season_returns[sym]).prod() - 1
            else:
                seasonality_scores[sym] = 0.0

        # -------------------------------------------------------------
        # 4. Regime detection (using TQQQ vs 200-day SMA)
        # -------------------------------------------------------------
        # If SMA is ready and price above SMA -> bull, else bear
        if self.sma.IsReady:
            price = self.Securities[self.tqqq].Close
            sma_value = self.sma.Current.Value
            bull_regime = price >= sma_value
        else:
            bull_regime = True  # default

        # Adjust total weight based on regime (reduce in bear markets)
        total_weight = 1.0
        if not bull_regime:
            total_weight = 0.8  # reduce exposure
        # In strong bull, could increase, but cap at 1.0 (no leverage)
        # We'll keep total_weight = 1.0 for bull

        # -------------------------------------------------------------
        # 5. Construct weights
        # -------------------------------------------------------------
        symbols_list = list(self.basket.keys())
        n = len(symbols_list)

        if n == 0:
            return

        if avg_corr < self.corr_threshold:
            # Low correlation: equal weight
            weights = {sym: total_weight / n for sym in symbols_list}
        else:
            # High correlation: concentrate based on composite signal
            # Composite = (momentum + seasonality) - volatility
            # Momentum: 60-day return
            # Seasonality: 252-day return (already computed)
            # Volatility: 20-day standard deviation (inverse)
            signals = {}
            for sym in symbols_list:
                if sym in recent_returns.columns and not recent_returns[sym].empty:
                    momentum = (1 + recent_returns[sym]).prod() - 1
                else:
                    momentum = 0.0
                if sym in recent_vol_returns.columns and not recent_vol_returns[sym].empty:
                    vol = recent_vol_returns[sym].std()
                else:
                    vol = close[sym].pct_change().std() if sym in close.columns else 0.01
                # Invert vol so lower vol gives higher score
                vol_score = -vol
                # Combine: momentum + seasonality - volatility (all normalized)
                # Simple rank‑based aggregation
                signals[sym] = momentum + seasonality_scores[sym] + vol_score

            # Safety: if all signals equal (e.g., zero), fallback to equal weight
            if all(v == 0 for v in signals.values()):
                weights = {sym: total_weight / n for sym in symbols_list}
            else:
                # Normalize signals to sum to 1
                total_signal = sum(signals.values())
                if total_signal == 0:
                    weights = {sym: total_weight / n for sym in symbols_list}
                else:
                    weights = {sym: (signals[sym] / total_signal) * total_weight for sym in symbols_list}

        # -------------------------------------------------------------
        # 6. Execute rebalance
        # -------------------------------------------------------------
        for sym, w in weights.items():
            if sym in data and data[sym] is not None:
                self.SetHoldings(sym, w)
