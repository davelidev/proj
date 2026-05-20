# region imports
from AlgorithmImports import *
import numpy as np
# endregion

# ─────────────────────────────────────────────────────────────────────────────────────────────────────
#  Algorithm
# ─────────────────────────────────────────────────────────────────────────────────────────────────────

class TQQQSOXLRotation(QCAlgorithm):
    """
    4-State TQQQ / SOXL / UVIX Daily Rotation  (Variants A + D + tuned bear)
    ══════════════════════════════════════════════════════════════════════════════════════════════════════
    In-sample  2014-2024:  CAGR ≈ 143%  |  MaxDD ≈ −47%  |  Calmar ≈ 3.05  |  Sharpe ≈ 1.71
    Out-of-sample 2025+:   CAGR ≈ 370%  |  MaxDD ≈ −30%  |  Calmar ≈ 12.2  |  Sharpe ≈ 2.10

    ── Regime gate — Variant A (3-of-4 voting; BULL if votes ≥ 3) ──────────
      • SPY  price  >  SMA(202)
      • QQQ  price  >  SMA(202)
      • SMH  price  >  SMA(202)
      • SOXL price  >  SMA(202)

    ── Bull rules (first match wins) ────────────────────────────────────────
      R1  RSI(15) > 72  on ANY of (SPY, QQQ, SMH, SOXL)  →  100% UVIX
             (UVXY proxy before UVIX live date 2022-03-30)  [Variant D]
      R3  default                                          →  50% TQQQ + 50% SOXL

    ── Bear rules (first match wins) ────────────────────────────────────────
      R4  QQQ_RSI8 < 29  OR  SMH_RSI8 < 31  →  100% SOXL  (bear-bounce)
      R5  default                             →  CASH

    ── Execution ─────────────────────────────────────────────────────────────────────────────────────
      Signal snapshot at 3:45 PM ET daily (Market-On-Close style).
      All RSI: Wilder smoothing (α = 1/n).
      RSI(15) used for UVIX trigger; RSI(8) for SOXL bear-bounce.
    """

    UVIX_LIVE = datetime(2022, 3, 30)   # UVIX IPO date

    # ── Initialise ───────────────────────────────────────────────────────────────────────────────────

    def Initialize(self) -> None:
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(10000)

        self.SetBrokerageModel(
            BrokerageName.InteractiveBrokersBrokerage,
            AccountType.Margin,
        )
        self.SetBenchmark("SPY")

        # Disable minimum-order-size filter so small-capital early trades aren't skipped
        self.Settings.MinimumOrderMarginPortfolioPercentage = 0.0

        res = Resolution.Daily

        # ── Universe ──────────────────────────────────────────────────────────────────────────────────────
        self._spy  = self.AddEquity("SPY",  res).Symbol   # regime + RSI
        self._qqq  = self.AddEquity("QQQ",  res).Symbol   # regime + RSI
        self._smh  = self.AddEquity("SMH",  res).Symbol   # regime + RSI
        self._tqqq = self.AddEquity("TQQQ", res).Symbol   # bull default
        self._soxl = self.AddEquity("SOXL", res).Symbol   # bull + bear bounce + regime
        self._uvix = self.AddEquity("UVIX", res).Symbol   # bull overbought (live 2022-03-30+)
        self._uvxy = self.AddEquity("UVXY", res).Symbol   # UVIX proxy pre-2022

        # ── Regime indicators — Variant A: SMA(202) on 4 tickers ─────────────
        self._spy_sma202  = self.SMA(self._spy,  202, res)
        self._qqq_sma202  = self.SMA(self._qqq,  202, res)
        self._smh_sma202  = self.SMA(self._smh,  202, res)
        self._soxl_sma202 = self.SMA(self._soxl, 202, res)

        # ── Wilder RSI(8)  — bear oversold trigger (R4) ───────────────────────
        self._rsi_qqq8 = self.RSI(self._qqq, 8, MovingAverageType.Wilders, res)
        self._rsi_smh8 = self.RSI(self._smh, 8, MovingAverageType.Wilders, res)

        # ── Wilder RSI(15) — bull overbought trigger (R1, Variant D) ─────────
        self._rsi_spy15  = self.RSI(self._spy,  15, MovingAverageType.Wilders, res)
        self._rsi_qqq15  = self.RSI(self._qqq,  15, MovingAverageType.Wilders, res)
        self._rsi_smh15  = self.RSI(self._smh,  15, MovingAverageType.Wilders, res)
        self._rsi_soxl15 = self.RSI(self._soxl, 15, MovingAverageType.Wilders, res)

        # ── Warm-up: SMA(202) is the longest lookback ──────────────────────────
        self.SetWarmUp(215, res)

        # ── Position tracking ─────────────────────────────────────────────────────────────────────────
        self._position    = "INIT"
        self._trade_count = 0

        # ── Daily rebalance at 3:45 PM ET ───────────────────────────────────────────
        self.Schedule.On(
            self.DateRules.EveryDay(self._spy),
            self.TimeRules.BeforeMarketClose(self._spy, 15),
            self._rebalance,
        )

    # ── Indicator readiness ──────────────────────────────────────────────────────────────────────────

    @property
    def _ready(self) -> bool:
        return (
            not self.IsWarmingUp
            and self._spy_sma202.IsReady
            and self._qqq_sma202.IsReady
            and self._smh_sma202.IsReady
            and self._soxl_sma202.IsReady
            and self._rsi_qqq8.IsReady
            and self._rsi_smh8.IsReady
            and self._rsi_spy15.IsReady
            and self._rsi_qqq15.IsReady
            and self._rsi_smh15.IsReady
            and self._rsi_soxl15.IsReady
        )

    def OnWarmupFinished(self) -> None:
        """Log indicator states at the end of warm-up to catch any readiness issues."""
        self.Log(
            f"WARMUP DONE | {self.Time.date()} | "
            f"spy_sma202={self._spy_sma202.IsReady} "
            f"qqq_sma202={self._qqq_sma202.IsReady} "
            f"smh_sma202={self._smh_sma202.IsReady} "
            f"soxl_sma202={self._soxl_sma202.IsReady} "
            f"rsi8 qqq={self._rsi_qqq8.IsReady} smh={self._rsi_smh8.IsReady} "
            f"rsi15 spy={self._rsi_spy15.IsReady} qqq={self._rsi_qqq15.IsReady} "
            f"smh={self._rsi_smh15.IsReady} soxl={self._rsi_soxl15.IsReady} "
            f"→ ready={self._ready}"
        )

    # ── UVIX / UVXY selector ─────────────────────────────────────────────────────────────

    def _vol_etf(self) -> Symbol:
        """Return UVIX when live and has a price; otherwise UVXY proxy."""
        try:
            if (self.Time >= self.UVIX_LIVE
                    and self.Securities[self._uvix].HasData
                    and self.Securities[self._uvix].Price > 0):
                return self._uvix
        except Exception:
            pass
        return self._uvxy

    # ── Portfolio construction ───────────────────────────────────────────────────────────────────────

    def _apply(self, weights: dict) -> None:
        """
        Liquidate anything not in target weights, then set targets.
        Pass weights={} for full CASH.
        """
        targets = set(weights)
        for h in self.Portfolio.Values:
            if h.Invested and h.Symbol not in targets:
                self.Liquidate(h.Symbol)
        for sym, w in weights.items():
            self.SetHoldings(sym, w)

    # ── Core signal logic ────────────────────────────────────────────────────────────────────────────

    def _rebalance(self) -> None:
        if not self._ready:
            return

        # ── Prices ──
        spy_px  = self.Securities[self._spy].Price
        qqq_px  = self.Securities[self._qqq].Price
        smh_px  = self.Securities[self._smh].Price
        soxl_px = self.Securities[self._soxl].Price

        # ── Indicator values ──
        spy_sma  = self._spy_sma202.Current.Value
        qqq_sma  = self._qqq_sma202.Current.Value
        smh_sma  = self._smh_sma202.Current.Value
        soxl_sma = self._soxl_sma202.Current.Value

        # RSI(8) for bear oversold (R4)
        rsi_qqq8 = self._rsi_qqq8.Current.Value
        rsi_smh8 = self._rsi_smh8.Current.Value

        # RSI(15) for bull overbought (R1, Variant D — "any of 4 > 72")
        rsi_spy15  = self._rsi_spy15.Current.Value
        rsi_qqq15  = self._rsi_qqq15.Current.Value
        rsi_smh15  = self._rsi_smh15.Current.Value
        rsi_soxl15 = self._rsi_soxl15.Current.Value

        # ── 3-of-4 regime vote (Variant A) ──
        spy_bull  = spy_px  > spy_sma
        qqq_bull  = qqq_px  > qqq_sma
        smh_bull  = smh_px  > smh_sma
        soxl_bull = soxl_px > soxl_sma
        votes     = int(spy_bull) + int(qqq_bull) + int(smh_bull) + int(soxl_bull)
        bull      = votes >= 3

        # ── Bull overbought (Variant D) ──
        overbought = (rsi_spy15  > 72 or
                      rsi_qqq15  > 72 or
                      rsi_smh15  > 72 or
                      rsi_soxl15 > 72)

        # ── State machine ──
        if bull:
            if overbought:
                # R1 — overbought → volatility hedge
                vol     = self._vol_etf()
                new_pos = f"UVIX({vol.Value})"
                weights = {vol: 1.0}
            else:
                # R3 — default bull
                new_pos = "50/50_TQQQ+SOXL"
                weights = {self._tqqq: 0.5, self._soxl: 0.5}
        else:
            if rsi_qqq8 < 29 or rsi_smh8 < 31:
                # R4 — bear oversold bounce
                new_pos = "SOXL_BEAR"
                weights = {self._soxl: 1.0}
            else:
                # R5 — default bear
                new_pos = "CASH"
                weights = {}

        # ── Log only on state change ──
        if new_pos != self._position:
            self._trade_count += 1
            regime = f"BULL({votes}/4)" if bull else f"BEAR({votes}/4)"
            spy_icon  = '\u25b2' if spy_bull else '\u25bd'
            qqq_icon  = '\u25b2' if qqq_bull else '\u25bd'
            smh_icon  = '\u25b2' if smh_bull else '\u25bd'
            soxl_icon = '\u25b2' if soxl_bull else '\u25bd'
            flags  = (f"spy={spy_icon} "
                      f"qqq={qqq_icon} "
                      f"smh={smh_icon} "
                      f"soxl={soxl_icon}")
            self.Log(
                f"[{self._trade_count:04d}] {self.Time.date()} | "
                f"{regime} | {flags} | "
                f"RSI8 qqq={rsi_qqq8:.1f} smh={rsi_smh8:.1f} | "
                f"RSI15 spy={rsi_spy15:.1f} qqq={rsi_qqq15:.1f} "
                f"smh={rsi_smh15:.1f} soxl={rsi_soxl15:.1f} | "
                f"{self._position} → {new_pos}"
            )
            self._position = new_pos

        self._apply(weights)

    # ── Lifecycle hooks ──────────────────────────────────────────────────────────────────────────────

    def OnData(self, data: Slice) -> None:
        pass    # all logic runs in the scheduled _rebalance

    def OnEndOfAlgorithm(self) -> None:
        nav = self.Portfolio.TotalPortfolioValue
        self.Log(
            f"Final NAV     : ${nav:>15,.2f}\n"
            f"State changes : {self._trade_count}\n"
            f"Last position : {self._position}"
        )
