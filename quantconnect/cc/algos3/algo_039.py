from AlgorithmImports import *
from collections import deque

class Algo039(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        # Hardcoded TQQQ
        self.AddEquity("TQQQ", Resolution.Daily)

        # Universe selection for top-10 mega-cap stocks
        self.AddUniverse(self.CoarseSelectionFunction, self.FineSelectionFunction)

        # Basket to hold current universe symbols (as a set)
        self.basket = set()

        # Equity curve tracking for drawdown cycle
        self.equity_history = deque(maxlen=252)

    def CoarseSelectionFunction(self, coarse):
        # Select stocks with reasonable price and volume
        filtered = [c for c in coarse if c.HasFundamentalData and c.Price > 5 and c.Volume > 0]
        # Sort by dollar volume, take top 100 for fine selection
        sorted_by_dollarvol = sorted(filtered, key=lambda c: c.DollarVolume, reverse=True)[:100]
        return [c.Symbol for c in sorted_by_dollarvol]

    def FineSelectionFunction(self, fine):
        # From fine data, sort by market cap and take top 10
        sorted_by_marketcap = sorted(fine, key=lambda f: f.MarketCap, reverse=True)
        return [f.Symbol for f in sorted_by_marketcap[:10]]

    def OnSecuritiesChanged(self, changes):
        # Update self.basket with currently selected symbols
        for added in changes.AddedSecurities:
            self.basket.add(added.Symbol)
        for removed in changes.RemovedSecurities:
            self.basket.discard(removed.Symbol)

    def OnData(self, data):
        # 1. Update equity curve (total portfolio value)
        current_equity = self.Portfolio.TotalPortfolioValue
        self.equity_history.append(current_equity)

        # 2. Drawdown cycle check: only rebalance if equity > 252-day max - 10%
        if len(self.equity_history) == 252:
            rolling_max = max(self.equity_history)
            if current_equity <= rolling_max * 0.9:
                self.Debug("Drawdown too deep – skipping rebalance")
                return

        # 3. Rebalance day – compute signals for basket and TQQQ
        # Get history for basket symbols (last 252 trading days)
        basket_symbols = list(self.basket)
        if not basket_symbols:
            return

        # Use trade bars, fill forward
        history = self.History(basket_symbols, 252, Resolution.Daily)
        if history.empty:
            return

        # Unstack to get DataFrame of close prices (symbols as columns)
        close = history['close'].unstack(level=0)

        # Ensure we have enough data
        if len(close) < 252:
            return

        # 4. Compute signals per stock in basket
        # 12-month momentum (252-day return)
        mom12 = close.iloc[-1] / close.iloc[-252] - 1

        # 1-month momentum (21-day return)
        mom1 = close.iloc[-1] / close.iloc[-21] - 1

        # 20-day volatility (standard deviation of daily returns, annualized)
        daily_returns = close.pct_change().dropna()
        vol20 = daily_returns.tail(20).std() * np.sqrt(252)

        # Pairwise correlation (60 days)
        corr60 = daily_returns.tail(60).corr()
        avg_corr = corr60.mean().mean() if not corr60.empty else 0.5

        # Breadth: percentage of stocks above 200-day SMA
        sma200 = close.rolling(200).mean()
        breadth = (close.iloc[-1] > sma200.iloc[-1]).mean()

        # Composite score for each stock (momentum adjusted for volatility)
        # Use rank-based to avoid outliers
        mom12_rank = mom12.rank(pct=True)
        mom1_rank = mom1.rank(pct=True)
        vol_rank = -vol20.rank(pct=True)  # lower vol is better
        # Simple equal weight combination
        composite = mom12_rank * 0.4 + mom1_rank * 0.3 + vol_rank * 0.3
        composite = composite.clip(lower=0)  # ensure non-negative

        # 5. Market regime from basket volatility
        avg_vol = vol20.mean()
        hist_avg_vol = daily_returns.std() * np.sqrt(252)  # long-term average vol
        high_vol_regime = avg_vol > hist_avg_vol * 1.2  # threshold

        # 6. Determine basket allocation based on regime
        if high_vol_regime:
            basket_allocation = 0.5
        else:
            basket_allocation = 0.8

        # 7. Compute stock weights (proportional to composite score)
        total_score = composite.sum()
        if total_score > 0:
            raw_weights = composite / total_score
        else:
            raw_weights = pd.Series(0.0, index=composite.index)

        basket_weights = raw_weights * basket_allocation

        # 8. TQQQ signal – use its own history (simple momentum)
        tqqq_history = self.History("TQQQ", 252, Resolution.Daily)
        if not tqqq_history.empty:
            tqqq_close = tqqq_history['close']
            if len(tqqq_close) >= 252:
                tqqq_mom12 = tqqq_close.iloc[-1] / tqqq_close.iloc[-252] - 1
                tqqq_vol20 = tqqq_close.pct_change().tail(20).std() * np.sqrt(252)
                tqqq_hist_vol = tqqq_close.pct_change().std() * np.sqrt(252)
                tqqq_high_vol = tqqq_vol20 > tqqq_hist_vol * 1.2

                # TQQQ allocation: positive momentum and not overly risky
                if tqqq_mom12 > 0 and not tqqq_high_vol:
                    tqqq_weight = 1.0 - basket_allocation  # remaining cash
                else:
                    tqqq_weight = 0.0
            else:
                tqqq_weight = 0.0
        else:
            tqqq_weight = 0.0

        # 9. Ensure total weight <= 1
        total_weight = basket_allocation + tqqq_weight
        if total_weight > 1.0:
            # Scale down basket weights proportionally
            basket_weights *= (1.0 - tqqq_weight) / basket_allocation

        # 10. Place trades
        # First, liquidate any positions not in current basket and not TQQQ
        for symbol, holding in self.Portfolio.Items:
            if symbol.Value != "TQQQ" and symbol not in self.basket and holding.Invested:
                self.Liquidate(symbol)

        # Set holdings for basket
        for symbol, weight in basket_weights.items():
            if weight > 0:
                self.SetHoldings(symbol, weight)

        # Set holdings for TQQQ
        if tqqq_weight > 0:
            self.SetHoldings("TQQQ", tqqq_weight)
