from AlgorithmImports import *
from base import START_DATE, END_DATE, INITIAL_CASH, WARMUP_DAYS, SCHEDULE_TICKER, DAILY_OPEN_MIN, BaseSubAlgo
from leveraged_rebalance import LeveragedRebalanceSub
from ibs_basket import IBSATRStopSub
from rsi2_dip_vote import RSIThreeVoteSub
from range_breakout import RangeBreakoutSub
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
    """Reserves its weight fraction as uninvested cash (holds no position)."""
    def initialize(self):
        self.targets = {}


class UltimateAlgo(QCAlgorithm):
    REBAL_DRIFT       = 0.005  # skip SetHoldings if per-symbol drift < this
    CASH_BUFFER       = 0.05   # always hold this fraction as real cash; rest of idle capital -> BIL

    def Initialize(self):
        self.SetStartDate(*START_DATE)
        self.SetEndDate(*END_DATE)
        self.SetCash(INITIAL_CASH)
        # Minute resolution so BIL orders fill at 3:50 PM with the rest of the
        # rebalance. With Daily, BIL fills one session late, stacking the new
        # leveraged-ETF leg on top of the not-yet-sold BIL → ~30% margin.
        self.bil         = self.AddEquity("BIL", Resolution.Minute).Symbol
        self.last_prices = {}
        self._last_year  = None

        sub_specs = [
            (LeveragedRebalanceSub,  "LevRebal",       10),
            (IBSATRStopSub,          "IBSBasket",      10),
            (RSIThreeVoteSub,        "RSI2DipVote",    10),
            (RangeBreakoutSub,       "RangeBreak",     10),
            (SMA200RSITiersSub,      "SMA200Tiers",    10),
            (SMA200PyramidSub,       "SMA200Pyramid",  10),
            (SMAFiveVoteSub,         "SMA5Vote",       10),
            (DonchianFiveVoteSub,    "D5Vote",         10),
            (MomentumVoteSub,        "MomVote",        10),
            (TrendStretchExitSub,    "StretchExit",    10),
            (GoldenCrossATRSub,      "GoldXATR",       10),
            (RangeCompressedSub,     "RangeCompr",     10),
            (MFI14HystSub,           "MFI14Hyst",      10),
            (VolRegime20Sub,         "VolReg20",       10),
            # CashReserve removed: cash/BIL split is now handled globally in
            # _execute_aggregation (CASH_BUFFER cash, remainder -> BIL).
        ]
        total_w = sum(w for _, _, w in sub_specs)
        self.sub_algos = []
        for cls, name, w in sub_specs:
            sub = cls(self, name)
            sub.weight             = w
            sub.equity             = INITIAL_CASH * w / total_w
            sub.active             = True   # set False permanently if equity hits 0
            sub.trade_count        = 0
            sub._prev_targets_snap = {}
            sub.initialize()
            self.sub_algos.append(sub)

        self.SetWarmUp(timedelta(days=WARMUP_DAYS), Resolution.Minute)
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
                self.Log(f"SUB DISABLED: {sub.id} virtual equity hit zero — locked out permanently")

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

        # Aggregate: each active sub's targets contribute proportional to its virtual share
        agg = {}
        for sub in alive:
            share = sub.equity / total_v
            for sym, w in sub.targets.items():
                agg[sym] = agg.get(sym, 0) + w * share

        # Always keep CASH_BUFFER as real uninvested cash; park the rest of the
        # idle capital in BIL. Deploy cap = 1 - CASH_BUFFER. If strategy targets
        # alone exceed the cap, scale them down so the cash buffer is preserved.
        cap = 1.0 - self.CASH_BUFFER
        invested = sum(agg.values())
        if invested > cap:
            scale = cap / invested
            agg = {sym: w * scale for sym, w in agg.items()}
            invested = cap
        bil_w = cap - invested
        if bil_w > 0:
            agg[self.bil] = agg.get(self.bil, 0) + bil_w

        # Execute: SetHoldings for symbols whose actual position drifted from target
        for sym, w in agg.items():
            cur = self.Portfolio[sym].HoldingsValue / total_real
            if abs(w - cur) > self.REBAL_DRIFT:
                self.SetHoldings(sym, w)

        # Liquidate any held symbol no longer in aggregated targets
        for x in self.Portfolio.Values:
            if x.Invested and x.Symbol not in agg:
                self.Liquidate(x.Symbol)

    def OnEndOfAlgorithm(self):
        for sub in self.sub_algos:
            self.SetRuntimeStatistic(f"trades_{sub.id}", str(sub.trade_count))
