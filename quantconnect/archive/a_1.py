# region imports
from AlgorithmImports import *
from datetime import datetime, timedelta
import numpy as np
# endregion

class MinimalMomentumMeanReversionLETFs(QCAlgorithm):
    """
    [BETA] V0.1 | Minimal Momentum Mean Reversion LETFs with Black Swan Catcher Minimal
    DJKeyhole - Use V1 Tech LETFs For The Long Term Minimal

    Converted from Composer Symphony DSL.
    Asset class : EQUITIES
    Rebalance threshold : 0.24  (24%)
    """

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        # ── Assets ────────────────────────────────────────────────────────────
        tickers = [
            "SPY",   # SPDR S&P 500 ETF Trust
            "QQQ",   # Invesco QQQ Trust
            "TQQQ",  # ProShares UltraPro QQQ
            "SQQQ",  # ProShares UltraPro Short QQQ
            "SOXL",  # Direxion Daily Semiconductor Bull 3x Shares
            "SOXS",  # Direxion Daily Semiconductor Bear 3x Shares
            "UVXY",  # ProShares Ultra VIX Short-Term Futures ETF
            "TLT",   # iShares 20+ Year Treasury Bond ETF
            "SPXL",  # Direxion Daily S&P 500 Bull 3x Shares
            "UPRO",  # ProShares UltraPro S&P500
        ]
        self._sym: dict[str, Symbol] = {}
        for t in tickers:
            self._sym[t] = self.AddEquity(t, Resolution.Daily).Symbol

        # ── Rebalance threshold ────────────────────────────────────────────────
        self._threshold = 0.24

        # ── Built-in indicators ────────────────────────────────────────────────
        # RSI windows: 5 and 10
        rsi_tickers = ["SPY", "QQQ", "TQQQ", "SQQQ", "SOXL", "UVXY", "SPXL"]
        self._rsi: dict[tuple, RelativeStrengthIndex] = {}
        for t in rsi_tickers:
            for w in (5, 10):
                self._rsi[(t, w)] = self.RSI(
                    self._sym[t], w, MovingAverageType.Wilders, Resolution.Daily
                )

        # Simple Moving Averages
        self._sma: dict[tuple, SimpleMovingAverage] = {
            ("SPY",  200): self.SMA(self._sym["SPY"],  200, Resolution.Daily),
            ("TQQQ",  20): self.SMA(self._sym["TQQQ"],  20, Resolution.Daily),
        }

        # ── Price history windows (cumret / stdev / ma-return) ────────────────
        warmup = 215
        self._pw: dict[str, RollingWindow] = {
            t: RollingWindow[float](warmup) for t in tickers
        }
        self.SetWarmUp(warmup, Resolution.Daily)

        # ── Schedule daily rebalance ───────────────────────────────────────────
        self.Schedule.On(
            self.DateRules.EveryDay("SPY"),
            self.TimeRules.AfterMarketOpen("SPY", 30),
            self._rebalance,
        )

    # ─── Data ─────────────────────────────────────────────────────────────────

    def OnData(self, data: Slice):
        for t, sym in self._sym.items():
            if data.Bars.ContainsKey(sym):
                self._pw[t].Add(float(data.Bars[sym].Close))

    # ─── Low-level indicator helpers ──────────────────────────────────────────

    def _price(self, t: str):
        sec = self.Securities[self._sym[t]]
        return float(sec.Price) if sec.HasData else None

    def _sma_v(self, t: str, w: int):
        ind = self._sma.get((t, w))
        return float(ind.Current.Value) if ind and ind.IsReady else None

    def _rsi_v(self, t: str, w: int):
        ind = self._rsi.get((t, w))
        return float(ind.Current.Value) if ind and ind.IsReady else None

    def _cum_ret(self, t: str, w: int):
        """
        DSL: (cumulative-return ticker {:window w})
        Returns (price_now / price_w_bars_ago - 1) * 100  [percent].
        """
        pw = self._pw[t]
        if pw.Count < w + 1:
            return None
        base = pw[w]
        return (pw[0] / base - 1.0) * 100.0 if base else None

    def _stdev_ret(self, t: str, w: int):
        """
        DSL: (stdev-return ticker {:window w})
        Population std-dev of daily % returns over the last w bars.
        """
        pw = self._pw[t]
        if pw.Count < w + 1:
            return None
        prices = [pw[i] for i in range(w + 1)]
        rets = [(prices[i] / prices[i + 1] - 1.0) * 100.0 for i in range(w)]
        return float(np.std(rets, ddof=0))

    def _ma_ret(self, t: str, w: int):
        """
        DSL: (moving-average-return ticker {:window w})
        Arithmetic mean of daily % returns over the last w bars.
        """
        pw = self._pw[t]
        if pw.Count < w + 1:
            return None
        prices = [pw[i] for i in range(w + 1)]
        rets = [(prices[i] / prices[i + 1] - 1.0) * 100.0 for i in range(w)]
        return float(np.mean(rets))

    # ─── Filter helpers ────────────────────────────────────────────────────────
    # DSL: (filter metric (select-top 1) assets)  → highest metric
    # DSL: (filter metric (select-bottom 1) assets) → lowest metric

    def _top_rsi5(self, tickers):
        """(filter (rsi {:window 5}) (select-top 1) tickers)"""
        scored = [(t, self._rsi_v(t, 5)) for t in tickers]
        valid  = [(t, v) for t, v in scored if v is not None]
        return max(valid, key=lambda x: x[1])[0] if valid else tickers[0]

    def _bot_rsi5(self, tickers):
        """(filter (rsi {:window 5}) (select-bottom 1) tickers)"""
        scored = [(t, self._rsi_v(t, 5)) for t in tickers]
        valid  = [(t, v) for t, v in scored if v is not None]
        return min(valid, key=lambda x: x[1])[0] if valid else tickers[0]

    def _bot_ma_ret5(self, tickers):
        """(filter (moving-average-return {:window 5}) (select-bottom 1) tickers)"""
        scored = [(t, self._ma_ret(t, 5)) for t in tickers]
        valid  = [(t, v) for t, v in scored if v is not None]
        return min(valid, key=lambda x: x[1])[0] if valid else tickers[0]

    # ─── Strategy sub-logic ───────────────────────────────────────────────────

    def _tech_dips(self):
        """
        DSL group: V1 | A Better "Tech LETF buy the dips" Minimal
        Pre-condition: SPY > MA200, TQQQ RSI10 <= 79, SPXL RSI10 <= 80.
        """
        qqq_5d = self._cum_ret("QQQ", 5)

        if qqq_5d is not None and qqq_5d < -6.0:
            # ── Deep QQQ dip ─────────────────────────────────────────────────
            tqqq_1d = self._cum_ret("TQQQ", 1)
            if tqqq_1d is not None and tqqq_1d > 5.0:
                # Violent 1-day TQQQ bounce → rotate defensive
                return self._top_rsi5(["SQQQ", "SOXS", "TLT"])
            tqqq_rsi10 = self._rsi_v("TQQQ", 10)
            if tqqq_rsi10 is not None and tqqq_rsi10 > 31.0:
                return self._bot_rsi5(["SQQQ", "SOXS", "TLT"])
            # TQQQ oversold → most-momentum bull/bond
            return self._top_rsi5(["TQQQ", "SOXL", "TLT"])

        else:
            # ── Normal regime ────────────────────────────────────────────────
            qqq_rsi10 = self._rsi_v("QQQ", 10)
            if qqq_rsi10 is not None and qqq_rsi10 > 80.0:
                return self._top_rsi5(["SQQQ", "SOXS", "TLT"])
            tqqq_std = self._stdev_ret("TQQQ", 10)
            if tqqq_std is not None and tqqq_std > 5.0:
                return "TLT"    # high volatility → bond safety
            return "TQQQ"       # low-vol bull → ride TQQQ

    def _bear_inner(self):
        """
        DSL: inner bear branch (SPY <= MA200) inside the Tech LETFs group.
        """
        tqqq_rsi10 = self._rsi_v("TQQQ", 10)
        if tqqq_rsi10 is not None and tqqq_rsi10 < 31.0:
            return self._bot_rsi5(["TQQQ", "SOXL"])

        spy_rsi10 = self._rsi_v("SPY", 10)
        if spy_rsi10 is not None and spy_rsi10 < 30.0:
            return self._bot_rsi5(["TQQQ", "SOXL"])

        uvxy_rsi10 = self._rsi_v("UVXY", 10)
        if uvxy_rsi10 is not None and uvxy_rsi10 > 74.0:
            if uvxy_rsi10 > 84.0:
                return self._bot_rsi5(["SQQQ", "SOXS", "TLT"])
            return "UVXY"

        tqqq_p  = self._price("TQQQ")
        tqqq_ma = self._sma_v("TQQQ", 20)
        if tqqq_p is not None and tqqq_ma is not None and tqqq_p > tqqq_ma:
            sqqq_rsi10 = self._rsi_v("SQQQ", 10)
            if sqqq_rsi10 is not None and sqqq_rsi10 < 31.0:
                return self._bot_rsi5(["SQQQ", "SOXS", "TLT"])
            return self._bot_rsi5(["TQQQ", "SOXL"])

        # TQQQ below MA20 → short side
        return self._top_rsi5(["SQQQ", "SOXS", "TLT"])

    def _tech_letfs(self):
        """
        DSL groups: V1/[BETA] Tech LETFs For The Long Term Minimal
        Top-level SPY-trend router; also called recursively from _outer_bear
        when UVXY RSI10 > 84 (black-swan catcher).
        """
        spy_p  = self._price("SPY")
        spy_ma = self._sma_v("SPY", 200)
        if spy_p is None or spy_ma is None:
            return "TLT"

        if spy_p > spy_ma:
            # ── Bull market ──────────────────────────────────────────────────
            tqqq_rsi10 = self._rsi_v("TQQQ", 10)
            if tqqq_rsi10 is not None and tqqq_rsi10 > 79.0:
                return "UVXY"
            spxl_rsi10 = self._rsi_v("SPXL", 10)
            if spxl_rsi10 is not None and spxl_rsi10 > 80.0:
                return "UVXY"
            return self._tech_dips()
        else:
            # ── Bear market ──────────────────────────────────────────────────
            return self._bear_inner()

    def _short_shorts(self):
        """
        DSL group: V1 | Who likes Short shorts Minimal
        """
        tqqq_p  = self._price("TQQQ")
        tqqq_ma = self._sma_v("TQQQ", 20)

        if tqqq_p is not None and tqqq_ma is not None and tqqq_p > tqqq_ma:
            sqqq_rsi10 = self._rsi_v("SQQQ", 10)
            if sqqq_rsi10 is not None and sqqq_rsi10 < 31.0:
                return self._bot_rsi5(["SQQQ", "SOXS", "TLT"])
            return self._bot_ma_ret5(["TQQQ", "SOXL", "UPRO"])

        # TQQQ below MA20 → strongest short-side asset
        return self._top_rsi5(["SQQQ", "SOXS", "TLT"])

    def _outer_bear(self):
        """
        DSL: outer ELSE arm (SPY <= MA200) of the top-level if.
        """
        tqqq_rsi10 = self._rsi_v("TQQQ", 10)

        if tqqq_rsi10 is not None and tqqq_rsi10 < 31.0:
            # ── TQQQ deeply oversold ─────────────────────────────────────────
            t2 = self._cum_ret("TQQQ", 2)
            t5 = self._cum_ret("TQQQ", 5)
            if t2 is not None and t5 is not None and t2 >= t5:
                # Short-term momentum >= longer-term → buy weakest bull LETF
                return self._bot_ma_ret5(["TQQQ", "SOXL", "UPRO"])

            spy_rsi10 = self._rsi_v("SPY", 10)
            if spy_rsi10 is not None and spy_rsi10 < 30.0:
                return self._bot_ma_ret5(["TQQQ", "SOXL", "UPRO"])

            uvxy_rsi10 = self._rsi_v("UVXY", 10)
            if uvxy_rsi10 is not None and uvxy_rsi10 > 74.0:
                if uvxy_rsi10 > 84.0:
                    # Extreme fear → hand off to V1 Tech LETFs
                    return self._tech_letfs()
                return "UVXY"

            # Default oversold recovery
            return self._bot_ma_ret5(["TQQQ", "SOXL", "UPRO"])

        else:
            # ── TQQQ not oversold ────────────────────────────────────────────
            spy_rsi10 = self._rsi_v("SPY", 10)
            if spy_rsi10 is not None and spy_rsi10 < 30.0:
                return self._bot_ma_ret5(["TQQQ", "SOXL", "UPRO"])

            uvxy_rsi10 = self._rsi_v("UVXY", 10)
            if uvxy_rsi10 is not None and uvxy_rsi10 > 74.0:
                if uvxy_rsi10 > 84.0:
                    # Extreme fear → hand off to [BETA] Tech LETFs
                    return self._tech_letfs()
                return "UVXY"

            return self._short_shorts()

    def _select_target(self):
        """Top-level routing — mirrors the outermost DSL if."""
        spy_p  = self._price("SPY")
        spy_ma = self._sma_v("SPY", 200)
        if spy_p is None or spy_ma is None:
            return "TLT"

        if spy_p > spy_ma:
            return self._tech_letfs()
        else:
            return self._outer_bear()

    # ─── Rebalance execution ──────────────────────────────────────────────────

    def _rebalance(self):
        if self.IsWarmingUp:
            return

        target = self._select_target()
        if not target:
            return

        target_sym  = self._sym[target]
        port_value  = self.Portfolio.TotalPortfolioValue
        if port_value <= 0:
            return

        current_w  = self.Portfolio[target_sym].HoldingsValue / port_value
        deviation  = abs(current_w - 1.0)
        holds_other = any(
            self.Portfolio[sym].Invested
            for t, sym in self._sym.items() if t != target
        )

        if deviation > self._threshold or holds_other:
            for t, sym in self._sym.items():
                if t != target and self.Portfolio[sym].Invested:
                    self.Liquidate(sym)
            self.SetHoldings(target_sym, 1.0)
            self.Log(f"Rebalanced → {target}  (deviation={deviation:.1%})")
