from AlgorithmImports import *
from base import START_DATE, END_DATE, INITIAL_CASH, WARMUP_DAYS, SCHEDULE_TICKER, DAILY_OPEN_MIN, BaseSubAlgo
from leveraged_rebalance import LeveragedRebalanceSub
from ibs_basket import IBSATRStopSub
from rsi2_dip_vote import RSIThreeVoteSub
from sma200_rsi_tiers import SMA200RSITiersSub
from sma200_pyramid import SMA200PyramidSub
from sma_five_vote import SMAFiveVoteSub
from donchian_four_vote import DonchianFiveVoteSub
from momentum_vote import MomentumVoteSub
from trend_stretch_exit import TrendStretchExitSub
from golden_cross_atr import GoldenCrossATRSub
from range_compressed import RangeCompressedSub
from mfi14_hyst import MFI14HystSub
from vol_regime_20 import VolRegime20Sub


class CashReserveSub(BaseSubAlgo):
    """Holds 100% BIL. Weight controls the cash reserve fraction."""
    def initialize(self):
        self.bil = self.algo.AddEquity("BIL", Resolution.Daily).Symbol
        self.targets = {self.bil: 1.0}


# ---------------------------------------------------------------------------
# UltimateAlgoNQ — same sub-algos and aggregation as UltimateAlgo, but trades
# Nasdaq-100 e-mini futures (MNQ) instead of the TQQQ/SOXL/TECL ETF basket.
#
# Translation:
#   Each sub still computes targets in {TQQQ, SOXL, TECL, BIL} weights.
#   Aggregator sums all "leveraged-equity" weights into a single NQ exposure:
#       nq_weight = (agg[TQQQ] + agg[SOXL] + agg[TECL]) × LEV_FACTOR
#   where LEV_FACTOR = 3.0 to mimic TQQQ's 3x leverage with unlevered NQ futures.
#   Cash sleeve still holds BIL.
# ---------------------------------------------------------------------------

