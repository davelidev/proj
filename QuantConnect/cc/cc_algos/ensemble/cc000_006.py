from AlgorithmImports import *


# --- strategies/base.py ---


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


# ---------------------------------------------------------------------------
# Standalone mixin factory
# ---------------------------------------------------------------------------

def _make_standalone(sub_cls):
    uses_on_data = sub_cls.on_data is not BaseSubAlgo.on_data

    # QC uses Python.NET — multiple inheritance with managed classes is forbidden.
    # Use composition: Algo owns a sub instance and delegates all calls to it.
    class Algo(QCAlgorithm):
        def Initialize(self):
            self.SetStartDate(*START_DATE)
            self.SetEndDate(*END_DATE)
            self.SetCash(INITIAL_CASH)
            self._sub = sub_cls(self, sub_cls.__name__)
            
            # Initialize virtual equity to total cash for standalone runs
            self._sub.equity = INITIAL_CASH
            self._sub.initialize()
            
            universes = self._sub.get_universes()
            if universes:
                self.UniverseSettings.Resolution = Resolution.Daily
                for name, func in universes.items():
                    self.AddUniverse(self._wrap_selection(name, func))
                    
            self.SetWarmUp(WARMUP_DAYS)
            if not uses_on_data:
                self.Schedule.On(
                    self.DateRules.EveryDay("SPY"),
                    self.TimeRules.AfterMarketOpen("SPY", DAILY_OPEN_MIN),
                    self._rebalance,
                )

        def _wrap_selection(self, name, func):
            def wrapped(fundamental):
                selected = func(fundamental)
                self._sub.universe_groups[name] = set(selected)
                return selected
            return wrapped

        def _rebalance(self):
            if self.IsWarmingUp: return
            changed = self._sub.update_targets()
            if changed or self._sub.force_rebalance:
                self._execute()
                self._sub.force_rebalance = False

        def OnData(self, data):
            if self.IsWarmingUp: return
            
            # [Virtual Accounting] Update equity to track real growth
            if not hasattr(self, "_prev_total_value"):
                self._prev_total_value = self.Portfolio.TotalPortfolioValue
            
            curr_value = self.Portfolio.TotalPortfolioValue
            if self._prev_total_value > 0:
                change_ratio = curr_value / self._prev_total_value
                self._sub.equity *= change_ratio
            self._prev_total_value = curr_value

            if uses_on_data:
                changed = self._sub.on_data(data)
                if changed or self._sub.force_rebalance:
                    self._execute()
                    self._sub.force_rebalance = False

        def OnSecuritiesChanged(self, changes):
            self._sub.on_securities_changed(changes)

        def _execute(self):
            # [Leverage Gate] Ensure total weight does not exceed 1.0
            total_w = sum(self._sub.targets.values())
            scale = 1.0 / total_w if total_w > 1.0 else 1.0
            
            total_real = self.Portfolio.TotalPortfolioValue
            if total_real <= 0: return

            # In Standalone mode, we do NOT force cash into BIL.
            # We let the sub-algo manage its own symbols and let the rest stay as USD.
            for sym, w in self._sub.targets.items():
                target_w = w * scale
                current_w = self.Portfolio[sym].HoldingsValue / total_real
                
                # Only trade if drift > 0.5% or it is an exit (target=0)
                if abs(target_w - current_w) > 0.005 or (target_w == 0 and self.Portfolio[sym].Invested):
                    self.SetHoldings(sym, target_w)
            
            # Cleanup removed symbols
            for x in self.Portfolio.Values:
                if x.Invested and x.Symbol not in self._sub.targets:
                    self.Liquidate(x.Symbol)


    Algo.__name__     = sub_cls.__name__.replace("Sub", "Algo")
    Algo.__qualname__ = Algo.__name__
    return Algo


# --- strategies/algos/expanding_breakout.py ---




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


ExpandingBreakoutAlgo = _make_standalone(ExpandingBreakoutSub)

