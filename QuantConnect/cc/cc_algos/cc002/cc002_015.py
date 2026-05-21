# SOXL.SOXS SeeSaw
# Converted from Composer symphony to QuantConnect
#
# Logic tree:
#   1. RSI(SOXS, 25) > 62.5
#        → select-bottom 1 by 1-day return from [SOXL, UVXY]
#   2. Else RSI(SOXL, 32) > 66
#        → select-bottom 1 by 1-day return from [SOXS, UVXY]
#   3. Else cumret(SOXL, 6) > 34%
#        → SOXS 100%  (select-top 1 from single-asset list)
#   4. Else cumret(SOXS, 6) > 26.5%:
#        If cumret(SOXS, 1) < -3%  → SOXS 100%  (select-bottom 1 from [SOXS])
#        Else                      → SOXL 100%  (select-bottom 1 from [SOXL])
#   5. Else → BIL 100%
#
# Rebalances only when any holding drifts > 10% from target (rebalance-threshold 0.10).

from AlgorithmImports import *
from datetime import datetime, timedelta


class SOXLSOXSSeeSaw(QCAlgorithm):

    RSI_SOXS_WINDOW     = 25
    RSI_SOXL_WINDOW     = 32
    REBALANCE_THRESHOLD = 0.10

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.Margin)

        for ticker in ["SOXL", "SOXS", "UVXY", "BIL"]:
            self.AddEquity(ticker, Resolution.Daily)

        self.rsi_soxs = self.RSI("SOXS", self.RSI_SOXS_WINDOW, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi_soxl = self.RSI("SOXL", self.RSI_SOXL_WINDOW, MovingAverageType.Wilders, Resolution.Daily)

        self.SetWarmUp(max(self.RSI_SOXS_WINDOW, self.RSI_SOXL_WINDOW) + 10, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay("SOXL"),
            self.TimeRules.AfterMarketOpen("SOXL", 1),
            self.Rebalance,
        )

    def _cumret(self, ticker, window):
        """Percentage cumulative return over `window` trading days."""
        history = list(self.History(ticker, window + 1, Resolution.Daily))
        if len(history) < window + 1:
            return None
        closes = [x.Close for x in history]
        return (closes[-1] / closes[0] - 1) * 100

    def _bottom_1_by_1d(self, tickers):
        """Ticker with the lowest 1-day return among candidates."""
        scores = {t: r for t in tickers if (r := self._cumret(t, 1)) is not None}
        return min(scores, key=scores.get) if scores else None

    def _get_target(self):
        if self.rsi_soxs.Current.Value > 62.5:
            selected = self._bottom_1_by_1d(["SOXL", "UVXY"])
            return {selected: 1.0} if selected else None

        if self.rsi_soxl.Current.Value > 66:
            selected = self._bottom_1_by_1d(["SOXS", "UVXY"])
            return {selected: 1.0} if selected else None

        cr_soxl_6 = self._cumret("SOXL", 6)
        if cr_soxl_6 is None:
            return None
        if cr_soxl_6 > 34:
            return {"SOXS": 1.0}

        cr_soxs_6 = self._cumret("SOXS", 6)
        if cr_soxs_6 is None:
            return None
        if cr_soxs_6 > 26.5:
            cr_soxs_1 = self._cumret("SOXS", 1)
            if cr_soxs_1 is None:
                return None
            return {"SOXS": 1.0} if cr_soxs_1 < -3 else {"SOXL": 1.0}

        return {"BIL": 1.0}

    def Rebalance(self):
        if self.IsWarmingUp:
            return
        if not self.rsi_soxs.IsReady or not self.rsi_soxl.IsReady:
            return

        target = self._get_target()
        if target is None:
            self.Debug("Insufficient history — skipping rebalance.")
            return

        total_value = self.Portfolio.TotalPortfolioValue
        if total_value == 0:
            return

        needs_rebalance = any(
            h.Invested and h.Symbol.Value not in target
            for h in self.Portfolio.Values
        )
        if not needs_rebalance:
            for ticker, target_weight in target.items():
                current_weight = self.Portfolio[ticker].HoldingsValue / total_value
                if abs(current_weight - target_weight) > self.REBALANCE_THRESHOLD:
                    needs_rebalance = True
                    break

        if not needs_rebalance:
            return

        for h in self.Portfolio.Values:
            if h.Invested and h.Symbol.Value not in target:
                self.Liquidate(h.Symbol)

        for ticker, weight in target.items():
            self.SetHoldings(ticker, weight)

    def OnData(self, data):
        pass
