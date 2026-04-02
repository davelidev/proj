# region imports
from AlgorithmImports import *
from datetime import datetime, timedelta
# endregion

class TQQQSimpleLongTerm(QCAlgorithm):
    """
    TQQQ simple long term
    Converted from Composer Symphony DSL.
    Asset class : EQUITIES
    Rebalance frequency : daily
    """

    def Initialize(self):
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100_000)

        # ── Assets ────────────────────────────────────────────────────────────
        tickers = [
            "SPY",   # SPDR S&P 500 ETF Trust
            "TQQQ",  # ProShares UltraPro QQQ
            "SQQQ",  # ProShares UltraPro Short QQQ
            "UVXY",  # ProShares Ultra VIX Short-Term Futures ETF
            "SPXL",  # Direxion Daily S&P 500 Bull 3x Shares
            "UPRO",  # ProShares UltraPro S&P500
            "TLT",   # iShares 20+ Year Treasury Bond ETF
        ]
        self._sym: dict[str, Symbol] = {}
        for t in tickers:
            self._sym[t] = self.AddEquity(t, Resolution.Daily).Symbol

        # ── Indicators ────────────────────────────────────────────────────────
        rsi_tickers = ["TQQQ", "SPY", "SPXL", "SQQQ"]
        self._rsi: dict[tuple, RelativeStrengthIndex] = {}
        for t in rsi_tickers:
            self._rsi[(t, 10)] = self.RSI(
                self._sym[t], 10, MovingAverageType.Wilders, Resolution.Daily
            )

        self._sma: dict[tuple, SimpleMovingAverage] = {
            ("SPY",  200): self.SMA(self._sym["SPY"],  200, Resolution.Daily),
            ("TQQQ",  20): self.SMA(self._sym["TQQQ"],  20, Resolution.Daily),
        }

        warmup = 205
        self.SetWarmUp(warmup, Resolution.Daily)

        # ── Schedule daily rebalance ───────────────────────────────────────────
        self.Schedule.On(
            self.DateRules.EveryDay("SPY"),
            self.TimeRules.AfterMarketOpen("SPY", 30),
            self._rebalance,
        )

    # ─── Helpers ──────────────────────────────────────────────────────────────

    def _price(self, t: str):
        sec = self.Securities[self._sym[t]]
        return float(sec.Price) if sec.HasData else None

    def _sma_v(self, t: str, w: int):
        ind = self._sma.get((t, w))
        return float(ind.Current.Value) if ind and ind.IsReady else None

    def _rsi_v(self, t: str, w: int):
        ind = self._rsi.get((t, w))
        return float(ind.Current.Value) if ind and ind.IsReady else None

    def _top_rsi10(self, tickers):
        """(filter (rsi {:window 10}) (select-top 1) tickers)"""
        scored = [(t, self._rsi_v(t, 10)) for t in tickers]
        valid  = [(t, v) for t, v in scored if v is not None]
        return max(valid, key=lambda x: x[1])[0] if valid else tickers[0]

    # ─── Strategy logic ───────────────────────────────────────────────────────

    def _select_target(self):
        """
        Top-level routing:

        IF SPY > SPY_MA200  (bull market):
            IF TQQQ_RSI10 > 79  → UVXY
            ELSE IF SPXL_RSI10 > 80  → UVXY
            ELSE  → TQQQ

        ELSE  (bear market):
            IF TQQQ_RSI10 < 31  → TQQQ  (oversold bounce)
            ELSE IF SPY_RSI10 < 30  → UPRO  (SPY oversold bounce)
            ELSE:
                IF TQQQ < TQQQ_MA20  (TQQQ below short-term MA):
                    → top RSI10 of [SQQQ, TLT]   (strongest defensive)
                ELSE  (TQQQ above MA20):
                    IF SQQQ_RSI10 < 31  → SQQQ   (SQQQ oversold short entry)
                    ELSE  → TQQQ
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

            return "TQQQ"

        else:
            # ── Bear market ──────────────────────────────────────────────────
            tqqq_rsi10 = self._rsi_v("TQQQ", 10)
            if tqqq_rsi10 is not None and tqqq_rsi10 < 31.0:
                return "TQQQ"

            spy_rsi10 = self._rsi_v("SPY", 10)
            if spy_rsi10 is not None and spy_rsi10 < 30.0:
                return "UPRO"

            tqqq_p  = self._price("TQQQ")
            tqqq_ma = self._sma_v("TQQQ", 20)
            if tqqq_p is not None and tqqq_ma is not None and tqqq_p < tqqq_ma:
                # TQQQ in short-term downtrend → strongest defensive
                return self._top_rsi10(["SQQQ", "TLT"])
            else:
                # TQQQ above MA20
                sqqq_rsi10 = self._rsi_v("SQQQ", 10)
                if sqqq_rsi10 is not None and sqqq_rsi10 < 31.0:
                    return "SQQQ"
                return "TQQQ"

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

        # Liquidate everything except target, then go 100% target
        for t, sym in self._sym.items():
            if t != target and self.Portfolio[sym].Invested:
                self.Liquidate(sym)

        if not self.Portfolio[target_sym].Invested:
            self.SetHoldings(target_sym, 1.0)
            self.Log(f"Rebalanced → {target}")
