from AlgorithmImports import *


class Algo090(QCAlgorithm):
    """
    Equal-Weight Top 3 Leveraged Sector ETFs by 3mo Momentum.

    Universe: 7 leveraged sector ETFs:
        TQQQ (3x Nasdaq), TECL (3x Tech), SOXL (3x Semis),
        FAS (3x Financials), CURE (3x Healthcare),
        DPST (3x Regional Banks), TNA (3x Small Cap).
    Each month, rank by 3-month return (63d). Hold top 3 equal-weight (1/3 each).
    No trend gate. Liquidate non-winners.
    """

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tickers = ["TQQQ", "TECL", "SOXL", "FAS", "CURE", "DPST", "TNA"]
        self.symbols = []
        for t in self.tickers:
            eq = self.AddEquity(t, Resolution.Daily)
            self.symbols.append(eq.Symbol)

        self.SetWarmUp(80, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.MonthStart(self.symbols[0]),
            self.TimeRules.AfterMarketOpen(self.symbols[0], 30),
            self.MonthlyRebalance,
        )

    def _ret_3mo(self, sym):
        history = self.History([sym], 70, Resolution.Daily)
        if history.empty:
            return None
        try:
            closes = history.loc[sym]["close"].values
        except Exception:
            return None
        if len(closes) < 64:
            return None
        prev = closes[-64]
        last = closes[-1]
        if prev <= 0:
            return None
        return last / prev - 1.0

    def MonthlyRebalance(self):
        if self.IsWarmingUp:
            return

        scored = []
        for sym in self.symbols:
            r = self._ret_3mo(sym)
            if r is not None:
                scored.append((sym, r))

        if len(scored) < 3:
            return

        scored.sort(key=lambda x: x[1], reverse=True)
        winners = [s for s, _ in scored[:3]]
        winner_set = set(winners)

        # Liquidate non-winners
        for sym in self.symbols:
            if sym not in winner_set and self.Portfolio[sym].Invested:
                self.SetHoldings(sym, 0.0)

        # Equal-weight 1/3 each
        target = 1.0 / 3.0
        for sym in winners:
            self.SetHoldings(sym, target)
