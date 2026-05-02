from AlgorithmImports import *


# --- Content from strategies/base.py ---


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
        self.on_change = None

    def initialize(self): pass
    def update_targets(self) -> bool: return False
    def on_data(self, data) -> bool: return False
    def on_securities_changed(self, changes): pass
    def universe_selection(self, fundamental): return []


# ---------------------------------------------------------------------------
# Standalone mixin factory
# ---------------------------------------------------------------------------

def _make_standalone(sub_cls):
    uses_on_data = sub_cls.on_data is not BaseSubAlgo.on_data
    has_universe = sub_cls.HAS_UNIVERSE

    # QC uses Python.NET — multiple inheritance with managed classes is forbidden.
    # Use composition: Algo owns a sub instance and delegates all calls to it.
    class Algo(QCAlgorithm):
        def Initialize(self):
            self.SetStartDate(*START_DATE)
            self.SetEndDate(*END_DATE)
            self.SetCash(INITIAL_CASH)
            self._sub = sub_cls(self, sub_cls.__name__)
            self._sub.initialize()
            if has_universe:
                self.UniverseSettings.Resolution = Resolution.Daily
                self.AddUniverse(self._sub.universe_selection)
            self.SetWarmUp(WARMUP_DAYS)
            if not uses_on_data:
                self.Schedule.On(
                    self.DateRules.EveryDay("SPY"),
                    self.TimeRules.AfterMarketOpen("SPY", DAILY_OPEN_MIN),
                    self._rebalance,
                )

        def _rebalance(self):
            if self._sub.update_targets():
                self._execute()

        def OnData(self, data):
            if uses_on_data and self._sub.on_data(data):
                self._execute()

        def OnSecuritiesChanged(self, changes):
            if has_universe:
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


# --- Content from strategies/algos/tech_dip_sub.py ---




class TechDipBuySub(BaseSubAlgo):
    HAS_UNIVERSE = True

    def initialize(self):
        self.selected_syms = []
        # DISABLE orchestrator warmup to match Day 1 start of tech_dip_orig.py
        self.algo.Settings.AutomaticIndicatorWarmUp = True
        self.algo.Settings.SeedInitialPrices = True

    def universe_selection(self, fundamental):
        # Mirror LargeCapTechStrategy._select exactly
        filtered = [
            f for f in fundamental
            if (f.HasFundamentalData and
                f.AssetClassification.MorningstarSectorCode == MorningstarSectorCode.Technology)
        ]
        top5 = sorted(filtered, key=lambda f: f.MarketCap)[-5:]
        return [f.Symbol for f in top5]

    def on_securities_changed(self, changes):
        # Mirror LargeCapTechStrategy.on_securities_changed exactly
        for sec in changes.AddedSecurities:
            if sec.Symbol.Value in {"TQQQ", "QQQ", "SOXL", "TECL", "SPY", "BIL"}: continue
            
            sec.rsi   = self.algo.RSI(sec.Symbol, 2)
            sec.max   = self.algo.MAX(sec.Symbol, 252)
            sec.sma50 = self.algo.SMA(sec.Symbol, 50)
            
            # Manual Warmup (Claude's hint) to ensure parity from Day 1
            hist = self.algo.History(sec.Symbol, 252, Resolution.Daily)
            for bar in hist.itertuples():
                sec.rsi.Update(bar.Index[1], bar.close)
                sec.max.Update(bar.Index[1], bar.close)
                sec.sma50.Update(bar.Index[1], bar.close)

            if sec.Symbol not in self.selected_syms:
                self.selected_syms.append(sec.Symbol)

        for sec in changes.RemovedSecurities:
            if sec.Symbol in self.selected_syms:
                self.selected_syms.remove(sec.Symbol)
            self.targets.pop(sec.Symbol, None)
            self.algo.Liquidate(sec.Symbol)

    def update_targets(self) -> bool:
        # Check for Weekly parity (Monday)
        if self.algo.Time.weekday() != 0: return False
        
        if not self.selected_syms: return False
        
        changed = False
        # Use dynamic weight to match tech_dip_orig.py behavior
        num_selected = len(self.selected_syms)
        w_entry = 1.0 / num_selected if num_selected > 0 else 0.2
        
        for s in self.selected_syms:
            sec = self.algo.Securities[s]
            if not (hasattr(sec, "max") and sec.max.IsReady and sec.sma50.IsReady): continue
            
            if not sec.Invested:
                if sec.rsi.Current.Value < 30 and sec.Price > sec.sma50.Current.Value:
                    self.algo.Log(f"ENTRY {self.algo.Time.date()} {sec.Symbol.Value} rsi={sec.rsi.Current.Value:.1f} price={sec.Price:.2f} max={sec.max.Current.Value:.2f}")
                    self.targets[s] = w_entry
                    changed = True
            else:
                reason = "STOP" if sec.Price <= sec.Holdings.AveragePrice * 0.85 else "ATH"
                if sec.Price <= sec.Holdings.AveragePrice * 0.85 or sec.Price >= sec.max.Current.Value:
                    self.algo.Log(f"EXIT  {self.algo.Time.date()} {sec.Symbol.Value} {reason} price={sec.Price:.2f} avg={sec.Holdings.AveragePrice:.2f} max={sec.max.Current.Value:.2f}")
                    if s in self.targets:
                        del self.targets[s]
                        changed = True
                else:
                    # PRESERVE DRIFT: Set target to current weight so SetHoldings does nothing
                    # This allows winners to grow past 20%, matching the 31% CAGR of orig
                    # We only do this if it's already in targets
                    if s in self.targets:
                        current_w = sec.Holdings.Quantity * sec.Price / self.algo.Portfolio.TotalPortfolioValue
                        self.targets[s] = current_w
        
        return changed


TechDipBuyAlgo = _make_standalone(TechDipBuySub)

