from AlgorithmImports import *
from base import START_DATE, END_DATE, INITIAL_CASH, WARMUP_DAYS, SCHEDULE_TICKER, DAILY_OPEN_MIN, BaseSubAlgo
from leveraged_rebalance import LeveragedRebalanceSub
from rsi_champion import RSIDipChampionSub
from tqqq_dynamic import TQQQDynamicSub
from expanding_breakout import ExpandingBreakoutSub
from tqqq_sma150 import TQQQSMA150Sub
from ibs_atr_stop import IBSATRStopSub


class MiniEnsemble38(QCAlgorithm):
    """Ensemble of cc000_003–cc000_008: LevRebal, RSIDip, TQQQDyn, ExpandBreak, TQQQSMA150, IBSATRStop."""
    REBAL_DRIFT = 0.005

    def Initialize(self):
        self.SetStartDate(*START_DATE)
        self.SetEndDate(*END_DATE)
        self.SetCash(INITIAL_CASH)

        self.sub_algos = [
            LeveragedRebalanceSub(self,  "LevRebal"),
            RSIDipChampionSub(self,      "RSIDip"),
            TQQQDynamicSub(self,         "TQQQDyn"),
            ExpandingBreakoutSub(self,   "ExpandBreak"),
            TQQQSMA150Sub(self,          "TQQQSMA150"),
            IBSATRStopSub(self,          "IBSATRStop"),
        ]

        start_equity = INITIAL_CASH / len(self.sub_algos)
        for sub in self.sub_algos:
            sub.equity     = start_equity
            sub.initialize()

        self.UniverseSettings.Resolution = Resolution.Daily
        for sub in self.sub_algos:
            for name, func in sub.get_universes().items():
                self.AddUniverse(self._wrap_universe(sub, name, func))

        self.SetWarmUp(WARMUP_DAYS, Resolution.Daily)
        self.Schedule.On(
            self.DateRules.EveryDay(SCHEDULE_TICKER),
            self.TimeRules.AfterMarketOpen(SCHEDULE_TICKER, DAILY_OPEN_MIN),
            self._daily_update,
        )

    def _wrap_universe(self, sub, name, func):
        def wrapped(fundamental):
            selected = func(fundamental)
            sub.universe_groups[name] = set(selected)
            return selected
        return wrapped

    def _daily_update(self):
        if self.IsWarmingUp: return
        for sub in self.sub_algos:
            if sub.update_targets():
                sub.force_rebalance = True
        self._execute()

    def OnSecuritiesChanged(self, changes):
        for sub in self.sub_algos:
            sub.on_securities_changed(changes)

    def OnData(self, data):
        if self.IsWarmingUp: return
        for sub in self.sub_algos:
            sub.on_data(data)

    def _execute(self):
        total_real    = self.Portfolio.TotalPortfolioValue
        total_virtual = sum(sub.equity for sub in self.sub_algos)
        if total_real <= 0 or total_virtual <= 0: return

        force = any(sub.force_rebalance for sub in self.sub_algos)

        agg = {}
        for sub in self.sub_algos:
            share = sub.equity / total_virtual
            for sym, w in sub.targets.items():
                agg[sym] = agg.get(sym, 0) + w * share

        total_w = sum(agg.values())
        if total_w > 1.0:
            for s in agg: agg[s] /= total_w

        if not force and hasattr(self, "_prev_agg"):
            if set(agg) == set(self._prev_agg) and all(
                abs(agg[s] - self._prev_agg[s]) <= self.REBAL_DRIFT for s in agg
            ):
                return

        self._prev_agg = agg.copy()

        for sym, w in agg.items():
            cur = self.Portfolio[sym].HoldingsValue / total_real
            if abs(w - cur) > self.REBAL_DRIFT or (w == 0 and self.Portfolio[sym].Invested):
                self.SetHoldings(sym, w)

        for x in self.Portfolio.Values:
            if x.Invested and x.Symbol not in agg:
                self.Liquidate(x.Symbol)

        for sub in self.sub_algos:
            sub.force_rebalance = False
