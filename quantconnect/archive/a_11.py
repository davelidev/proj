# SOXL Growth v2.4.5 RL
# Converted from Composer symphony to QuantConnect
#
# Top gate: max_drawdown(SOXL, 60) >= 50%?
#
# ── CRASH BRANCH (dd >= 50%) ──────────────────────────────────────────────────
#   stdev_return(TQQQ,14) <= 18  [low short-term vol]
#     stdev_return(TQQQ,100) <= 3.8  → top-2 by cumret(21) from [SOXL,TQQQ,SPXL]
#     else:
#       RSI(TQQQ,30) >= 50
#         stdev_return(TQQQ,30) >= 5.8  → SOXS
#         else                          → SPXL
#       RSI(TQQQ,30) < 50:
#         cumret(TQQQ,8) <= -20%        → SOXL
#         else:
#           max_drawdown(TQQQ,200) <= 65% → bottom-2 by cumret(3) from [TMV,SQQQ,SPXS]
#           else                          → SOXL
#   stdev_return(TQQQ,14) > 18   [high short-term vol]
#     cumret(TQQQ,30) <= -10%  → bottom-2 by cumret(3) from [TMV,SQQQ,SPXS]
#     else                     → top-3 by cumret(21) from [SOXL,TQQQ,TMF,SPXL]
#
# ── NORMAL BRANCH (dd < 50%) ──────────────────────────────────────────────────
#   RSI(SOXL,32) <= 62.1995:
#     stdev_return(SOXL,105) <= 4.9226  → SOXL
#     else:
#       RSI(SOXL,30) >= 57.49:
#         stdev_return(SOXL,30) >= 5.4135  → SOXS
#         else                             → top-2 by cumret(21) from [SOXL,SPXL,TQQQ]
#       RSI(SOXL,30) < 57.49:
#         cumret(SOXL,32) <= -12%          → SOXL
#         else:
#           max_drawdown(SOXL,250) <= 71%  → SOXS
#           else                           → SOXL
#   RSI(SOXL,32) > 62.1995  (implies >= 50, so always):
#     → SOXS
#
# Note: [TMV, SQQQ, SPXS, SPXS] in DSL — SPXS deduped → [TMV, SQQQ, SPXS].
# stdev_return = std dev of daily % returns over window.
# Rebalances daily.

from AlgorithmImports import *
from datetime import datetime, timedelta
import numpy as np


