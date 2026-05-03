from AlgorithmImports import *

# ---------------------------------------------------------------------------
# Shared backtest config — edit here to affect all standalone algos
# ---------------------------------------------------------------------------

START_DATE      = (2014, 1, 1)
END_DATE        = (2025, 12, 31)
INITIAL_CASH    = 100_000
WARMUP_DAYS     = 252
DAILY_OPEN_MIN  = 35


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
        self._prev_targets = {}
        self.universe_groups = {} # Automatically populated { 'GroupName': set(Symbols) }
        self.on_change = None

    def initialize(self): pass
    def update_targets(self): pass
    def on_data(self, data): pass
    def on_securities_changed(self, changes): pass
    
    def universe_selection(self, fundamental): return []

    def get_universes(self):
        """Returns a dict of { 'name': selection_function }."""
        if self.HAS_UNIVERSE:
            return { self.id: self.universe_selection }
        return {}

    def has_changed(self) -> bool:
        """Centralized check to see if target allocations have shifted."""
        if self.targets != self._prev_targets:
            self._prev_targets = self.targets.copy()
            return True
        return False


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
            self._sub.update_targets()
            if self._sub.has_changed():
                self._execute()

        def OnData(self, data):
            if uses_on_data:
                self._sub.on_data(data)
                if self._sub.has_changed():
                    self._execute()

        def OnSecuritiesChanged(self, changes):
            self._sub.on_securities_changed(changes)

        def _execute(self):
            for sym, w in self._sub.targets.items():
                self.SetHoldings(sym, w)
            for x in self.Portfolio.Values:
                if x.Invested and x.Symbol not in self._sub.targets:
                    self.Liquidate(x.Symbol)

    Algo.__name__     = sub_cls.__name__.replace("Sub", "Algo")
    Algo.__qualname__ = Algo.__name__
    return Algo
