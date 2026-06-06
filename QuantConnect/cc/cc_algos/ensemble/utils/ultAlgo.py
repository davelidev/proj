from AlgorithmImports import *
from base import START_DATE, END_DATE, INITIAL_CASH, WARMUP_DAYS, SCHEDULE_TICKER, DAILY_OPEN_MIN, BaseSubAlgo
from leveraged_rebalance import LeveragedRebalanceSub
from ibs_basket import IBSATRStopSub
from rsi2_dip_vote import RSIThreeVoteSub
from range_breakout import RangeBreakoutSub
from sma200_rsi_tiers import SMA200RSITiersSub
from sma150_trend import SMA150TrendSub
from sma200_pyramid import SMA200PyramidSub
from sma_five_vote import SMAFiveVoteSub
from donchian_four_vote import DonchianFourVoteSub
from momentum_vote import MomentumVoteSub
from trend_stretch_exit import TrendStretchExitSub
from golden_cross_atr import GoldenCrossATRSub
from range_compressed import RangeCompressedSub
from mfi14_hyst import MFI14HystSub

# ---------------------------------------------------------------------------
# Cash Reserve Sub-Algo — holds 100% BIL, gets weight-based share like any
# other sub-algo. Rebalanced yearly alongside the rest.
# ---------------------------------------------------------------------------

class CashReserveSub(BaseSubAlgo):
    """Always 100% BIL. Use weight to set the cash reserve fraction."""

    def initialize(self):
        self.bil = self.algo.AddEquity("BIL", Resolution.Daily).Symbol
        self.targets = {self.bil: 1.0}

    def update_targets(self):
        return False


# ---------------------------------------------------------------------------
# Combined Ensemble Algo
# ---------------------------------------------------------------------------

