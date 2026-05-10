from AlgorithmImports import *
import numpy as np

class Algo034(QCAlgorithm):
    """
    Modern quant daily trading algorithm using dynamic mega-cap basket,
    correlation crash signal (TLT), volatility regime, and breadth.
    Trades only TQQQ with adaptive position sizing.
    """

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        # Main asset – TQQQ
        self.AddEquity('TQQQ', Resolution.Daily)

        # Universe for top‑10 mega‑cap stocks (signal source)
        self.AddUniverse(self.CoarseSelectionFunction)
        self.basket = {}  # stores current universe symbols

        # Warm‑up for indicator calculation
        self.SetWarmUp(252)

        # Track peak portfolio value for drawdown
        self.peak_value = 0.0

    def CoarseSelectionFunction(self, coarse):
        """
        Select top 10 stocks by market cap from coarse universe.
        """
        # Filter: must have fundamental data, price > 5, positive market cap
        filtered = [c for c in coarse if c.HasFundamentalData and c.Price > 5 and c.MarketCap > 0]

        # Sort descending by market cap, take top 10
        sorted_by_mc = sorted(filtered, key=lambda c: c.MarketCap, reverse=True)
        top10 = sorted_by_mc[:10]

        # Update basket dictionary (keys = symbols)
        self.basket = {c.Symbol: None for c in top10}

        # Return the selected symbols for the algorithm to receive data
        return [c.Symbol for c in top10]

    def OnData(self, data):
        """
        Daily rebalance: compute signals and set TQQQ weight.
        """
        if self.IsWarmingUp or not self.basket:
            return

        basket_symbols = list(self.basket.keys())
        if not basket_symbols:
            return

        # ----------------------------------------------------------------------
        # 1. Fetch historical prices for basket + TLT (signal)
        # ----------------------------------------------------------------------
        lookback = max(252, 60)  # enough for SMA200 and correlation
        try:
            hist = self.History(basket_symbols + ['TLT'], lookback, Resolution.Daily)
        except Exception:
            return

        if hist.empty:
            return

        # Unstack to get close prices per symbol
        closes = hist['close'].unstack(level=0)

        # Ensure TLT data exists
        if 'TLT' not in closes.columns:
            return

        tlt_close = closes['TLT'].dropna()

        # Only keep basket symbols that are present in the history
        basket_in_hist = [s for s in basket_symbols if s in closes.columns]
        if len(basket_in_hist) == 0:
            return

        basket_close = closes[basket_in_hist].dropna()

        # ----------------------------------------------------------------------
        # 2. Correlation crash signal: corr(mega‑cap, TLT) < -0.4
        # ----------------------------------------------------------------------
        # Equal‑weighted basket daily returns
        basket_returns = basket_close.pct_change().dropna()
        basket_mean_ret = basket_returns.mean(axis=1)

        # TLT daily returns
        tlt_returns = tlt_close.pct_change().dropna()

        # Align and compute correlation over last 60 days
        combined = basket_mean_ret.to_frame('basket').join(tlt_returns.to_frame('tlt'), how='inner')
        if len(combined) < 20:
            return  # insufficient data
        corr = combined['basket'].corr(combined['tlt'])

        # ----------------------------------------------------------------------
        # 3. Volatility regime (TQQQ 60‑day annualized vol)
        # ----------------------------------------------------------------------
        tqqq_hist = self.History('TQQQ', 60, Resolution.Daily)
        if tqqq_hist.empty:
            return
        tqqq_close = tqqq_hist['close']
        tqqq_returns = tqqq_close.pct_change().dropna()
        vol = tqqq_returns.std() * np.sqrt(252)  # annualized

        # ----------------------------------------------------------------------
        # 4. Breadth: % of basket stocks above 200‑day SMA
        # ----------------------------------------------------------------------
        sma200 = basket_close.rolling(window=200).mean()
        if len(sma200) == 0:
            return
        last_close = basket_close.iloc[-1]
        last_sma = sma200.iloc[-1]
        above_sma = (last_close > last_sma).sum()
        breadth = above_sma / len(basket_in_hist)

        # ----------------------------------------------------------------------
        # 5. Drawdown cycle tracking
        # ----------------------------------------------------------------------
        equity = self.Portfolio.TotalPortfolioValue
        if equity > 0:
            self.peak_value = max(self.peak_value, equity)
            drawdown = (self.peak_value - equity) / self.peak_value
        else:
            drawdown = 0.0

        # ----------------------------------------------------------------------
        # 6. Combine signals into weight (0–1, no leverage)
        # ----------------------------------------------------------------------
        weight = 1.0

        # Correlation crash: reduce exposure
        if corr < -0.4:
            weight *= 0.5

        # High vol regime: reduce
        if vol > 0.25:
            weight *= 0.7

        # Low breadth (weak market): reduce
        if breadth < 0.5:
            weight *= 0.8

        # Large drawdown: reduce further
        if drawdown > 0.20:
            weight *= 0.5

        # Clamp to [0, 1] – no leverage
        weight = max(0.0, min(1.0, weight))

        # ----------------------------------------------------------------------
        # 7. Execute orders
        # ----------------------------------------------------------------------
        if weight > 0:
            self.SetHoldings('TQQQ', weight)
        else:
            self.Liquidate('TQQQ')

        # Optional logging
        self.Log(f"{self.Time.strftime('%Y-%m-%d')} | Corr={corr:.3f} | Vol={vol:.2f} | Breadth={breadth:.2f} | Drawdown={drawdown:.2%} | Weight={weight:.2f}")
