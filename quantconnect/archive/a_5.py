# The Holy Grail
# Converted from Composer symphony to QuantConnect
#
# Logic tree:
#   If TQQQ > SMA(TQQQ, 200):          ← above 200-day MA
#       If RSI(TQQQ, 10) > 79  → UVXY 100%
#       Else                   → TQQQ 100%
#   Else:                              ← below 200-day MA
#       If RSI(TQQQ, 10) < 31  → TECL 100%
#       Else:
#           If RSI(SOXL, 10) < 30  → SOXL 100%
#           Else:
#               If TQQQ < SMA(TQQQ, 20)  → select-top 1 by RSI(10) from [SQQQ, BSV]
#               Else                     → TQQQ 100%
#
# Rebalances only when any holding drifts > 5% from target (rebalance-threshold 0.05).

from AlgorithmImports import *
from datetime import datetime, timedelta


class TheHolyGrail(QCAlgorithm):

    RSI_WINDOW        = 10
    MA_FAST           = 20
    MA_SLOW           = 200
    REBALANCE_THRESHOLD = 0.05

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.Margin)

        for ticker in ["TQQQ", "UVXY", "TECL", "SOXL", "SQQQ", "BSV"]:
            self.AddEquity(ticker, Resolution.Daily)

        self.rsi_tqqq = self.RSI("TQQQ", self.RSI_WINDOW, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi_soxl = self.RSI("SOXL", self.RSI_WINDOW, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi_sqqq = self.RSI("SQQQ", self.RSI_WINDOW, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi_bsv  = self.RSI("BSV",  self.RSI_WINDOW, MovingAverageType.Wilders, Resolution.Daily)

        self.sma_200 = self.SMA("TQQQ", self.MA_SLOW, Resolution.Daily)
        self.sma_20  = self.SMA("TQQQ", self.MA_FAST, Resolution.Daily)

        self.SetWarmUp(self.MA_SLOW + 1, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay("TQQQ"),
            self.TimeRules.AfterMarketOpen("TQQQ", 1),
            self.Rebalance,
        )

    def _get_target(self):
        tqqq_price = self.Securities["TQQQ"].Price

        if tqqq_price > self.sma_200.Current.Value:
            # Above 200-day MA
            if self.rsi_tqqq.Current.Value > 79:
                return {"UVXY": 1.0}
            return {"TQQQ": 1.0}
        else:
            # Below 200-day MA
            if self.rsi_tqqq.Current.Value < 31:
                return {"TECL": 1.0}
            if self.rsi_soxl.Current.Value < 30:
                return {"SOXL": 1.0}
            if tqqq_price < self.sma_20.Current.Value:
                # Select top 1 by RSI(10) from [SQQQ, BSV]
                scores = {
                    "SQQQ": self.rsi_sqqq.Current.Value,
                    "BSV":  self.rsi_bsv.Current.Value,
                }
                return {max(scores, key=scores.get): 1.0}
            return {"TQQQ": 1.0}

    def Rebalance(self):
        if self.IsWarmingUp:
            return
        if not all([
            self.rsi_tqqq.IsReady, self.rsi_soxl.IsReady,
            self.rsi_sqqq.IsReady, self.rsi_bsv.IsReady,
            self.sma_200.IsReady, self.sma_20.IsReady,
        ]):
            return

        target = self._get_target()
        total_value = self.Portfolio.TotalPortfolioValue
        if total_value == 0:
            return

        # Check if any holding drifts beyond the rebalance threshold
        needs_rebalance = any(
            holding.Invested and holding.Symbol.Value not in target
            for holding in self.Portfolio.Values
        )
        if not needs_rebalance:
            for ticker, target_weight in target.items():
                current_weight = self.Portfolio[ticker].HoldingsValue / total_value
                if abs(current_weight - target_weight) > self.REBALANCE_THRESHOLD:
                    needs_rebalance = True
                    break

        if not needs_rebalance:
            return

        for holding in self.Portfolio.Values:
            if holding.Invested and holding.Symbol.Value not in target:
                self.Liquidate(holding.Symbol)

        for ticker, weight in target.items():
            self.SetHoldings(ticker, weight)

    def OnData(self, data):
        pass