class UltimateAlgo(QCAlgorithm):
    MONTHLY_OPEN_MIN  = 40    # minutes after open for monthly log
    CASH_TICKER       = "BIL"
    BIL_MIN_REMAINING = 0.01  # only route idle cash to BIL above this weight
    REBAL_DRIFT       = 0.005 # skip rebalance if drift is smaller than this

    def Initialize(self):
        self.SetStartDate(*START_DATE)
        self.SetEndDate(*END_DATE)
        self.SetCash(INITIAL_CASH)

        self.bil         = self.AddEquity(self.CASH_TICKER, Resolution.Daily).Symbol
        self.last_prices = {}

        # (Sub, name, weight) — weight controls capital share & annual rebalance proportion
        sub_specs = [
            (LeveragedRebalanceSub,  "LevRebal",       10),  #  1
            (IBSATRStopSub,          "IBSBasket",      20),  #  2
            (RSIThreeVoteSub,        "RSI2DipVote",    20),  #  3
            (RangeBreakoutSub,       "RangeBreak",     10),  #  4
            (SMA200RSITiersSub,      "SMA200Tiers",    10),  #  5
            (SMA150TrendSub,         "SMA150",         10),  #  6
            (SMA200PyramidSub,       "SMA200Pyramid",  10),  #  7
            (SMAFiveVoteSub,         "SMA5Vote",       15),  #  8
            (DonchianFourVoteSub,    "D4Vote",         15),  #  9
            (MomentumVoteSub,        "MomVote",        10),  # 10
            (TrendStretchExitSub,    "StretchExit",    10),  # 11
            (GoldenCrossATRSub,      "GoldXATR",       10),  # 12
            (RangeCompressedSub,     "RangeCompr",     10),  # 13
            (MFI14HystSub,           "MFI14Hyst",      10),  # 14
            (CashReserveSub,         "CashReserve",    5),   # 15
        ]
        self.sub_algos = [cls(self, name) for cls, name, _ in sub_specs]
        total_weight   = sum(w for _, _, w in sub_specs)
        for sub, (_, _, w) in zip(self.sub_algos, sub_specs):
            sub.weight              = w
            sub.equity              = INITIAL_CASH * w / total_weight
            sub.trade_count         = 0      # cumulative days where targets changed
            sub.trade_count_year    = 0      # reset on each yearly equity reset
            sub.last_trade_date     = None
            sub._prev_targets_snap  = {}     # for diff-based change detection
            sub.initialize()

        self.UniverseSettings.Resolution = Resolution.Daily
        for sub in self.sub_algos:
            universes = sub.get_universes()
            for name, func in universes.items():
                self.AddUniverse(self._wrap_universe(sub, name, func))

        self.SetWarmUp(WARMUP_DAYS, Resolution.Daily)

        # ONE CENTRAL SCHEDULER
        self.Schedule.On(
            self.DateRules.EveryDay(SCHEDULE_TICKER),
            self.TimeRules.AfterMarketOpen(SCHEDULE_TICKER, DAILY_OPEN_MIN),
            self.PerformDailyUpdate,
        )

        # Monthly: Log virtual statements
        self.Schedule.On(
            self.DateRules.MonthStart(SCHEDULE_TICKER),
            self.TimeRules.AfterMarketOpen(SCHEDULE_TICKER, self.MONTHLY_OPEN_MIN),
            self.LogVirtualStatement,
        )

    def UpdateVirtualAccounting(self):
        if self.IsWarmingUp: return

        if not self.last_prices:
            for x in self.Securities.Values:
                if x.Price > 0: self.last_prices[x.Symbol] = x.Price
            return

        for sub in self.sub_algos:
            profit_pct = 0
            for sym, weight in sub.targets.items():
                if weight == 0: continue
                price      = self.Securities[sym].Price
                last_price = self.last_prices.get(sym, price)
                asset_return = (price / last_price) - 1 if last_price > 0 else 0
                profit_pct  += weight * asset_return

            total_invested_weight = sum(sub.targets.values())
            cash_weight = max(0, 1.0 - total_invested_weight)
            bil_price   = self.Securities[self.bil].Price
            bil_last    = self.last_prices.get(self.bil, bil_price)
            bil_return  = (bil_price / bil_last) - 1 if bil_last > 0 else 0
            profit_pct += cash_weight * bil_return

            sub.equity *= (1 + profit_pct)

        for x in self.Securities.Values:
            if x.Price > 0: self.last_prices[x.Symbol] = x.Price

    def LogVirtualStatement(self):
        if self.IsWarmingUp: return
        msg     = f"--- Monthly Virtual Statement ({self.Time.strftime('%Y-%m')}) ---\n"
        total_v = sum(sub.equity for sub in self.sub_algos)
        for sub in self.sub_algos:
            share    = (sub.equity / total_v) * 100 if total_v > 0 else 0
            last_str = sub.last_trade_date.strftime('%Y-%m-%d') if sub.last_trade_date else "never"
            msg += (f"  {sub.id}: ${sub.equity:,.0f} ({share:.1f}% share) "
                    f"| trades: ytd={sub.trade_count_year} total={sub.trade_count} "
                    f"last={last_str}\n")
        msg += f"  TOTAL VIRTUAL: ${total_v:,.0f}"
        self.Log(msg)

    def _wrap_universe(self, sub, name, func):
        def wrapped(fundamental):
            selected = func(fundamental)
            sub.universe_groups[name] = set(selected)
            return selected
        return wrapped

    def PerformDailyUpdate(self):
        if self.IsWarmingUp: return

        self.UpdateVirtualAccounting()

        if not hasattr(self, "_last_year") or self.Time.year != self._last_year:
            if hasattr(self, "_last_year"):
                prev_yr = self._last_year
                rows    = [f"  {sub.id}: {sub.trade_count_year} trades"
                           + ("  <-- ZERO-TRADE WARNING" if sub.trade_count_year == 0 else "")
                           for sub in self.sub_algos]
                self.Log(f"YEARLY TRADE REPORT ({prev_yr}):\n" + "\n".join(rows))

            self._last_year = self.Time.year
            total_v    = sum(sub.equity for sub in self.sub_algos)
            total_w    = sum(sub.weight for sub in self.sub_algos)
            for sub in self.sub_algos:
                sub.equity           = total_v * sub.weight / total_w
                sub.trade_count_year = 0
            self.Log(f"YEARLY REBALANCE: total=${total_v:,.0f}, reset by weight (sum={total_w})")

        update_signaled = {}
        for sub in self.sub_algos:
            signaled = sub.update_targets()
            update_signaled[sub.id] = signaled
            if signaled:
                sub.force_rebalance = True

        for sub in self.sub_algos:
            cur          = {s: round(w, 6) for s, w in sub.targets.items() if w != 0}
            dict_changed = cur != sub._prev_targets_snap
            if dict_changed or update_signaled.get(sub.id):
                sub.trade_count       += 1
                sub.trade_count_year  += 1
                if sub.last_trade_date is None:
                    self.Log(f"FIRST TRADE: {sub.id} on {self.Time.strftime('%Y-%m-%d')}")
                sub.last_trade_date    = self.Time
            sub._prev_targets_snap = cur

        self.ExecuteAggregation()

    def OnSecuritiesChanged(self, changes):
        for sub in self.sub_algos:
            sub.on_securities_changed(changes)

    def ExecuteAggregation(self):
        total_real = self.Portfolio.TotalPortfolioValue
        if total_real <= 0: return

        total_virtual = sum(sub.equity for sub in self.sub_algos)
        if total_virtual <= 0: return

        force = any(sub.force_rebalance for sub in self.sub_algos)

        agg_weights = {}
        for sub in self.sub_algos:
            relative_share = sub.equity / total_virtual
            # Scale sub's targets down to 1.0 if they over-allocate (safety net).
            sub_target_sum = sum(sub.targets.values())
            sub_scale      = 1.0 / sub_target_sum if sub_target_sum > 1.0 else 1.0
            for sym, weight in sub.targets.items():
                agg_weights[sym] = agg_weights.get(sym, 0) + (weight * sub_scale * relative_share)

        remaining = max(0, 1.0 - sum(agg_weights.values()))
        if remaining > self.BIL_MIN_REMAINING:
            agg_weights[self.bil] = agg_weights.get(self.bil, 0) + remaining

        total_w = sum(agg_weights.values())
        if total_w > 1.0:
            self.Log(f"OVER-ALLOCATION: agg_weights sum = {total_w:.4f}, normalizing down")
            for s in agg_weights: agg_weights[s] /= total_w

        if not force and hasattr(self, "_prev_agg_weights"):
            if set(agg_weights.keys()) == set(self._prev_agg_weights.keys()):
                significant_change = False
                for sym, weight in agg_weights.items():
                    prev_w = self._prev_agg_weights[sym]
                    if abs(weight - prev_w) > self.REBAL_DRIFT:
                        significant_change = True
                        break
                if not significant_change:
                    return

        self._prev_agg_weights = agg_weights.copy()

        for sym, weight in agg_weights.items():
            cur = self.Portfolio[sym].HoldingsValue / total_real
            if abs(weight - cur) > self.REBAL_DRIFT or (weight == 0 and self.Portfolio[sym].Invested):
                self.SetHoldings(sym, weight)

        for x in self.Portfolio.Values:
            if x.Invested and x.Symbol not in agg_weights:
                self.Liquidate(x.Symbol)

        for sub in self.sub_algos:
            sub.force_rebalance = False

    def OnData(self, data):
        if self.IsWarmingUp: return

        self.UpdateVirtualAccounting()

        for sub in self.sub_algos:
            sub.on_data(data)

    def OnEndOfAlgorithm(self):
        rows = []
        for sub in self.sub_algos:
            last_str = sub.last_trade_date.strftime('%Y-%m-%d') if sub.last_trade_date else "NEVER"
            flag     = "  <-- NEVER TRADED" if sub.trade_count == 0 else ""
            rows.append(f"  {sub.id}: total trades={sub.trade_count}  last={last_str}{flag}")
        self.Log("=== FINAL TRADE ACTIVITY REPORT ===\n" + "\n".join(rows))
