from AlgorithmImports import *
import pandas as pd
import numpy as np

class Algo032(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        # Add TQQQ for volatility regime signal
        self.AddEquity('TQQQ', Resolution.Daily)

        # Universe for top 10 mega-cap stocks
        self.AddUniverse(self.CoarseSelectionFunction)

        # Basket for tracking selected symbols
        self.basket = {}
        self.vol_regime = 1.0  # 1.0 = full allocation, 0.5 = half
        self.equity_curve = []  # track drawdowns

        # Schedule daily rebalance at the close
        self.Schedule.On(self.DateRules.EveryDay('TQQQ'),
                        self.TimeRules.AfterMarketOpen('TQQQ', 1),
                        self.Rebalance)

    def CoarseSelectionFunction(self, coarse):
        # Select top 10 stocks by dollar volume
        sorted_by_volume = sorted([x for x in coarse if x.HasFundamentalData and x.Price > 0],
                                   key=lambda x: x.DollarVolume, reverse=True)
        top10 = [x.Symbol for x in sorted_by_volume[:10]]
        return top10

    def Rebalance(self):
        # Update basket with current universe symbols
        universe_symbols = list(self.basket.keys())
        if len(universe_symbols) == 0:
            return

        # Get historical data for all basket symbols + TQQQ
        all_symbols = universe_symbols + [Symbol.Create('TQQQ', SecurityType.Equity, Market.USA)]
        history_length = 252 + 20  # enough for rolling calculations
        hist = self.History(all_symbols, history_length, Resolution.Daily)
        if hist.empty or len(hist.index.levels[0]) < len(all_symbols):
            self.Debug("Not enough history, skipping")
            return

        # Separate TQQQ history
        tqqq_hist = hist.loc['TQQQ']
        tqqq_close = tqqq_hist['close']
        tqqq_returns = tqqq_close.pct_change().dropna()

        # -------------------------------
        # Vol regime for TQQQ
        # Compute rolling 20-day annualized vol over last 252 days
        if len(tqqq_returns) >= 252:
            rolling_20d_vol = tqqq_returns.rolling(20).std() * np.sqrt(252)
            rolling_20d_vol = rolling_20d_vol.dropna()
            # Median of these rolling vols over the last 252 days
            if len(rolling_20d_vol) >= 252:
                median_vol = rolling_20d_vol.iloc[-252:].median()
                current_vol = rolling_20d_vol.iloc[-1]
                self.vol_regime = 1.0 if current_vol < median_vol else 0.5
            else:
                self.vol_regime = 1.0  # default full allocation
        else:
            self.vol_regime = 1.0

        # -------------------------------
        # Compute factors for each basket symbol
        factor_data = {}
        for symbol in universe_symbols:
            try:
                sym_hist = hist.loc[symbol]
                sym_close = sym_hist['close']
                sym_returns = sym_close.pct_change().dropna()
            except:
                continue

            if len(sym_returns) < 63:  # minimum for correlation
                continue

            # 20-day volatility (annualized)
            vol_20d = sym_returns.tail(20).std() * np.sqrt(252)

            # 12-month momentum (252-day return) minus 1-month momentum (21-day return)
            mom_12m = sym_close.iloc[-1] / sym_close.iloc[-252] - 1 if len(sym_close) >= 252 else 0
            mom_1m = sym_close.iloc[-1] / sym_close.iloc[-21] - 1 if len(sym_close) >= 21 else 0
            momentum = mom_12m - mom_1m

            # Correlation to TQQQ over 63 days
            common_idx = sym_returns.index.intersection(tqqq_returns.index)
            if len(common_idx) >= 30:
                corr = sym_returns.loc[common_idx].corr(tqqq_returns.loc[common_idx])
            else:
                corr = 0

            factor_data[symbol] = {
                'vol': vol_20d,
                'momentum': momentum,
                'corr': corr
            }

        if len(factor_data) == 0:
            return

        # Normalize factors cross-sectionally (rank 0..1)
        symbols_list = list(factor_data.keys())
        vol_vals = np.array([factor_data[s]['vol'] for s in symbols_list])
        mom_vals = np.array([factor_data[s]['momentum'] for s in symbols_list])
        corr_vals = np.array([factor_data[s]['corr'] for s in symbols_list])

        # Rank and scale to [0,1]
        vol_rank = self.Rank(vol_vals, reverse=True)  # lower vol is better
        mom_rank = self.Rank(mom_vals, reverse=False)  # higher momentum is better
        corr_rank = self.Rank(corr_vals, reverse=True)  # lower correlation is better

        # Composite score (equal weights)
        scores = vol_rank + mom_rank + corr_rank
        sorted_idx = np.argsort(-scores)

        # Select top 5 symbols
        num_picks = min(5, len(symbols_list))
        picked_symbols = [symbols_list[i] for i in sorted_idx[:num_picks]]
        picked_scores = [scores[i] for i in sorted_idx[:num_picks]]

        # Compute weights proportional to score, scaled by vol regime
        total_score = sum(picked_scores)
        allocation = self.vol_regime
        weights = {}
        for sym, sc in zip(picked_symbols, picked_scores):
            if total_score > 0:
                w = (sc / total_score) * allocation
            else:
                w = allocation / num_picks
            weights[sym] = w

        # Liquidate all non-selected positions
        current_holdings = [s for s in self.Securities if self.Portfolio[s].Invested]
        for sym in current_holdings:
            if sym not in weights:
                self.Liquidate(sym)

        # Set holdings for selected symbols
        for sym, w in weights.items():
            if self.Securities.ContainsKey(sym):
                self.SetHoldings(sym, w)

        # Track equity for drawdown cycles
        self.equity_curve.append(self.Portfolio.TotalPortfolioValue)

    def Rank(self, values, reverse=False):
        """Rank array, returning normalized values in [0,1] (0 = worst, 1 = best)"""
        if len(values) < 2:
            return np.array([0.5]) if len(values) == 1 else np.array([])
        order = values.argsort()
        ranks = order.argsort().astype(float)
        # Normalize to 0..1
        if reverse:
            ranks = len(ranks) - 1 - ranks
        return ranks / (len(ranks) - 1) if len(ranks) > 1 else ranks
