from AlgorithmImports import *


# --- cc/cc_algos/ensemble/orig/base.py ---


# ---------------------------------------------------------------------------
# Shared backtest config — edit here to affect all standalone algos
# ---------------------------------------------------------------------------

START_DATE      = (2014, 1, 1)
END_DATE        = (2025, 12, 31)
INITIAL_CASH    = 100_000
WARMUP_DAYS     = 252
SCHEDULE_TICKER = "SPY"
DAILY_OPEN_MIN  = 45


# ---------------------------------------------------------------------------
# Base Sub-Algo
# ---------------------------------------------------------------------------

class BaseSubAlgo:
    HAS_UNIVERSE = False

    def __init__(self, algo, identifier):
        self.algo = algo
        self.id = identifier
        self.equity = 0.0
        self.targets = {}
        self.universe_groups = {} # Automatically populated { 'GroupName': set(Symbols) }
        self.on_change = None
        self.force_rebalance = False

    def initialize(self): pass
    def update_targets(self): pass  # subs return True iff self.targets changed
    def on_data(self, data): pass
    def on_securities_changed(self, changes): pass

    def universe_selection(self, fundamental): return []

    def get_universes(self):
        """Returns a dict of { 'name': selection_function }."""
        if self.HAS_UNIVERSE:
            return { self.id: self.universe_selection }
        return {}




# --- cc/cc_algos/ensemble/orig/leveraged_rebalance.py ---




class LeveragedRebalanceSub(BaseSubAlgo):
    def initialize(self):
        syms = ["TQQQ"]
        self.syms       = [self.algo.AddEquity(t, Resolution.Daily).Symbol for t in syms]
        self._last_year = None

    def update_targets(self):
        # Annual rebalance: always returns True on year-change so the ensemble
        # rebalances to correct positional drift, even though weights are static.
        if self.algo.Time.year == self._last_year: return False
        self._last_year = self.algo.Time.year
        self.targets = {s: 1 / len(self.syms) * .6 for s in self.syms}
        return True




# --- cc/cc_algos/ensemble/orig/rsi_champion.py ---




class RSIDipChampionSub(BaseSubAlgo):
    def initialize(self):
        self.algo.AddEquity("QQQ", Resolution.Daily)
        self.rsi2 = self.algo.RSI("QQQ", 2, MovingAverageType.Wilders, Resolution.Daily)
        self.syms = [self.algo.AddEquity(t, Resolution.Daily).Symbol for t in ["TQQQ", "SOXL", "TECL"]]

    def update_targets(self):
        if not self.rsi2.IsReady: return False

        prev = dict(self.targets)
        if self.rsi2.Current.Value < 20:
            self.targets = {s: 1 / len(self.syms) for s in self.syms}
            self.force_rebalance = True  # rebalance daily to maintain equal weight
        else:
            self.targets = {}
        return self.targets != prev




# --- cc/cc_algos/ensemble/orig/tqqq_dynamic.py ---




class TQQQDynamicSub(BaseSubAlgo):
    def initialize(self):
        self.sym    = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.rsi2   = self.algo.RSI(self.sym, 2,   MovingAverageType.Wilders, Resolution.Daily)
        self.rsi10  = self.algo.RSI(self.sym, 10, MovingAverageType.Wilders, Resolution.Daily)
        self.sma200 = self.algo.SMA(self.sym, 200, Resolution.Daily)

    def update_targets(self):
        if not (self.rsi2.IsReady and self.sma200.IsReady): return False
        price = self.algo.Securities[self.sym].Price

        prev = dict(self.targets)
        current_w = self.targets.get(self.sym, 0)

        if price > self.sma200.Current.Value:
            if self.rsi10.Current.Value > 80:
                self.targets[self.sym] = 0.2
            elif self.rsi2.Current.Value < 30:
                self.targets[self.sym] = 1.0
            elif current_w == 0:
                self.targets[self.sym] = 0.5
        else:
            self.targets = {}

        return self.targets != prev




# --- cc/cc_algos/ensemble/orig/expanding_breakout.py ---