class SOXLGrowthV245RL(QCAlgorithm):

    def Initialize(self):
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100000)
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.Margin)

        for ticker in ["SOXL", "SOXS", "TQQQ", "SPXL", "SPXS", "TMV", "SQQQ", "TMF"]:
            self.AddEquity(ticker, Resolution.Daily)

        self.rsi_tqqq_30 = self.RSI("TQQQ", 30, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi_soxl_32 = self.RSI("SOXL", 32, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi_soxl_30 = self.RSI("SOXL", 30, MovingAverageType.Wilders, Resolution.Daily)

        self.SetWarmUp(260, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay("SOXL"),
            self.TimeRules.AfterMarketOpen("SOXL", 1),
            self.Rebalance,
        )

    def _is_ready(self):
        return all([
            self.rsi_tqqq_30.IsReady,
            self.rsi_soxl_32.IsReady,
            self.rsi_soxl_30.IsReady,
        ])

    def _cumret(self, ticker, window):
        """% cumulative return over `window` trading days."""
        history = list(self.History(ticker, window + 1, Resolution.Daily))
        if len(history) < window + 1:
            return None
        c = [x.Close for x in history]
        return (c[-1] / c[0] - 1) * 100

    def _stdev_return(self, ticker, window):
        """Std dev of daily % returns over `window` bars."""
        history = list(self.History(ticker, window + 1, Resolution.Daily))
        if len(history) < window + 1:
            return None
        closes = [x.Close for x in history]
        returns = [((closes[i] / closes[i-1]) - 1) * 100 for i in range(1, len(closes))]
        return np.std(returns)

    def _max_drawdown(self, ticker, window):
        """Max peak-to-trough drawdown (%) over `window` trading days."""
        history = list(self.History(ticker, window, Resolution.Daily))
        if len(history) < window:
            return None
        closes = [x.Close for x in history]
        peak, max_dd = closes[0], 0.0
        for price in closes[1:]:
            if price > peak:
                peak = price
            dd = (peak - price) / peak * 100
            if dd > max_dd:
                max_dd = dd
        return max_dd

    def _dedup(self, tickers):
        seen, out = set(), []
        for t in tickers:
            if t not in seen:
                seen.add(t)
                out.append(t)
        return out

    def _top_n_cumret(self, tickers, n, window):
        tickers = self._dedup(tickers)
        scores = {t: r for t in tickers if (r := self._cumret(t, window)) is not None}
        selected = sorted(scores, key=scores.get, reverse=True)[:n] if scores else tickers[:n]
        w = 1.0 / len(selected)
        return {t: w for t in selected}

    def _bottom_n_cumret(self, tickers, n, window):
        tickers = self._dedup(tickers)
        scores = {t: r for t in tickers if (r := self._cumret(t, window)) is not None}
        selected = sorted(scores, key=scores.get)[:n] if scores else tickers[:n]
        w = 1.0 / len(selected)
        return {t: w for t in selected}

    # Shared short list used in two places
    _BEAR_SHORT = ["TMV", "SQQQ", "SPXS", "SPXS"]  # SPXS deduped → [TMV,SQQQ,SPXS]

    def _crash_branch(self):
        stdev14 = self._stdev_return("TQQQ", 14)
        if stdev14 is None:
            return None

        if stdev14 <= 18:
            stdev100 = self._stdev_return("TQQQ", 100)
            if stdev100 is None:
                return None
            if stdev100 <= 3.8:
                return self._top_n_cumret(["SOXL", "TQQQ", "SPXL"], 2, 21)

            rsi30 = self.rsi_tqqq_30.Current.Value
            if rsi30 >= 50:
                stdev30 = self._stdev_return("TQQQ", 30)
                if stdev30 is None:
                    return None
                return {"SOXS": 1.0} if stdev30 >= 5.8 else {"SPXL": 1.0}
            else:
                cr8 = self._cumret("TQQQ", 8)
                if cr8 is None:
                    return None
                if cr8 <= -20:
                    return {"SOXL": 1.0}
                dd200 = self._max_drawdown("TQQQ", 200)
                if dd200 is None:
                    return None
                if dd200 <= 65:
                    return self._bottom_n_cumret(self._BEAR_SHORT, 2, 3)
                return {"SOXL": 1.0}
        else:
            cr30 = self._cumret("TQQQ", 30)
            if cr30 is None:
                return None
            if cr30 <= -10:
                return self._bottom_n_cumret(self._BEAR_SHORT, 2, 3)
            return self._top_n_cumret(["SOXL", "TQQQ", "TMF", "SPXL"], 3, 21)

    def _normal_branch(self):
        rsi32 = self.rsi_soxl_32.Current.Value

        if rsi32 <= 62.1995:
            stdev105 = self._stdev_return("SOXL", 105)
            if stdev105 is None:
                return None
            if stdev105 <= 4.9226:
                return {"SOXL": 1.0}

            rsi30 = self.rsi_soxl_30.Current.Value
            if rsi30 >= 57.49:
                stdev30 = self._stdev_return("SOXL", 30)
                if stdev30 is None:
                    return None
                if stdev30 >= 5.4135:
                    return {"SOXS": 1.0}
                return self._top_n_cumret(["SOXL", "SPXL", "TQQQ"], 2, 21)
            else:
                cr32 = self._cumret("SOXL", 32)
                if cr32 is None:
                    return None
                if cr32 <= -12:
                    return {"SOXL": 1.0}
                dd250 = self._max_drawdown("SOXL", 250)
                if dd250 is None:
                    return None
                return {"SOXS": 1.0} if dd250 <= 71 else {"SOXL": 1.0}
        else:
            # rsi32 > 62.1995 → always >= 50
            return {"SOXS": 1.0} if rsi32 >= 50 else self._top_n_cumret(["SOXL", "TQQQ", "TMF", "SPXL"], 3, 21)

    def _get_target(self):
        dd60 = self._max_drawdown("SOXL", 60)
        if dd60 is None:
            return None
        return self._crash_branch() if dd60 >= 50 else self._normal_branch()

    def Rebalance(self):
        if self.IsWarmingUp or not self._is_ready():
            return

        target = self._get_target()
        if target is None:
            self.Debug("Insufficient history — skipping rebalance.")
            return

        for h in self.Portfolio.Values:
            if h.Invested and h.Symbol.Value not in target:
                self.Liquidate(h.Symbol)

        for ticker, weight in target.items():
            self.SetHoldings(ticker, weight)

    def OnData(self, data):
        pass