class UltimateAlgoNQ(QCAlgorithm):
    REBAL_DRIFT       = 0.005  # skip if drift < this
    BIL_MIN_REMAINING = 0.01   # route idle capital to BIL above this fraction
    # Target NQ notional = portfolio_value × lev_eq_weight × LEV_FACTOR
    # LEV_FACTOR=3.0 matches TQQQ's 3x leverage on a 1x NQ contract
    LEV_FACTOR        = 3.0
    MAX_NQ_NOTIONAL   = 3.0    # cap notional at 3x portfolio for safety

    # Symbols that represent leveraged-equity exposure (replace with NQ futures at execution)
    LEV_EQ_TICKERS    = ["TQQQ", "SOXL", "TECL"]

    def Initialize(self):
        self.SetStartDate(*START_DATE)
        self.SetEndDate(*END_DATE)
        # NQ contract value reaches ~$440k by 2025; bump capital so contracts
        # don't round to zero. Use 10x base capital ($1M).
        self.SetCash(INITIAL_CASH * 10)

        # BIL: cash sleeve (held directly)
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol

        # Nasdaq-100 E-mini futures (continuous, back-adjusted prices).
        # Using NQ (full history back to 1999) instead of MNQ (launched May 2019).
        # NQ multiplier = $20/point; needs larger account for granular sizing.
        self.nq_future = self.AddFuture(
            Futures.Indices.NASDAQ100EMini,
            Resolution.Daily,
            dataNormalizationMode=DataNormalizationMode.BackwardsRatio,
            dataMappingMode=DataMappingMode.OpenInterest,
            contractDepthOffset=0,
        )

        self.last_prices = {}
        self._last_year  = None

        sub_specs = [
            (LeveragedRebalanceSub,  "LevRebal",       10),
            (IBSATRStopSub,          "IBSBasket",      20),
            (RSIThreeVoteSub,        "RSI2DipVote",    20),
            (SMA200RSITiersSub,      "SMA200Tiers",    10),
            (SMA200PyramidSub,       "SMA200Pyramid",  10),
            (SMAFiveVoteSub,         "SMA5Vote",       15),
            (DonchianFiveVoteSub,    "D5Vote",         15),
            (MomentumVoteSub,        "MomVote",        10),
            (TrendStretchExitSub,    "StretchExit",    10),
            (GoldenCrossATRSub,      "GoldXATR",       10),
            (RangeCompressedSub,     "RangeCompr",     10),
            (MFI14HystSub,           "MFI14Hyst",      10),
            (VolRegime20Sub,         "VolReg20",       10),
            (CashReserveSub,         "CashReserve",     5),
        ]
        total_w = sum(w for _, _, w in sub_specs)
        self.sub_algos = []
        for cls, name, w in sub_specs:
            sub = cls(self, name)
            sub.weight             = w
            sub.equity             = INITIAL_CASH * w / total_w
            sub.active             = True
            sub.trade_count        = 0
            sub._prev_targets_snap = {}
            sub.initialize()  # subs add TQQQ/SOXL/TECL for indicators (price-only, not held)
            self.sub_algos.append(sub)

        # Cache leveraged-equity symbols (after sub-algos have registered them)
        self.lev_eq_syms = set()
        for ticker in self.LEV_EQ_TICKERS:
            sym = next((s for s in self.Securities.Keys if s.Value == ticker), None)
            if sym is not None:
                self.lev_eq_syms.add(sym)

        self.SetWarmUp(WARMUP_DAYS, Resolution.Daily)
        self.Schedule.On(
            self.DateRules.EveryDay(SCHEDULE_TICKER),
            self.TimeRules.BeforeMarketClose(SCHEDULE_TICKER, 10),
            self.PerformDailyUpdate,
        )

    def _alive(self):
        return [s for s in self.sub_algos if s.active]

    def PerformDailyUpdate(self):
        # Account for P&L of the positions held since the last update BEFORE
        # advancing targets — otherwise the prior day's price move is
        # misattributed to whatever each sub decides today, corrupting virtual
        # equity (and thus the equity-weighted aggregation, incl. the BIL reserve).
        if not self.IsWarmingUp:
            self._update_virtual_accounting()
            self._maybe_yearly_reset()

        for sub in self._alive():
            sub.update_targets()

        if self.IsWarmingUp: return
        self._track_trade_counts()
        self._execute_aggregation()

    def _update_virtual_accounting(self):
        if not self.last_prices:
            for x in self.Securities.Values:
                if x.Price > 0: self.last_prices[x.Symbol] = x.Price
            return

        bil_price  = self.Securities[self.bil].Price
        bil_last   = self.last_prices.get(self.bil, bil_price)
        bil_return = (bil_price / bil_last) - 1 if bil_last > 0 else 0

        for sub in self._alive():
            profit = 0
            for sym, weight in sub.targets.items():
                if sym not in self.Securities: continue
                price = self.Securities[sym].Price
                last  = self.last_prices.get(sym, price)
                if last > 0:
                    profit += weight * ((price / last) - 1)
            cash_weight = max(0, 1.0 - sum(sub.targets.values()))
            profit += cash_weight * bil_return
            sub.equity *= (1 + profit)
            if sub.equity <= 0:
                sub.active = False
                sub.targets = {}
                self.Log(f"SUB DISABLED: {sub.id} virtual equity hit zero")

        for x in self.Securities.Values:
            if x.Price > 0: self.last_prices[x.Symbol] = x.Price

    def _maybe_yearly_reset(self):
        if self.Time.year == self._last_year: return
        self._last_year = self.Time.year
        alive = self._alive()
        if not alive: return
        total_v = sum(s.equity for s in alive)
        total_w = sum(s.weight for s in alive)
        for sub in alive:
            sub.equity = total_v * sub.weight / total_w
        self.Log(f"YEARLY REBALANCE: total=${total_v:,.0f} across {len(alive)} active subs")

    def _track_trade_counts(self):
        for sub in self._alive():
            cur = {s: round(w, 6) for s, w in sub.targets.items() if w != 0}
            if cur != sub._prev_targets_snap:
                sub.trade_count += 1
                sub._prev_targets_snap = cur

    def _execute_aggregation(self):
        total_real = self.Portfolio.TotalPortfolioValue
        if total_real <= 0: return
        alive = self._alive()
        total_v = sum(s.equity for s in alive)
        if total_v <= 0: return

        # Aggregate sub.targets weighted by virtual share
        agg = {}
        for sub in alive:
            share = sub.equity / total_v
            for sym, w in sub.targets.items():
                agg[sym] = agg.get(sym, 0) + w * share

        # Sum all leveraged-equity exposure → target NQ notional
        lev_eq_weight = sum(agg.get(s, 0) for s in self.lev_eq_syms)
        target_notional_pct = min(self.MAX_NQ_NOTIONAL, lev_eq_weight * self.LEV_FACTOR)

        # Cash sleeve: remaining capital → BIL
        bil_weight = agg.get(self.bil, 0)
        # Add any uninvested residual from leveraged-equity bucket
        residual = max(0, 1.0 - lev_eq_weight - bil_weight)
        if residual > self.BIL_MIN_REMAINING:
            bil_weight += residual

        # Execute: NQ futures — compute target contracts explicitly to control notional
        mapped = self.nq_future.Mapped
        if mapped is not None and mapped in self.Securities and self.Securities[mapped].Price > 0:
            contract_price = self.Securities[mapped].Price
            contract_multiplier = self.Securities[mapped].SymbolProperties.ContractMultiplier
            contract_value = contract_price * contract_multiplier  # $ per contract
            target_notional = total_real * target_notional_pct
            target_qty = int(target_notional / contract_value)
            # Current contract quantity across all NQ contracts (handles roll-overs)
            current_qty = sum(
                self.Portfolio[s].Quantity
                for s in self.Portfolio.Keys
                if s.SecurityType == SecurityType.Future and s.Canonical == self.nq_future.Symbol
            )
            diff = target_qty - int(current_qty)
            if diff != 0:
                self.MarketOrder(mapped, diff)

        # Execute: BIL cash sleeve
        bil_cur = self.Portfolio[self.bil].HoldingsValue / total_real
        if abs(bil_weight - bil_cur) > self.REBAL_DRIFT:
            self.SetHoldings(self.bil, bil_weight)

        # Liquidate any TQQQ/SOXL/TECL positions if accidentally invested (shouldn't be)
        for sym in self.lev_eq_syms:
            if self.Portfolio[sym].Invested:
                self.Liquidate(sym)

    # NOTE: deliberately no OnSymbolChangedEvents roll handler.
    # Testing showed explicit early-roll pays ~0.7% calendar spread × 4 rolls/year ≈ 3% drag.
    # Implicit behavior (hold expiring contract → QC cash-settles at expiration → next
    # _execute_aggregation buys the new mapped contract) captures basis convergence.
    # Backtest comparison: implicit = 40%/-34%/1.058 vs explicit = 35%/-34%/0.948.

    def OnEndOfAlgorithm(self):
        for sub in self.sub_algos:
            self.SetRuntimeStatistic(f"trades_{sub.id}", str(sub.trade_count))
