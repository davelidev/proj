from AlgorithmImports import *
from base import START_DATE, END_DATE, INITIAL_CASH, WARMUP_DAYS, SCHEDULE_TICKER, DAILY_OPEN_MIN, BaseSubAlgo
from vol_breakout import VolatilityBreakoutSub
from tech_dip import TechDipBuySub
from leveraged_rebalance import LeveragedRebalanceSub
from rsi_champion import RSIDipChampionSub
from tqqq_dynamic import TQQQDynamicSub
from expanding_breakout import ExpandingBreakoutSub


# ---------------------------------------------------------------------------
# Combined Ensemble Algo
# ---------------------------------------------------------------------------

class UltimateAlgo(QCAlgorithm):
    MONTHLY_OPEN_MIN  = 60    # minutes after open for monthly log
    CASH_TICKER       = "BIL"
    BIL_MIN_REMAINING = 0.01  # only route idle cash to BIL above this weight
    REBAL_DRIFT       = 0.005 # skip rebalance if drift is smaller than this

    def Initialize(self):
        self.SetStartDate(*START_DATE)
        self.SetEndDate(*END_DATE)
        self.SetCash(INITIAL_CASH)

        self.bil         = self.AddEquity(self.CASH_TICKER, Resolution.Daily).Symbol
        self.last_prices = {}

        self.sub_algos = [
            VolatilityBreakoutSub(self, "VolBreakout"),
            TechDipBuySub(self,         "TechDip"),
            LeveragedRebalanceSub(self,  "LevRebal"),
            RSIDipChampionSub(self,      "RSIDip"),
            TQQQDynamicSub(self,         "TQQQDyn"),
            ExpandingBreakoutSub(self,   "ExpandBreak"),
        ]

        start_equity = INITIAL_CASH / len(self.sub_algos)
        for sub in self.sub_algos:
            sub.equity = start_equity
            sub.initialize()

        self.UniverseSettings.Resolution = Resolution.Daily
        for sub in self.sub_algos:
            if sub.HAS_UNIVERSE:
                self.AddUniverse(sub.universe_selection)
        self.SetWarmUp(WARMUP_DAYS)

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
            share = (sub.equity / total_v) * 100 if total_v > 0 else 0
            msg  += f"  {sub.id}: ${sub.equity:,.0f} ({share:.1f}% share)\n"
        msg += f"  TOTAL VIRTUAL: ${total_v:,.0f}"
        self.Log(msg)

    def PerformDailyUpdate(self):
        if self.IsWarmingUp: return

        self.UpdateVirtualAccounting()

        if not hasattr(self, "_last_year") or self.Time.year != self._last_year:
            self._last_year = self.Time.year
            total_v   = sum(sub.equity for sub in self.sub_algos)
            reset_val = total_v / len(self.sub_algos)
            for sub in self.sub_algos: sub.equity = reset_val
            self.Log(f"YEARLY REBALANCE: All sub-algos reset to ${reset_val:,.0f}")

        for sub in self.sub_algos:
            sub.update_targets()

        self.ExecuteAggregation()

    def OnSecuritiesChanged(self, changes):
        for sub in self.sub_algos:
            sub.on_securities_changed(changes)

    def ExecuteAggregation(self):
        total_real = self.Portfolio.TotalPortfolioValue
        if total_real <= 0: return

        total_virtual = sum(sub.equity for sub in self.sub_algos)
        if total_virtual <= 0: return

        agg_weights = {}
        for sub in self.sub_algos:
            relative_share = sub.equity / total_virtual
            for sym, weight in sub.targets.items():
                agg_weights[sym] = agg_weights.get(sym, 0) + (weight * relative_share)

        remaining = max(0, 1.0 - sum(agg_weights.values()))
        if remaining > self.BIL_MIN_REMAINING:
            agg_weights[self.bil] = remaining

        total_w = sum(agg_weights.values())
        if total_w > 1.0:
            for s in agg_weights: agg_weights[s] /= total_w

        for sym, weight in agg_weights.items():
            cur = self.Portfolio[sym].HoldingsValue / total_real
            if abs(weight - cur) > self.REBAL_DRIFT or (weight == 0 and self.Portfolio[sym].Invested):
                self.SetHoldings(sym, weight)

        for x in self.Portfolio.Values:
            if x.Invested and x.Symbol not in agg_weights:
                self.Liquidate(x.Symbol)

    def OnData(self, data):
        if self.IsWarmingUp: return

        self.UpdateVirtualAccounting()

        any_changed = False
        for sub in self.sub_algos:
            if sub.on_data(data):
                any_changed = True

        if any_changed:
            self.ExecuteAggregation()
