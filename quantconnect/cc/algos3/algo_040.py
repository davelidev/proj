# region imports
from AlgorithmImports import *
from QuantConnect.Data.UniverseSelection import *
from System.Collections.Generic import List
# endregion

class Algo040(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        # Add TQQQ as core asset (no hardcoded tickers otherwise)
        self.AddEquity('TQQQ', Resolution.Daily)
        self.tqqq = self.Symbol('TQQQ')

        # Universe selection for top-10 mega-cap stocks
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelectionFunction, self.FineSelectionFunction)

        # Basket dictionary for tracking (not self.universe)
        self.basket = {}

        # Warmup for historical prices
        self.SetWarmUp(252, Resolution.Daily)

        # Track portfolio for drawdown cycles
        self.portfolio_peak = 100_000
        self.portfolio_value_history = []

        # Schedule rebalance at market open using daily data
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.BeforeMarketClose(self.tqqq, 5),
                         self.Rebalance)

    def CoarseSelectionFunction(self, coarse):
        # Filter by dollar volume top 1000
        sorted_by_volume = sorted(
            [c for c in coarse if c.HasFundamentalData and c.Volume > 0],
            key=lambda c: c.DollarVolume,
            reverse=True
        )
        return [c.Symbol for c in sorted_by_volume[:1000]]

    def FineSelectionFunction(self, fine):
        # Select top 10 by market cap
        sorted_by_market_cap = sorted(
            [f for f in fine if f.MarketCap > 0],
            key=lambda f: f.MarketCap,
            reverse=True
        )
        selected = [f.Symbol for f in sorted_by_market_cap[:10]]
        return selected

    def OnSecuritiesChanged(self, changes):
        # Update basket dictionary when universe changes
        for added in changes.AddedSecurities:
            if added.Symbol not in self.basket:
                self.basket[added.Symbol] = {}

        for removed in changes.RemovedSecurities:
            if removed.Symbol in self.basket:
                del self.basket[removed.Symbol]

    def Rebalance(self):
        if self.IsWarmingUp:
            return

        # Update portfolio peak for drawdown tracking
        current_value = self.Portfolio.TotalPortfolioValue
        self.portfolio_value_history.append(current_value)
        if current_value > self.portfolio_peak:
            self.portfolio_peak = current_value
        drawdown = (self.portfolio_peak - current_value) / self.portfolio_peak

        # Get all symbols in basket plus TQQQ
        symbols = list(self.basket.keys()) + [self.tqqq]

        if len(symbols) < 2:
            return

        # Fetch history for all symbols (daily, 252 days)
        history = self.History(symbols, 252, Resolution.Daily)
        if history.empty:
            return

        # Compute signals for each symbol
        signals = {}
        for symbol in symbols:
            if symbol not in history.index.get_level_values('symbol'):
                continue
            df = history.loc[symbol].copy()
            if len(df) < 60:
                continue

            # Gap: (open - previous close) / previous close
            prev_close = df['close'].shift(1)
            gap = (df['open'] - prev_close) / prev_close
            current_gap = gap.iloc[-1]

            # Volatility: 14-day ATR
            high_low = df['high'] - df['low']
            high_close = np.abs(df['high'] - df['close'].shift(1))
            low_close = np.abs(df['low'] - df['close'].shift(1))
            tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
            atr_14 = tr.rolling(14).mean().iloc[-1]

            # Momentum: 20-day rate of change
            roc_20 = (df['close'].iloc[-1] / df['close'].iloc[-21] - 1) if len(df) >= 21 else 0

            # Volume ratio: current volume vs 20-day avg
            vol_avg = df['volume'].rolling(20).mean().iloc[-1]
            vol_ratio = df['volume'].iloc[-1] / vol_avg if vol_avg > 0 else 1

            # Correlation with TQQQ (60-day rolling) – use log returns
            if self.tqqq in history.index.get_level_values('symbol'):
                tqqq_df = history.loc[self.tqqq].copy()
                tqqq_returns = tqqq_df['close'].pct_change()
                symbol_returns = df['close'].pct_change()
                combined = pd.DataFrame({
                    'symbol_ret': symbol_returns,
                    'tqqq_ret': tqqq_returns
                }).dropna()
                if len(combined) >= 60:
                    corr = combined['symbol_ret'].rolling(60).corr(combined['tqqq_ret']).iloc[-1]
                else:
                    corr = 0
            else:
                corr = 0

            # Store signal components for scoring
            signals[symbol] = {
                'gap': current_gap,
                'atr': atr_14,
                'roc_20': roc_20,
                'vol_ratio': vol_ratio,
                'corr': corr,
                'price': df['close'].iloc[-1]
            }

        if len(signals) == 0:
            return

        # Compute breadth: proportion of positive gaps among all basket stocks (excl TQQQ)
        basket_signals = {s: v for s, v in signals.items() if s in self.basket}
        if len(basket_signals) > 0:
            pos_gaps = sum(1 for v in basket_signals.values() if v['gap'] > 0.005)
            breadth = pos_gaps / len(basket_signals)
        else:
            breadth = 0.5

        # Volatility regime: classify average ATR of basket into low/med/high quantiles
        atr_values = [v['atr'] for v in basket_signals.values() if v['atr'] > 0]
        if len(atr_values) > 5:
            avg_atr = np.mean(atr_values)
            # Use historical quantiles; simple approach: compare to median of past ATR
            # For simplicity use a fixed threshold (since no prev data stored)
            # Instead determine regime relative to historical data: we have history – compute median
            all_atr = [v['atr'] for v in signals.values() if v['atr'] > 0]
            median_atr = np.median(all_atr) if len(all_atr) > 0 else avg_atr
            if avg_atr > 1.5 * median_atr:
                vol_regime = 'high'
            elif avg_atr < 0.5 * median_atr:
                vol_regime = 'low'
            else:
                vol_regime = 'med'
        else:
            vol_regime = 'med'

        # Position sizing adjustment based on regime and drawdown
        base_exposure = 0.8  # Maximum total exposure
        if vol_regime == 'high':
            base_exposure *= 0.5
        elif vol_regime == 'low':
            base_exposure *= 1.2
        if drawdown > 0.15:
            base_exposure *= 0.5
        elif drawdown > 0.1:
            base_exposure *= 0.75
        base_exposure = min(base_exposure, 1.0)

        # Score each symbol: gap * corr * momentum * volume ratio
        # For reversal: if gap large in direction opposite to correlation? But modern quant: combine factors.
        # Score = gap * (corr * 0.4 + roc_20 * 0.3 + vol_ratio * 0.1 + breadth * 0.2)
        # Then normalize – but adapt based on vol regime
        scores = {}
        for sym, data in signals.items():
            # Combine factors; use abs of gap to penalize extreme moves? We'll keep direction.
            score = data['gap'] * (0.4 * data['corr'] + 0.3 * data['roc_20'] + 0.1 * data['vol_ratio'] + 0.2 * breadth)
            # Vol scaling: lower weight for high vol stocks
            if data['atr'] > 0:
                score /= data['atr'] ** 0.5  # inverse sqrt vol weighting
            scores[sym] = score

        # Select positions: long top 3, short bottom 3 (if scores are extreme)
        sorted_scores = sorted(scores.items(), key=lambda x: x[1])
        longs = [sym for sym, sc in sorted_scores[-3:] if sc > 0.001]
        shorts = [sym for sym, sc in sorted_scores[:3] if sc < -0.001]

        # Determine total number of positions
        total_positions = len(longs) + len(shorts)
        if total_positions == 0:
            self.Liquidate()
            return

        # Allocate weights: equal weight among selected, adjusted by base_exposure
        weight_per_position = base_exposure / total_positions

        # Place orders
        for sym in self.basket.keys():
            if sym in longs:
                self.SetHoldings(sym, weight_per_position)
            elif sym in shorts:
                self.SetHoldings(sym, -weight_per_position)
            else:
                # Close any existing position not in signals
                if self.Portfolio[sym].Invested:
                    self.Liquidate(sym)

        # TQQQ: only trade if it appears in signals (it will always be there)
        # We can trade it as part of the basket or separately. Include it in scoring.
        if self.tqqq in signals:
            tqqq_weight = 0
            if self.tqqq in longs:
                tqqq_weight = weight_per_position
            elif self.tqqq in shorts:
                tqqq_weight = -weight_per_position
            self.SetHoldings(self.tqqq, tqqq_weight)

        # Update peak for next cycle (tracked in OnData)
        self.Debug(f"Rebalanced: {len(longs)} longs, {len(shorts)} shorts, exposure {base_exposure:.2f}")

    def OnData(self, slice):
        # Update portfolio value for drawdown tracking
        if not self.IsWarmingUp:
            self.portfolio_peak = max(self.portfolio_peak, self.Portfolio.TotalPortfolioValue)

    def OnEndOfDay(self):
        # Optional: any end-of-day logging
        pass
