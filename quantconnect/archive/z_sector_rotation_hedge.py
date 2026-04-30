# region imports
from AlgorithmImports import *
from datetime import datetime, timedelta
# endregion

class HedgedSectorRotator(QCAlgorithm):
    """
    "Copy of Hedged Sector Rotator"
    60/40: andrew.thomas.taylor's Sector Rotator / DereckN's Hedge System
    Rebalance: Daily

    ── Component 1 (60%): Sector Rotator ─────────────────────────────────────
    Guard:  If ANY sector RSI(10) > 80  → hold UVXY  (overbought hedge)
    Buy:    Else if ANY sector RSI(10) < 30 → hold best asset in that sector
            (sector ETF, leveraged ETF, or SVXY ranked by MA return,
             filtered above sector's MA filter window)
    Else:   Hold the asset with the lowest 10-day std-dev return across all
            sector groups (sector ETF or leveraged ETF, above 200-day MA)

    Sectors checked in order:
        XLK, XLF, XLV, XLE, XLB, XTL, XLRE, XLY, XLI, XLU, XLP

    Sector pairs (sector ETF → leveraged ETF):
        XLK → TECL (3x Tech),  XLF → FAS (3x Fin),  XLV → CURE (3x HC),
        XLE → ERX (2x Energy), XLB → UYM (2x Mat),  XTL → LTL (2x Telecom),
        XLRE → DRN (3x RE),    XLY → WANT (3x Disc), XLI → DUSL (3x Ind),
        XLU → UTSL (3x Util),  XLP → UGE (2x Staples)

    MA-return sort window: 200 days for XLK; 10 days for all others
    MA filter window:      200 days for all except XLP (10 days)
    SVXY included as 3rd candidate for all sectors except XLK

    ── Component 2 (40%): DereckN Hedge System ───────────────────────────────
    5 equal sub-strategies at 8% each:

    1. TMV Momentum:     QQQ/SPY RSI > 80 → VIXY; else TMF RSI tree → TMF/SHV/TECL
    2. TMF Momentum:     Same logic as TMV Momentum
    3. SVXY FTLT:        QQQ/SPY RSI > 80 → VIXY; else oversold sector ETF; else SHV
    4. TINA:             QQQ 10-day return > 5.5% → PSQ;
                         TQQQ 62-day return < -33% → TQQQ; else TQQQ
    5. SVXY FTLT V2:     QQQ/SPY RSI > 80 → UVXY; else SVXY vs 21-day SMA → SVXY/BTAL

    Note: XTL (SPDR S&P Telecom) was delisted in 2021; the algo will skip its
    RSI check gracefully when historical data is unavailable.
    """

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.Margin)

        # Daily rebalance 30 min after open
        self.Schedule.On(
            self.DateRules.EveryDay("SPY"),
            self.TimeRules.AfterMarketOpen("SPY", 30),
            self.Rebalance,
        )

        # ── Sector groups ──────────────────────────────────────────────────────
        # Order matters: RSI checks run in this sequence
        self.sector_order = [
            "XLK", "XLF", "XLV", "XLE", "XLB",
            "XTL", "XLRE", "XLY", "XLI", "XLU", "XLP",
        ]

        # sector → {sector, levered, use_svxy, sort_window, filter_window}
        self.sector_cfg = {
            "XLK":  dict(sector="XLK",  levered="TECL", use_svxy=False, sort_w=200, filter_w=200),
            "XLF":  dict(sector="XLF",  levered="FAS",  use_svxy=True,  sort_w=10,  filter_w=200),
            "XLV":  dict(sector="XLV",  levered="CURE", use_svxy=True,  sort_w=10,  filter_w=200),
            "XLE":  dict(sector="XLE",  levered="ERX",  use_svxy=True,  sort_w=10,  filter_w=200),
            "XLB":  dict(sector="XLB",  levered="UYM",  use_svxy=True,  sort_w=10,  filter_w=200),
            "XTL":  dict(sector="XTL",  levered="LTL",  use_svxy=True,  sort_w=10,  filter_w=200),
            "XLRE": dict(sector="XLRE", levered="DRN",  use_svxy=True,  sort_w=10,  filter_w=200),
            "XLY":  dict(sector="XLY",  levered="WANT", use_svxy=True,  sort_w=10,  filter_w=200),
            "XLI":  dict(sector="XLI",  levered="DUSL", use_svxy=True,  sort_w=10,  filter_w=200),
            "XLU":  dict(sector="XLU",  levered="UTSL", use_svxy=True,  sort_w=10,  filter_w=200),
            "XLP":  dict(sector="XLP",  levered="UGE",  use_svxy=True,  sort_w=10,  filter_w=10),
        }

        # ── Securities ────────────────────────────────────────────────────────
        all_tickers: set[str] = set()
        for cfg in self.sector_cfg.values():
            all_tickers.update([cfg["sector"], cfg["levered"]])
        all_tickers.update([
            "UVXY", "SVXY", "VIXY",
            "QQQ",  "SPY",
            "TMF",  "TMV", "SHV", "BIL", "TLT",
            "TECL", "TQQQ",
            "PSQ",  "VTI", "VIXM", "BTAL",
        ])

        self.syms: dict[str, Symbol] = {}
        for ticker in sorted(all_tickers):
            try:
                self.syms[ticker] = self.AddEquity(ticker, Resolution.Daily).Symbol
            except Exception as e:
                self.Debug(f"[Init] Could not add {ticker}: {e}")

        # ── RSI indicators ────────────────────────────────────────────────────
        # RSI(10) for sector ETFs and key hedge tickers
        rsi10_tickers = self.sector_order + ["QQQ", "SPY", "TMF", "TQQQ", "SVXY"]
        self.rsi10: dict[str, RelativeStrengthIndex] = {}
        for t in rsi10_tickers:
            if t in self.syms:
                self.rsi10[t] = self.RSI(self.syms[t], 10, MovingAverageType.Wilders, Resolution.Daily)

        # Special-window RSIs for hedge sub-strategy 1/2
        self.rsi_bil30 = (
            self.RSI(self.syms["BIL"], 30, MovingAverageType.Wilders, Resolution.Daily)
            if "BIL" in self.syms else None
        )
        self.rsi_tlt20 = (
            self.RSI(self.syms["TLT"], 20, MovingAverageType.Wilders, Resolution.Daily)
            if "TLT" in self.syms else None
        )

        # TMF EMA(8) and SMA(10)
        self.ema_tmf8 = (
            self.EMA(self.syms["TMF"], 8,  Resolution.Daily)
            if "TMF" in self.syms else None
        )
        self.sma_tmf10 = (
            self.SMA(self.syms["TMF"], 10, Resolution.Daily)
            if "TMF" in self.syms else None
        )

        # SVXY SMA(21) for sub-strategy 5
        self.sma_svxy21 = (
            self.SMA(self.syms["SVXY"], 21, Resolution.Daily)
            if "SVXY" in self.syms else None
        )

        # Warm up enough bars for the longest MA (200 days + RSI buffer)
        self.SetWarmUp(220, Resolution.Daily)

    # ── Utility helpers ────────────────────────────────────────────────────────

    def _closes(self, ticker: str, window: int) -> list[float] | None:
        """Return `window` daily closes for ticker, or None if unavailable."""
        if ticker not in self.syms:
            return None
        hist = self.History(self.syms[ticker], window, Resolution.Daily)
        if hist.empty or len(hist) < window:
            return None
        return list(hist["close"])

    def _ma_return(self, ticker: str, window: int) -> float:
        """(close[now] / close[window days ago]) - 1; returns -999 on failure."""
        closes = self._closes(ticker, window + 1)
        if closes is None or len(closes) < window + 1:
            return -999.0
        return (closes[-1] / closes[0]) - 1.0

    def _above_sma(self, ticker: str, window: int) -> bool:
        """True if latest close is above the `window`-day simple moving average."""
        closes = self._closes(ticker, window)
        if closes is None:
            return False
        return closes[-1] > (sum(closes) / len(closes))

    def _std_return(self, ticker: str, window: int) -> float:
        """Population std-dev of daily returns over `window` days (lower = less volatile)."""
        closes = self._closes(ticker, window + 1)
        if closes is None or len(closes) < 2:
            return float("inf")
        rets = [(closes[i + 1] / closes[i]) - 1.0 for i in range(len(closes) - 1)]
        mu = sum(rets) / len(rets)
        return (sum((r - mu) ** 2 for r in rets) / len(rets)) ** 0.5

    def _cumret(self, ticker: str, window: int) -> float | None:
        """Cumulative return over `window` days, or None on failure."""
        closes = self._closes(ticker, window + 1)
        if closes is None or len(closes) < window + 1:
            return None
        return (closes[-1] / closes[0]) - 1.0

    def _rsi10(self, ticker: str) -> float:
        """Current RSI(10) value, defaulting to 50 if indicator not ready."""
        ind = self.rsi10.get(ticker)
        return float(ind.Current.Value) if (ind and ind.IsReady) else 50.0

    # ── Component 1: Sector Rotator ───────────────────────────────────────────

    def _best_sector_asset(self, trigger: str) -> str:
        """
        For an oversold sector, pick the top-ranked asset from its candidate pool.
        Candidates: [sector ETF, leveraged ETF] + optionally [SVXY]
        Filter:     must be above its MA filter window
        Sort:       by MA return over sort_window (highest wins)
        """
        cfg = self.sector_cfg[trigger]
        candidates = [cfg["sector"], cfg["levered"]]
        if cfg["use_svxy"]:
            candidates.append("SVXY")

        fw = cfg["filter_w"]
        sw = cfg["sort_w"]

        valid = [t for t in candidates if self._above_sma(t, fw)]
        if not valid:
            valid = candidates  # bypass filter if nothing qualifies

        return max(valid, key=lambda t: self._ma_return(t, sw))

    def _sector_rotator_pick(self) -> str:
        """Return the single ticker for the 60% sector rotator slice."""

        # ① Any sector overbought? → hedge with UVXY
        for ticker in self.sector_order:
            if ticker in self.rsi10 and self.rsi10[ticker].IsReady:
                if self._rsi10(ticker) > 80:
                    self.Debug(f"[Rotator] Overbought: {ticker} RSI={self._rsi10(ticker):.1f} → UVXY")
                    return "UVXY"

        # ② Any sector oversold? → buy best asset in that sector group
        for ticker in self.sector_order:
            if ticker in self.rsi10 and self.rsi10[ticker].IsReady:
                if self._rsi10(ticker) < 30:
                    pick = self._best_sector_asset(ticker)
                    self.Debug(f"[Rotator] Oversold: {ticker} RSI={self._rsi10(ticker):.1f} → {pick}")
                    return pick

        # ③ No signal → lowest 10-day volatility asset across all sector groups
        #    (sector ETF or leveraged ETF that is above its 200-day MA)
        candidates = []
        for cfg in self.sector_cfg.values():
            for t in [cfg["sector"], cfg["levered"]]:
                if self._above_sma(t, 200):
                    candidates.append((t, self._std_return(t, 10)))

        if candidates:
            pick = min(candidates, key=lambda x: x[1])[0]
            self.Debug(f"[Rotator] No signal → low-vol fallback: {pick}")
            return pick

        return "XLK"  # ultimate fallback

    # ── Component 2: Hedge sub-strategies ────────────────────────────────────

    def _tmf_momentum_pick(self) -> str:
        """
        Sub-strategies 1 (TMV Momentum) & 2 (TMF Momentum) — identical logic.

        QQQ or SPY RSI(10) > 80 → VIXY
        Else:
          TMF RSI(10) < 32  → TMF
          TMF RSI(10) > 72  → SHV
          EMA(8) < SMA(10) on TMF or otherwise:
            (Both EMA branches) → TQQQ RSI(10) < 31 → TECL; else SHV
        """
        if self._rsi10("QQQ") > 80 or self._rsi10("SPY") > 80:
            return "VIXY"

        tmf_rsi = self._rsi10("TMF")
        if tmf_rsi < 32:
            return "TMF"
        if tmf_rsi > 72:
            return "SHV"

        # TQQQ oversold check (used in all remaining EMA branches)
        return "TECL" if self._rsi10("TQQQ") < 31 else "SHV"

    def _svxy_ftlt_pick(self) -> str:
        """
        Sub-strategy 3: SVXY FTLT

        QQQ or SPY RSI(10) > 80 → VIXY
        Else if any sector oversold → hold that sector's ETF
        Else → SHV (safety)
        """
        if self._rsi10("QQQ") > 80 or self._rsi10("SPY") > 80:
            return "VIXY"

        for ticker in self.sector_order:
            if ticker in self.rsi10 and self.rsi10[ticker].IsReady:
                if self._rsi10(ticker) < 30:
                    return self.sector_cfg[ticker]["sector"]

        return "SHV"

    def _tina_pick(self) -> str:
        """
        Sub-strategy 4: TINA (There Is No Alternative)

        QQQ 10-day return > +5.5% → PSQ  (short QQQ; market exhaustion)
        TQQQ 62-day return < -33% → TQQQ (buy the dip)
        Else                       → TQQQ
        """
        qqq10 = self._cumret("QQQ", 10)
        if qqq10 is not None and qqq10 > 0.055:
            return "PSQ"

        tqqq62 = self._cumret("TQQQ", 62)
        if tqqq62 is not None and tqqq62 < -0.33:
            return "TQQQ"

        return "TQQQ"

    def _svxy_ftlt_v2_pick(self) -> str:
        """
        Sub-strategy 5: SVXY FTLT V2

        QQQ or SPY RSI(10) > 80 → UVXY
        Else if SVXY > 21-day SMA → SVXY  (vol selling regime)
        Else                      → BTAL  (anti-beta hedge)
        """
        if self._rsi10("QQQ") > 80 or self._rsi10("SPY") > 80:
            return "UVXY"

        if self.sma_svxy21 and self.sma_svxy21.IsReady:
            svxy_close = self._closes("SVXY", 1)
            if svxy_close:
                return "SVXY" if svxy_close[-1] > self.sma_svxy21.Current.Value else "BTAL"

        return "VTI"

    # ── Main rebalance ─────────────────────────────────────────────────────────

    def Rebalance(self):
        if self.IsWarmingUp:
            return

        # Require all RSI(10) indicators to be ready before trading
        if not all(ind.IsReady for ind in self.rsi10.values()):
            return

        # ── Build target-weight dict ───────────────────────────────────────────
        targets: dict[str, float] = {}

        def add(ticker: str, weight: float) -> None:
            targets[ticker] = targets.get(ticker, 0.0) + weight

        # Component 1: Sector Rotator → 60%
        add(self._sector_rotator_pick(), 0.60)

        # Component 2: Hedge System → 5 × 8% = 40%
        add(self._tmf_momentum_pick(), 0.08)   # Sub-strategy 1: TMV Momentum
        add(self._tmf_momentum_pick(), 0.08)   # Sub-strategy 2: TMF Momentum
        add(self._svxy_ftlt_pick(),    0.08)   # Sub-strategy 3: SVXY FTLT
        add(self._tina_pick(),          0.08)  # Sub-strategy 4: TINA
        add(self._svxy_ftlt_v2_pick(), 0.08)   # Sub-strategy 5: SVXY FTLT V2

        # ── Execute ────────────────────────────────────────────────────────────
        # Liquidate positions not in the new target set
        for symbol in list(self.Portfolio.Keys):
            if self.Portfolio[symbol].Invested:
                ticker = self.Securities[symbol].Symbol.Value
                if ticker not in targets:
                    self.Liquidate(symbol)

        # Set new target weights
        for ticker, weight in targets.items():
            if ticker in self.syms:
                self.SetHoldings(self.syms[ticker], weight)
            else:
                self.Debug(f"[Rebalance] {ticker} not in universe, skipping")

        self.Debug(f"[Rebalance] Targets: { {k: f'{v:.0%}' for k, v in targets.items()} }")

    def OnData(self, data):
        pass
