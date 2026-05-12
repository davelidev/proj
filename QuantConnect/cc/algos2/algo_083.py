from AlgorithmImports import *


class Algo083(QCAlgorithm):
    """NR7 Volatility Compression Breakout on QQQ.
    Today's range narrowest of last 7 days → next day buy 100% QQQ.
    Exit: close above 5-day high (reached during trade) OR 10-day max hold."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol

        self.nr7_lookback = 7
        self.exit_high_window = 5
        self.max_hold_days = 10

        # State
        self.signal_armed = False  # NR7 fired today, enter next bar
        self.in_trade = False
        self.days_held = 0

        self.SetWarmUp(self.nr7_lookback + 10, Resolution.Daily)

    def OnData(self, data):
        if self.IsWarmingUp:
            return
        if self.qqq not in data or data[self.qqq] is None:
            return

        # Step 1: if signal_armed from previous bar's close, enter at today's open price (market order at this bar)
        if self.signal_armed and not self.in_trade:
            self.SetHoldings(self.qqq, 1.0)
            self.in_trade = True
            self.days_held = 0
            self.signal_armed = False
            return  # don't evaluate exit on entry day

        # Step 2: manage open position
        if self.in_trade:
            self.days_held += 1

            # Exit on close above 5-day high (using last 5 daily bars including today)
            hist_exit = self.History(self.qqq, self.exit_high_window + 1, Resolution.Daily)
            exit_signal = False
            if hist_exit is not None and not hist_exit.empty:
                try:
                    highs = hist_exit["high"]
                    closes = hist_exit["close"]
                    if len(highs) >= self.exit_high_window + 1 and len(closes) >= 1:
                        # 5-day high excluding today's bar
                        prior_high = float(highs.iloc[:-1].tail(self.exit_high_window).max())
                        today_close = float(closes.iloc[-1])
                        if today_close > prior_high:
                            exit_signal = True
                except Exception:
                    pass

            if exit_signal or self.days_held >= self.max_hold_days:
                if self.Portfolio[self.qqq].Invested:
                    self.Liquidate(self.qqq)
                self.in_trade = False
                self.days_held = 0
                # fall through to potentially re-arm

        # Step 3: check NR7 condition on today's bar (only when flat)
        if not self.in_trade:
            hist = self.History(self.qqq, self.nr7_lookback, Resolution.Daily)
            if hist is None or hist.empty:
                return
            try:
                highs = hist["high"]
                lows = hist["low"]
            except Exception:
                return
            if len(highs) < self.nr7_lookback or len(lows) < self.nr7_lookback:
                return

            ranges = (highs - lows).values
            today_range = float(ranges[-1])
            min_range = float(min(ranges))

            if today_range <= min_range + 1e-12:
                self.signal_armed = True
