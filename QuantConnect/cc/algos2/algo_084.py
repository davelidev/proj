from AlgorithmImports import *


class Algo084(QCAlgorithm):
    """Dual-Asset Momentum Rotation: SPY vs TLT, 6-month return.
    Hold whichever is higher at 100%. If both negative, hold cash. Monthly rebalance."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        self.tlt = self.AddEquity("TLT", Resolution.Daily).Symbol
        self.assets = [self.spy, self.tlt]

        self.lookback = 126  # ~6 months trading days

        self.Schedule.On(
            self.DateRules.MonthStart("SPY"),
            self.TimeRules.At(10, 0),
            self.Rebalance,
        )

    def _six_month_return(self, sym):
        hist = self.History(sym, self.lookback, Resolution.Daily)
        if hist is None or hist.empty:
            return None
        try:
            closes = hist["close"]
        except Exception:
            return None
        if len(closes) < 2:
            return None
        first = float(closes.iloc[0])
        last = float(closes.iloc[-1])
        if first <= 0:
            return None
        return (last / first) - 1.0

    def Rebalance(self):
        spy_ret = self._six_month_return(self.spy)
        tlt_ret = self._six_month_return(self.tlt)

        if spy_ret is None or tlt_ret is None:
            return

        # If both negative → cash
        if spy_ret < 0 and tlt_ret < 0:
            for sym in self.assets:
                if self.Portfolio[sym].Invested:
                    self.Liquidate(sym)
            return

        winner = self.spy if spy_ret >= tlt_ret else self.tlt
        loser = self.tlt if winner == self.spy else self.spy

        if self.Portfolio[loser].Invested:
            self.Liquidate(loser)
        self.SetHoldings(winner, 1.0)
