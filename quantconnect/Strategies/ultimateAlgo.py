from AlgorithmImports import *


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
        self.active = False
        self.on_change = None  # set by parent; called when targets change

    def initialize(self): pass
    def update_targets(self) -> bool: return False
    def on_data(self, data) -> bool: return False
    def on_securities_changed(self, changes): pass
    def universe_selection(self, fundamental): return []

    def _fire(self):
        if self.algo.IsWarmingUp: return
        if self.update_targets() and self.on_change:
            self.on_change()


# ---------------------------------------------------------------------------
# Sub-algos
# ---------------------------------------------------------------------------

class VolatilityBreakoutSub(BaseSubAlgo):
    # Minute-level logic — evaluated in OnData
    def initialize(self):
        self.sym = self.algo.AddEquity("TQQQ", Resolution.Minute).Symbol
        self.volatility = AverageIntraBarVolatility(240)
        self.algo.RegisterIndicator(self.sym, self.volatility, Resolution.Minute)
        self.high = self.algo.MAX(self.sym, 240, Resolution.Minute)
        self.entry_price = 0

    def on_data(self, data) -> bool:
        return self.update_targets()

    def update_targets(self) -> bool:
        if self.algo.IsWarmingUp or self.algo.Time.hour < 10: return False
        price = self.algo.Securities[self.sym].Price
        changed = False
        if not self.active:
            if self.volatility.Value < 0.1 and price >= self.high.Current.Value * 0.98:
                self.active = True
                self.entry_price = price
                changed = True
        else:
            if self.volatility.Value > 0.15 or price <= self.entry_price * 0.97:
                self.active = False
                changed = True
        self.targets = {self.sym: 1.0 if self.active else 0}
        return changed


class TechDipBuySub(BaseSubAlgo):
    HAS_UNIVERSE = True

    def initialize(self):
        self.selected_syms = []
        self.targets = {}

    def universe_selection(self, fundamental):
        tech = [f for f in fundamental
                if f.AssetClassification.MorningstarSectorCode == MorningstarSectorCode.Technology]
        top5 = sorted(tech, key=lambda x: x.MarketCap, reverse=True)[:5]
        return [x.Symbol for x in top5]

    def on_securities_changed(self, changes):
        skip = {"TQQQ", "QQQ", "SOXL", "TECL", "SPY", "BIL"}
        for sec in changes.AddedSecurities:
            if sec.Symbol.Value in skip: continue
            sec.rsi = self.algo.RSI(sec.Symbol, 2)
            sec.max = self.algo.MAX(sec.Symbol, 252)
            sec.sma50 = self.algo.SMA(sec.Symbol, 50)
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
            if sec.Symbol in self.targets:
                del self.targets[sec.Symbol]

    def update_targets(self) -> bool:
        # Weekly (Mondays) - Python weekday() 0 is Monday
        if self.algo.Time.weekday() != 0: return False
        
        changed = False
        if not self.selected_syms: return False
        w = 1.0 / len(self.selected_syms)
        for s in self.selected_syms:
            sec = self.algo.Securities[s]
            if not (hasattr(sec, "rsi") and sec.rsi.IsReady): continue
            old_w = self.targets.get(s, 0)
            if old_w == 0:
                if sec.rsi.Current.Value < 30 and sec.Price > sec.sma50.Current.Value:
                    self.targets[s] = w
                    changed = True
            else:
                avg_price = sec.Holdings.AveragePrice if sec.Invested else 0
                if (avg_price > 0 and sec.Price <= avg_price * 0.85) or sec.Price >= sec.max.Current.Value:
                    self.targets[s] = 0
                    changed = True
        return changed


class LeveragedRebalanceSub(BaseSubAlgo):
    def initialize(self):
        assets = ["TQQQ", "SOXL", "TECL"]
        self.syms = [self.algo.AddEquity(t, Resolution.Daily).Symbol for t in assets]
        self.targets = {s: 0.20 for s in self.syms}
        self._last_year = None

    def update_targets(self) -> bool:
        # Yearly rebalance
        if self.algo.Time.year == self._last_year: return False
        self._last_year = self.algo.Time.year
        self.targets = {s: 0.20 for s in self.syms}
        return True


