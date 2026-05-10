from AlgorithmImports import *
import math

class Algo038(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.AddEquity('TQQQ', Resolution.Daily)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelectionFunction)

        # Basket of selected symbols (size = 7)
        self.basket = []
        self.basket_size = 7
        self.breadth_threshold = 5          # need >=5 out of 7 up over 21 days

        # Regime tracking
        self.peak_equity = 100_000
        self.vol_lookback = 252
        self.vol_period = 21
        self.return_period = 21
        self.regime_vol_percentile = 0.75
        self.drawdown_threshold = 0.15
        self.tqqq_vol_history = []          # rolling list of TQQQ 21d annualized vol

    def CoarseSelectionFunction(self, coarse):
        # Filter for liquid mega-cap stocks and take top 10 by market cap
        sorted_coarse = sorted(
            [c for c in coarse if c.Price > 5 and c.MarketCap is not None],
            key=lambda c: c.MarketCap,
            reverse=True
        )
        return [c.Symbol for c in sorted_coarse[:10]]

    def OnData(self, data):
        # Liquidate all positions; we will re‑establish desired holdings
        self.Liquidate()

        # Get all currently traded symbols from universe (excluding TQQQ)
        universe_symbols = [
            s for s in self.ActiveSecurities.Keys
            if s != 'TQQQ' and self.ActiveSecurities[s].IsTradable
        ]

        if len(universe_symbols) == 0:
            # No universe data yet – go to TQQQ with full allocation
            self.SetHoldings('TQQQ', 1.0)
            return

        # For each symbol, compute 21-day return and volatility
        symbols_info = {}
        for symbol in universe_symbols:
            hist = self.History(symbol, self.return_period + 1, Resolution.Daily)
            if hist.empty or len(hist) < self.return_period + 1:
                continue
            prices = hist['close'].values
            # 21-day return
            ret_21d = (prices[-1] / prices[0]) - 1.0
            # 21-day annualized volatility
            daily_returns = []
            for i in range(1, len(prices)):
                daily_returns.append((prices[i] / prices[i-1]) - 1.0)
            avg = sum(daily_returns) / len(daily_returns)
            var = sum((r - avg)**2 for r in daily_returns) / len(daily_returns)
            vol_21d = math.sqrt(var) * math.sqrt(252) if var > 0 else 0.0
            symbols_info[symbol] = {'return': ret_21d, 'vol': vol_21d}

        if len(symbols_info) < self.basket_size:
            self.SetHoldings('TQQQ', 1.0)
            return

        # Select top 7 by short-term momentum (21-day return)
        sorted_symbols = sorted(
            symbols_info.keys(),
            key=lambda s: symbols_info[s]['return'],
            reverse=True
        )
        self.basket = sorted_symbols[:self.basket_size]

        # Breadth voting: count how many of the 7 have positive 21-day return
        up_count = sum(1 for s in self.basket if symbols_info[s]['return'] > 0)

        # Compute regime factor based on TQQQ volatility and portfolio drawdown
        # Get TQQQ 21-day volatility
        tqqq_hist = self.History('TQQQ', self.vol_period + 1, Resolution.Daily)
        if not tqqq_hist.empty and len(tqqq_hist) >= self.vol_period + 1:
            tqqq_prices = tqqq_hist['close'].values
            tqqq_daily = []
            for i in range(1, len(tqqq_prices)):
                tqqq_daily.append((tqqq_prices[i] / tqqq_prices[i-1]) - 1.0)
            tqqq_avg = sum(tqqq_daily) / len(tqqq_daily)
            tqqq_var = sum((r - tqqq_avg)**2 for r in tqqq_daily) / len(tqqq_daily)
            tqqq_vol = math.sqrt(tqqq_var) * math.sqrt(252) if tqqq_var > 0 else 0.20
        else:
            tqqq_vol = 0.20

        # Update rolling history of TQQQ volatility
        self.tqqq_vol_history.append(tqqq_vol)
        if len(self.tqqq_vol_history) > self.vol_lookback:
            self.tqqq_vol_history.pop(0)

        # Determine if current volatility is in the top quartile
        high_vol = False
        if len(self.tqqq_vol_history) >= 60:  # enough data for percentile
            sorted_hist = sorted(self.tqqq_vol_history)
            threshold_idx = int(len(sorted_hist) * self.regime_vol_percentile)
            threshold = sorted_hist[threshold_idx] if threshold_idx < len(sorted_hist) else sorted_hist[-1]
            high_vol = tqqq_vol > threshold

        # Current drawdown
        current_equity = self.Portfolio.TotalPortfolioValue
        if current_equity > self.peak_equity:
            self.peak_equity = current_equity
        drawdown = (self.peak_equity - current_equity) / self.peak_equity if self.peak_equity > 0 else 0.0

        # Combine regime factors – reduce exposure in high vol or large drawdown
        regime_factor = 1.0
        if high_vol:
            regime_factor *= 0.5
        if drawdown > self.drawdown_threshold:
            regime_factor *= 0.5
        regime_factor = max(0.1, min(1.0, regime_factor))

        if up_count >= self.breadth_threshold:
            # Hold the basket – use inverse volatility weighting (modern quant)
            inv_vols = [1.0 / symbols_info[s]['vol'] for s in self.basket]
            total_inv = sum(inv_vols)
            if total_inv == 0:
                weights = [regime_factor / self.basket_size] * self.basket_size
            else:
                weights = [iv / total_inv * regime_factor for iv in inv_vols]

            for sym, w in zip(self.basket, weights):
                self.SetHoldings(sym, w)
        else:
            # Shift to TQQQ
            self.SetHoldings('TQQQ', regime_factor)
