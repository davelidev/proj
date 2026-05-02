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


# --- Content from strategies/algos/vol_breakout.py ---




class AverageIntraBarVolatility(PythonIndicator):
    def __init__(self, period):
        super().__init__()
        self.sma = SimpleMovingAverage(period)

    def Update(self, input):
        if not hasattr(input, "Open") or input.Open == 0: return False
        self.sma.Update(input.EndTime, abs((input.Open - input.Close) / input.Open) * 100)
        self.Current.Value = self.sma.Current.Value
        return self.sma.IsReady

    @property
    def Value(self): return self.Current.Value


class VolatilityBreakoutSub(BaseSubAlgo):
    def initialize(self):
        self.sym        = self.algo.AddEquity("TQQQ", Resolution.Minute).Symbol
        self.volatility = AverageIntraBarVolatility(240)
        self.algo.RegisterIndicator(self.sym, self.volatility, Resolution.Minute)
        self.high        = self.algo.MAX(self.sym, 240, Resolution.Minute)
        self.entry_price = 0

    def on_data(self, data) -> bool:
        return self.update_targets()

    def update_targets(self) -> bool:
        if self.algo.IsWarmingUp or self.algo.Time.hour < 10: return False
        price    = self.algo.Securities[self.sym].Price
        invested = self.targets.get(self.sym, 0) > 0
        changed  = False
        if not invested:
            if self.volatility.Value < 0.1 and price >= self.high.Current.Value * 0.98:
                self.entry_price = price
                self.targets     = {self.sym: 1.0}
                changed          = True
        else:
            if self.volatility.Value > 0.15 or price <= self.entry_price * 0.97:
                self.targets = {self.sym: 0}
                changed      = True
        return changed


VolatilityBreakoutAlgo = _make_standalone(VolatilityBreakoutSub)


# --- Content from strategies/algos/tech_dip.py ---




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


# --- Content from strategies/algos/leveraged_rebalance.py ---




class LeveragedRebalanceSub(BaseSubAlgo):
    def initialize(self):
        self.syms       = [self.algo.AddEquity(t, Resolution.Daily).Symbol for t in ["TQQQ", "SOXL", "TECL"]]
        self.targets    = {s: 0.20 for s in self.syms}
        self._last_year = None

    def update_targets(self) -> bool:
        if self.algo.Time.year == self._last_year: return False
        self._last_year = self.algo.Time.year
        self.targets    = {s: 0.20 for s in self.syms}
        return True


LeveragedRebalanceAlgo = _make_standalone(LeveragedRebalanceSub)


# --- Content from strategies/algos/rsi_champion.py ---




class RSIDipChampionSub(BaseSubAlgo):
    def initialize(self):
        self.algo.AddEquity("QQQ", Resolution.Daily)
        self.rsi2 = self.algo.RSI("QQQ", 2, MovingAverageType.Wilders, Resolution.Daily)
        self.syms = [self.algo.AddEquity(t, Resolution.Daily).Symbol for t in ["TQQQ", "SOXL", "TECL"]]

    def update_targets(self) -> bool:
        if not self.rsi2.IsReady: return False
        weight  = 1/3 if self.rsi2.Current.Value < 25 else 0
        changed = (self.targets.get(self.syms[0], -1) != weight)
        self.targets = {s: weight for s in self.syms}
        return changed


RSIDipChampionAlgo = _make_standalone(RSIDipChampionSub)


# --- Content from strategies/algos/tqqq_dynamic.py ---




class TQQQDynamicSub(BaseSubAlgo):
    def initialize(self):
        self.sym    = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.rsi2   = self.algo.RSI(self.sym, 2,   MovingAverageType.Wilders, Resolution.Daily)
        self.rsi10  = self.algo.RSI(self.sym, 10, MovingAverageType.Wilders, Resolution.Daily)
        self.sma200 = self.algo.SMA(self.sym, 200, Resolution.Daily)
        self.current_weight = 0

    def update_targets(self) -> bool:
        if not (self.rsi2.IsReady and self.sma200.IsReady): return False
        price = self.algo.Securities[self.sym].Price
        if price > self.sma200.Current.Value:
            if self.rsi10.Current.Value > 80:
                new_w = 0.2
            elif self.rsi2.Current.Value < 30:
                new_w = 1.0
            elif self.current_weight == 0:
                new_w = 0.5
            else:
                new_w = self.current_weight
        else:
            new_w = 0
        changed             = (self.current_weight != new_w)
        self.current_weight = new_w
        self.targets        = {self.sym: self.current_weight}
        return changed


TQQQDynamicAlgo = _make_standalone(TQQQDynamicSub)


# --- Content from strategies/algos/expanding_breakout.py ---




class ExpandingBreakoutSub(BaseSubAlgo):
    def initialize(self):
        self.sym       = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq       = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.adx       = self.algo.ADX(self.qqq, 10, Resolution.Daily)
        self.sma200    = self.algo.SMA(self.qqq, 200, Resolution.Daily)
        self.atr       = self.algo.ATR(self.sym, 14, MovingAverageType.Wilders, Resolution.Daily)
        self.max_exit      = self.algo.MAX(self.sym, 20, Resolution.Daily)
        self.trailing_stop = 0

    def on_data(self, data) -> bool:
        return self.update_targets()

    def update_targets(self) -> bool:
        if not self.adx.IsReady or not self.sma200.IsReady or not self.max_exit.IsReady:
            return False
        price     = self.algo.Securities[self.sym].Price
        qqq_price = self.algo.Securities[self.qqq].Price
        s200      = self.sma200.Current.Value
        adx_val   = self.adx.Current.Value
        max_val   = self.max_exit.Current.Value
        hist = self.algo.History(self.sym, 3, Resolution.Daily)
        if len(hist) < 3: return False
        r2 = hist.iloc[-3].high - hist.iloc[-3].low
        r1 = hist.iloc[-2].high - hist.iloc[-2].low
        if not self.targets:
            if qqq_price > s200 and r1 > r2 and adx_val > 25:
                self.targets       = {self.sym: 1.0}
                self.trailing_stop = price - 3.0 * self.atr.Current.Value
                return True
        else:
            new_stop = price - 3.0 * self.atr.Current.Value
            if new_stop > self.trailing_stop: self.trailing_stop = new_stop
            if price >= max_val or price < self.trailing_stop or qqq_price < s200:
                self.targets       = {}
                self.trailing_stop = 0
                return True
        return False


ExpandingBreakoutAlgo = _make_standalone(ExpandingBreakoutSub)


# --- Content from strategies/ultAlgo.py ---










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

