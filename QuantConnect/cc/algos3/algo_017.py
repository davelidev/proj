from AlgorithmImports import *


class Algo017(QCAlgorithm):
    """TQQQ vol compression-then-expansion: enter when ATR(14)/ATR(14, 60d ago) < 0.6 AND 20d high; exit on ratio > 1.2 or 15d hold."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.atr = self.ATR(self.tqqq, 14, MovingAverageType.Simple, Resolution.Daily)

        self.compression = 0.6
        self.expansion = 1.2
        self.high_lookback = 20
        self.atr_lag = 60
        self.max_hold = 15

        self.in_position = False
        self.days_held = 0

        self.SetWarmUp(90, Resolution.Daily)

    def OnData(self, data):
        if self.IsWarmingUp:
            return
        if not data.ContainsKey(self.tqqq):
            return
        if not self.atr.IsReady:
            return

        # Get history: enough for atr_lag + 14 (ATR window) + buffer
        bars_needed = self.atr_lag + 30
        hist = self.History(self.tqqq, bars_needed, Resolution.Daily)
        if hist is None or hist.empty:
            return
        try:
            highs = hist["high"]
            lows = hist["low"]
            closes = hist["close"]
        except Exception:
            return
        if len(closes) < self.atr_lag + 15:
            return

        # Compute ATR(14) value 60 days ago using simple TR average
        def tr(i):
            h = highs.iloc[i]
            l = lows.iloc[i]
            pc = closes.iloc[i - 1]
            return max(h - l, abs(h - pc), abs(l - pc))

        # current ATR from indicator
        atr_now = self.atr.Current.Value

        # historical ATR: end index = len - 1 - atr_lag
        end_idx = len(closes) - 1 - self.atr_lag
        start_idx = end_idx - 14 + 1
        if start_idx < 1:
            return
        tr_vals = [tr(i) for i in range(start_idx, end_idx + 1)]
        atr_then = sum(tr_vals) / len(tr_vals)
        if atr_then <= 0:
            return

        ratio = atr_now / atr_then

        # 20d high check using last 20 closes
        recent_closes = closes.iloc[-self.high_lookback:]
        today_close = closes.iloc[-1]
        is_20d_high = today_close >= recent_closes.max()

        if self.in_position:
            self.days_held += 1
            if ratio > self.expansion or self.days_held >= self.max_hold:
                self.Liquidate()
                self.in_position = False
                self.days_held = 0
        else:
            if ratio < self.compression and is_20d_high:
                self.SetHoldings(self.tqqq, 1.0)
                self.in_position = True
                self.days_held = 0
