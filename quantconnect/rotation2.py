# region imports
from AlgorithmImports import *
# endregion

class TQQQForTheLongTerm(QCAlgorithm):
    """
    "TQQQ For The Long Term (Reddit Post Link)"
    Asset class: Equities | Rebalance: Daily

    Decision tree (100% in one asset at a time):

    IF SPY > SMA(200):                         ← BULL regime
        IF TQQQ RSI(10) > 79  → UVXY
        ELIF SPXL RSI(10) > 80 → UVXY
        ELSE                   → TQQQ

    ELSE (SPY ≤ SMA(200)):                     ← BEAR regime
        IF TQQQ RSI(10) < 31   → TECL
        ELIF SPY  RSI(10) < 30 → UPRO
        ELIF TQQQ < SMA(20):
            → Top 1 of [SQQQ, TLT] by RSI(10)  (higher RSI wins)
        ELSE (TQQQ ≥ SMA(20)):
            IF SQQQ RSI(10) < 31 → SQQQ
            ELSE                  → TQQQ
    """

    def Initialize(self):
        self.SetStartDate(2020, 1, 1)
        self.SetCash(100_000)
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.Margin)

        self.Schedule.On(
            self.DateRules.EveryDay("SPY"),
            self.TimeRules.AfterMarketOpen("SPY", 30),
            self.Rebalance,
        )

        tickers = ["SPY", "TQQQ", "SPXL", "UVXY", "TECL", "UPRO", "SQQQ", "TLT"]
        self.syms = {t: self.AddEquity(t, Resolution.Daily).Symbol for t in tickers}

        # RSI(10) for all tickers
        self.rsi10 = {
            t: self.RSI(self.syms[t], 10, MovingAverageType.Wilders, Resolution.Daily)
            for t in tickers
        }

        # SMA(200) for SPY — trend filter
        self.sma_spy200 = self.SMA(self.syms["SPY"],  200, Resolution.Daily)
        # SMA(20) for TQQQ — bear-regime sub-filter
        self.sma_tqqq20 = self.SMA(self.syms["TQQQ"], 20,  Resolution.Daily)

        self.SetWarmUp(210, Resolution.Daily)

    def _rsi(self, ticker: str) -> float:
        ind = self.rsi10[ticker]
        return float(ind.Current.Value) if ind.IsReady else 50.0

    def _pick(self) -> str:
        spy_price  = self.Securities[self.syms["SPY"]].Price
        tqqq_price = self.Securities[self.syms["TQQQ"]].Price

        bull = (
            self.sma_spy200.IsReady
            and spy_price > self.sma_spy200.Current.Value
        )

        if bull:
            # ── BULL: SPY above 200-day MA ─────────────────────────────────
            if self._rsi("TQQQ") > 80 or self._rsi("SPXL") > 80:
                return "UVXY"
            return "TQQQ"

        else:
            # ── BEAR: SPY at or below 200-day MA ──────────────────────────
            if self._rsi("TQQQ") < 30 or self._rsi("SPY") < 30:
                return "UPRO"

            tqqq_below_20sma = (
                self.sma_tqqq20.IsReady
                and tqqq_price < self.sma_tqqq20.Current.Value
            )

            if tqqq_below_20sma:
                # Top 1 of [SQQQ, TLT] by RSI(10) — higher RSI wins
                return max(["SQQQ", "TLT"], key=lambda t: self._rsi(t))

            # TQQQ at or above its 20-day MA
            if self._rsi("SQQQ") < 30:
                return "SQQQ"
            return "TQQQ"

    def Rebalance(self):
        if self.IsWarmingUp:
            return
        if not self.sma_spy200.IsReady or not all(i.IsReady for i in self.rsi10.values()):
            return

        pick = self._pick()
        self.Debug(f"[Rebalance] → {pick}")

        for sym in self.Portfolio.Keys:
            if self.Portfolio[sym].Invested and sym != self.syms[pick]:
                self.Liquidate(sym)

        self.SetHoldings(self.syms[pick], 1.0)

    def OnData(self, data):
        pass
