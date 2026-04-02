# It is what it is 0.0.0.3
# Converted from Composer symphony to QuantConnect
#
# Structure: a chain of 11 overbought RSI guards — any trigger → UVXY 100%.
# If none trigger, enter the QQQ regime block:
#
#   max_drawdown(QQQ, 200) > 10%  ["medium crash happened recently"]
#     QQQ > SMA(QQQ, 200)  ["recovered"]
#       cumret(QQQ, 200) > 40%  → PSQ
#       else                    → TQQQ
#     QQQ ≤ SMA(QQQ, 200)  ["still below — sideways risk"]
#       cumret(QQQ, 200) > 5%   → SQQQ
#       else                    → QLD
#   else  ["no medium crash — watch for overextension"]
#     cumret(QQQ, 200) > 15%    → PSQ
#     else                      → TQQQ
#
# Rebalance threshold: 10%.

from AlgorithmImports import *


class ItIsWhatItIs0003(QCAlgorithm):

    # Checked in order; first trigger → UVXY
    UVXY_GUARDS = [
        ("QQQE", 10, 79),
        ("VTV",  10, 79),
        ("VOX",  10, 79),
        ("TECL", 10, 79),
        ("VOOG", 10, 79),
        ("VOOV", 10, 79),
        ("XLP",  10, 75),
        ("TQQQ", 10, 79),
        ("XLY",  10, 80),
        ("FAS",  10, 80),
        ("SPY",  10, 80),
    ]

    REBALANCE_THRESHOLD = 0.10
    LOOKBACK = 200

    def Initialize(self):
        self.SetStartDate(2019, 1, 1)
        self.SetCash(100000)
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.Margin)

        guard_tickers = {t for t, _, _ in self.UVXY_GUARDS}
        for ticker in guard_tickers | {"UVXY", "QQQ", "TQQQ", "QLD", "PSQ", "SQQQ"}:
            self.AddEquity(ticker, Resolution.Daily)

        # One RSI indicator per unique (ticker, window) pair
        self.rsi = {}
        for ticker, window, _ in self.UVXY_GUARDS:
            key = (ticker, window)
            if key not in self.rsi:
                self.rsi[key] = self.RSI(ticker, window, MovingAverageType.Wilders, Resolution.Daily)

        self.sma_qqq_200 = self.SMA("QQQ", self.LOOKBACK, Resolution.Daily)

        self.SetWarmUp(self.LOOKBACK + 10, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay("QQQ"),
            self.TimeRules.AfterMarketOpen("QQQ", 1),
            self.Rebalance,
        )

    def _is_ready(self):
        return all(ind.IsReady for ind in self.rsi.values()) and self.sma_qqq_200.IsReady

    def _cumret(self, ticker, window):
        """Percentage return over `window` trading days."""
        history = self.History(ticker, window + 1, Resolution.Daily)
        if history.empty or len(history) < window + 1:
            return None
        closes = history["close"]
        return (closes.iloc[-1] / closes.iloc[0] - 1) * 100

    def _max_drawdown(self, ticker, window):
        """Max peak-to-trough decline (%) over the last `window` trading days."""
        history = self.History(ticker, window, Resolution.Daily)
        if history.empty or len(history) < window:
            return None
        closes = history["close"].values
        peak, max_dd = closes[0], 0.0
        for price in closes[1:]:
            if price > peak:
                peak = price
            dd = (peak - price) / peak * 100
            if dd > max_dd:
                max_dd = dd
        return max_dd

    def _get_target(self):
        # --- Overbought guard chain ---
        for ticker, window, threshold in self.UVXY_GUARDS:
            if self.rsi[(ticker, window)].Current.Value > threshold:
                return {"UVXY": 1.0}

        # --- QQQ regime block ---
        max_dd = self._max_drawdown("QQQ", self.LOOKBACK)
        cumret = self._cumret("QQQ", self.LOOKBACK)
        if max_dd is None or cumret is None:
            return None

        if max_dd > 10:
            if self.Securities["QQQ"].Price > self.sma_qqq_200.Current.Value:
                return {"PSQ": 1.0} if cumret > 40 else {"TQQQ": 1.0}
            else:
                return {"SQQQ": 1.0} if cumret > 5 else {"QLD": 1.0}
        else:
            return {"PSQ": 1.0} if cumret > 15 else {"TQQQ": 1.0}

    def Rebalance(self):
        if self.IsWarmingUp or not self._is_ready():
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
