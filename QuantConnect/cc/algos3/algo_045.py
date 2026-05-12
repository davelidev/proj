from AlgorithmImports import *
import numpy as np


class Algo045(QCAlgorithm):
    """Mega-7 EW + own-basket 20d annualized vol < 30% gate."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)


        self.vol_threshold = 0.30
        self.in_market = False

        self.AddUniverse(self._Sel)

        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.Schedule.On(
            self.DateRules.EveryDay(self.qqq),
            self.TimeRules.AfterMarketOpen(self.qqq, 30),
            self.R,
        )


    def _Sel(self, fundamental):
        elig = [f for f in fundamental
                if f.HasFundamentalData and f.MarketCap > 0 and f.Price > 5]
        elig.sort(key=lambda f: f.MarketCap, reverse=True)
        self._universe = [f.Symbol for f in elig[:5]]
        return self._universe

    def R(self):
        hist = self.History(self._universe, 21, Resolution.Daily)
        if hist is None or hist.empty:
            return

        # Build per-symbol log return series, then average them per day -> basket return.
        try:
            closes_df = hist['close'].unstack(level=0)
        except Exception:
            return

        # Drop columns with insufficient data
        closes_df = closes_df.dropna(axis=1, how='any')
        if closes_df.shape[0] < 21 or closes_df.shape[1] == 0:
            return

        log_close = np.log(closes_df.values)
        per_sym_log_rets = np.diff(log_close, axis=0)  # shape (20, n_syms)
        basket_rets = per_sym_log_rets.mean(axis=1)  # equal-weighted basket daily return
        vol = float(np.std(basket_rets) * np.sqrt(252))

        target_in = vol < self.vol_threshold
        if target_in == self.in_market:
            return

        if target_in:
            w = 1.0 / len(self._universe)
            for s in self._universe:
                self.SetHoldings(s, w)
        else:
            self.Liquidate()

        self.in_market = target_in