class ExpandingBreakoutSub(BaseSubAlgo):
    def initialize(self):
        self.sym       = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq       = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.adx       = self.algo.ADX(self.qqq, 10, Resolution.Daily)
        self.sma200    = self.algo.SMA(self.qqq, 200, Resolution.Daily)
        self.atr       = self.algo.ATR(self.sym, 14, MovingAverageType.Wilders, Resolution.Daily)
        self.max_exit      = self.algo.MAX(self.sym, 20, Resolution.Daily)
        self.trailing_stop = 0

    def on_data(self, data):
        return self.update_targets()

    def update_targets(self):
        if not self.adx.IsReady or not self.sma200.IsReady or not self.max_exit.IsReady:
            return False
        price     = self.algo.Securities[self.sym].Price
        qqq_price = self.algo.Securities[self.qqq].Price
        s200      = self.sma200.Current.Value
        adx_val   = self.adx.Current.Value
        max_val   = self.max_exit.Current.Value
        # USE QQQ FOR RANGE SIGNAL
        hist = self.algo.History(self.qqq, 3, Resolution.Daily)
        if len(hist) < 3: return False
        rang = lambda x: x.high - x.low
        r2, r1 = rang(hist.iloc[-3]), rang(hist.iloc[-2])

        prev = dict(self.targets)
        if not self.targets:
            if qqq_price > s200 and r1 > r2 and adx_val > 25:
                self.targets       = {self.sym: 1.0}
                self.trailing_stop = price - 3.0 * self.atr.Current.Value
        else:
            new_stop = price - 3.0 * self.atr.Current.Value
            if new_stop > self.trailing_stop: self.trailing_stop = new_stop
            if price >= max_val or price < self.trailing_stop or qqq_price < s200:
                self.targets       = {}
                self.trailing_stop = 0
        return self.targets != prev




# --- cc/cc_algos/ensemble/orig/tqqq_sma150.py ---




class TQQQSMA150Sub(BaseSubAlgo):
    """#006 — TQQQ trend on QQQ 150d SMA."""

    def initialize(self):
        self.sym  = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.sma  = self.algo.SMA(self.qqq, 150, Resolution.Daily)

    def update_targets(self):
        if not self.sma.IsReady: return False
        prev = dict(self.targets)
        in_trend = self.algo.Securities[self.qqq].Price > self.sma.Current.Value
        if in_trend:
            self.targets[self.sym] = 1.0
        else:
            self.targets.pop(self.sym, None)
        return self.targets != prev




# --- cc/cc_algos/ensemble/orig/ibs_atr_stop.py ---




class IBSATRStopSub(BaseSubAlgo):
    """#031 — IBS extreme + ATR-based stop loss.

    Uses update_targets (scheduled at +DAILY_OPEN_MIN after market open) rather
    than on_data: the standalone factory's on_data path delivered systematically
    worse fills (30% vs 46% CAGR over 2014–2026). With Resolution.Daily,
    Securities[self.sym] at +45 min after open already reflects the previous
    trading day's complete bar, so IBS/ATR can be computed cleanly here.
    """

    def initialize(self):
        self.sym = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.atr = self.algo.ATR(self.sym, 14, MovingAverageType.Wilders, Resolution.Daily)
        self.entry_price = None

    def update_targets(self):
        if not self.atr.IsReady: return False
        bar = self.algo.Securities[self.sym]
        h, l, c = bar.High, bar.Low, bar.Close
        if h <= l: return False
        ibs = (c - l) / (h - l)
        invested = self.sym in self.targets
        atr_val = self.atr.Current.Value

        prev = dict(self.targets)

        if not invested and ibs < 0.1:
            self.targets[self.sym] = 1.0
            self.entry_price = c
        elif invested:
            stop = self.entry_price - 3.0 * atr_val if self.entry_price else 0
            if ibs > 0.9 or c < stop:
                self.targets.pop(self.sym, None)
                self.entry_price = None

        return self.targets != prev




# --- cc/cc_algos/ensemble/orig/mini_ensemble_3_8.py ---










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