class RSIDipChampionSub(BaseSubAlgo):
    def initialize(self):
        self.algo.AddEquity("QQQ", Resolution.Daily)
        self.rsi2 = self.algo.RSI("QQQ", 2, MovingAverageType.Wilders, Resolution.Daily)
        assets = ["TQQQ", "SOXL", "TECL"]
        self.syms = [self.algo.AddEquity(t, Resolution.Daily).Symbol for t in assets]

    def update_targets(self) -> bool:
        if not self.rsi2.IsReady: return False
        weight = 0.333 if self.rsi2.Current.Value < 25 else 0
        changed = (self.targets.get(self.syms[0], -1) != weight)
        self.targets = {s: weight for s in self.syms}
        return changed


class TQQQDynamicSub(BaseSubAlgo):
    def initialize(self):
        self.sym = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.rsi2 = self.algo.RSI(self.sym, 2, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi10 = self.algo.RSI(self.sym, 10, MovingAverageType.Wilders, Resolution.Daily)
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
        changed = (self.current_weight != new_w)
        self.current_weight = new_w
        self.targets = {self.sym: self.current_weight}
        return changed


class ExpandingBreakoutSub(BaseSubAlgo):
    def initialize(self):
        self.sym = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.algo.AddEquity("QQQ", Resolution.Daily).Symbol
        self.adx = self.algo.ADX(self.qqq, 10, Resolution.Daily)
        self.sma200 = self.algo.SMA(self.qqq, 200, Resolution.Daily)
        self.atr = self.algo.ATR(self.sym, 14, MovingAverageType.Wilders, Resolution.Daily)
        self.max_exit = self.algo.MAX(self.sym, 20, Resolution.Daily)
        self.trailing_stop = 0
        self._invested = False

    def update_targets(self) -> bool:
        if not self.adx.IsReady or not self.sma200.IsReady or not self.max_exit.IsReady:
            return False
        price = self.algo.Securities[self.sym].Price
        qqq_price = self.algo.Securities[self.qqq].Price
        s200 = self.sma200.Current.Value
        adx_val = self.adx.Current.Value
        max_val = self.max_exit.Current.Value
        hist = self.algo.History(self.sym, 3, Resolution.Daily)
        if len(hist) < 3: return False
        r2 = hist.iloc[-3].high - hist.iloc[-3].low
        r1 = hist.iloc[-2].high - hist.iloc[-2].low
        if not self._invested:
            if qqq_price > s200 and r1 > r2 and adx_val > 25:
                self._invested = True
                self.targets = {self.sym: 1.0}
                self.trailing_stop = price - 3.0 * self.atr.Current.Value
                return True
        else:
            new_stop = price - 3.0 * self.atr.Current.Value
            if new_stop > self.trailing_stop: self.trailing_stop = new_stop
            if price >= max_val or price < self.trailing_stop or qqq_price < s200:
                self._invested = False
                self.targets = {}
                self.trailing_stop = 0
                return True
        return False


# ---------------------------------------------------------------------------
# Combined Ensemble Algo
# ---------------------------------------------------------------------------

class UltimateAlgo(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        self.last_prices = {}

        self.sub_algos = [
            VolatilityBreakoutSub(self, "VolBreakout"),
            TechDipBuySub(self, "TechDip"),
            LeveragedRebalanceSub(self, "LevRebal"),
            RSIDipChampionSub(self, "RSIDip"),
            TQQQDynamicSub(self, "TQQQDyn"),
            ExpandingBreakoutSub(self, "ExpandBreak"),
        ]
        
        # Initial funding
        start_equity = 100000 / len(self.sub_algos)
        for sub in self.sub_algos:
            sub.equity = start_equity
            sub.initialize()

        self.UniverseSettings.Resolution = Resolution.Daily
        for sub in self.sub_algos:
            if sub.HAS_UNIVERSE:
                self.AddUniverse(sub.universe_selection)
        self.SetWarmUp(252)

        # ONE CENTRAL SCHEDULER
        self.Schedule.On(
            self.DateRules.EveryDay("SPY"),
            self.TimeRules.AfterMarketOpen("SPY", 45),
            self.PerformDailyUpdate,
        )

        # Monthly: Log virtual statements
        self.Schedule.On(
            self.DateRules.MonthStart("SPY"),
            self.TimeRules.AfterMarketOpen("SPY", 60),
            self.LogVirtualStatement,
        )

    def UpdateVirtualAccounting(self):
        """Update each sub-algo's equity based on live price movement."""
        if self.IsWarmingUp: return

        # Capture prices if empty
        if not self.last_prices:
            for x in self.Securities.Values:
                if x.Price > 0: self.last_prices[x.Symbol] = x.Price
            return

        for sub in self.sub_algos:
            profit_pct = 0
            for sym, weight in sub.targets.items():
                if weight == 0: continue
                price = self.Securities[sym].Price
                last_price = self.last_prices.get(sym, price)
                asset_return = (price / last_price) - 1 if last_price > 0 else 0
                profit_pct += weight * asset_return
            
            # Cash portion (idle or BIL)
            total_invested_weight = sum(sub.targets.values())
            cash_weight = max(0, 1.0 - total_invested_weight)
            bil_price = self.Securities[self.bil].Price
            bil_last = self.last_prices.get(self.bil, bil_price)
            bil_return = (bil_price / bil_last) - 1 if bil_last > 0 else 0
            profit_pct += cash_weight * bil_return
            
            sub.equity *= (1 + profit_pct)

        # Sync prices for next bar
        for x in self.Securities.Values:
            if x.Price > 0: self.last_prices[x.Symbol] = x.Price

    def LogVirtualStatement(self):
        if self.IsWarmingUp: return
        msg = f"--- Monthly Virtual Statement ({self.Time.strftime('%Y-%m')}) ---\n"
        total_v = sum(sub.equity for sub in self.sub_algos)
        for sub in self.sub_algos:
            share = (sub.equity / total_v) * 100 if total_v > 0 else 0
            msg += f"  {sub.id}: ${sub.equity:,.0f} ({share:.1f}% share)\n"
        msg += f"  TOTAL VIRTUAL: ${total_v:,.0f}"
        self.Log(msg)

    def PerformDailyUpdate(self):
        if self.IsWarmingUp: return
        
        # 1. Update Virtual Accounting first
        self.UpdateVirtualAccounting()
        
        # 2. Check for Yearly Reset (First trading day of year)
        if not hasattr(self, "_last_year") or self.Time.year != self._last_year:
            self._last_year = self.Time.year
            total_v = sum(sub.equity for sub in self.sub_algos)
            reset_val = total_v / len(self.sub_algos)
            for sub in self.sub_algos: sub.equity = reset_val
            self.Log(f"YEARLY REBALANCE: All sub-algos reset to ${reset_val:,.0f}")

        # 3. Poll all Daily/Weekly/Yearly sub-algos
        # Each sub-algo handles its own internal timing (e.g. weekday checks).
        for sub in self.sub_algos:
            sub.update_targets()
        
        # 4. Always aggregate on daily event to handle equity share drift
        self.ExecuteAggregation()

    def OnSecuritiesChanged(self, changes):
        for sub in self.sub_algos:
            sub.on_securities_changed(changes)

    def ExecuteAggregation(self):
        total_real = self.Portfolio.TotalPortfolioValue
        if total_real <= 0: return
        
        # Calculate Relative Equity Share
        total_virtual = sum(sub.equity for sub in self.sub_algos)
        if total_virtual <= 0: return
        
        agg_weights = {}
        for sub in self.sub_algos:
            relative_share = sub.equity / total_virtual
            for sym, weight in sub.targets.items():
                agg_weights[sym] = agg_weights.get(sym, 0) + (weight * relative_share)
        
        # BIL hedge for remaining real-world cash
        remaining = max(0, 1.0 - sum(agg_weights.values()))
        if remaining > 0.01:
            agg_weights[self.bil] = remaining
            
        total_w = sum(agg_weights.values())
        if total_w > 1.0:
            for s in agg_weights: agg_weights[s] /= total_w
            
        for sym, weight in agg_weights.items():
            cur = self.Portfolio[sym].HoldingsValue / total_real
            if abs(weight - cur) > 0.005 or (weight == 0 and self.Portfolio[sym].Invested):
                self.SetHoldings(sym, weight)
                
        for x in self.Portfolio.Values:
            if x.Invested and x.Symbol not in agg_weights:
                self.Liquidate(x.Symbol)

    def OnData(self, data):
        if self.IsWarmingUp: return
        
        # Live virtual accounting on every data bar
        self.UpdateVirtualAccounting()
        
        # Check all sub-algos for intra-day target updates
        any_changed = False
        for sub in self.sub_algos:
            if sub.on_data(data):
                any_changed = True
        
        if any_changed:
            self.ExecuteAggregation()
