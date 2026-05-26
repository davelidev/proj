from AlgorithmImports import *


# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/utils/base.py ---


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




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/001.py ---




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




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/002.py ---




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




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/003.py ---




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




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/004.py ---




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




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/005.py ---




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




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/006.py ---




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




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/007.py ---




class CMO20Sub(BaseSubAlgo):
    def initialize(self):
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol

    def update_targets(self):
        h = self.algo.History(self.qqq, 21, Resolution.Daily)
        if h.empty or len(h) < 21: return False
        c = [float(x) for x in h["close"].values]
        changes = [c[i] - c[i-1] for i in range(1, len(c))]
        up  = sum(x for x in changes if x > 0)
        dn  = sum(-x for x in changes if x < 0)
        tot = up + dn
        cmo = 0 if tot == 0 else 100 * (up - dn) / tot
        prev = dict(self.targets)
        self.targets = {self.tqqq: 1.0} if cmo > 0 else {}
        return self.targets != prev




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/008.py ---




class ROC20Sub(BaseSubAlgo):
    def initialize(self):
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self._roc = self.algo.ROC("QQQ", 20, Resolution.Daily)

    def update_targets(self):
        if not self._roc.IsReady: return False
        prev = dict(self.targets)
        self.targets = {self.tqqq: 1.0} if self._roc.Current.Value > 0 else {}
        return self.targets != prev




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/009.py ---




class UpDay20Sub(BaseSubAlgo):
    def initialize(self):
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol

    def update_targets(self):
        h = self.algo.History(self.qqq, 21, Resolution.Daily)
        if h.empty or len(h) < 21: return False
        c = [float(x) for x in h["close"].values]
        up_days = sum(1 for i in range(1, len(c)) if c[i] > c[i-1])
        prev = dict(self.targets)
        self.targets = {self.tqqq: 1.0} if up_days > 10 else {}
        return self.targets != prev




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/010.py ---




class TII20Sub(BaseSubAlgo):
    def initialize(self):
        self.qqq   = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq  = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self._sma  = self.algo.SMA("QQQ", 20, Resolution.Daily)
        self._wins = RollingWindow[float](20)

    def update_targets(self):
        if not self._sma.IsReady or not self._wins.IsReady: return False
        sma = self._sma.Current.Value
        tii = sum(1 for i in range(20) if self._wins[i] > sma)
        prev = dict(self.targets)
        self.targets = {self.tqqq: 1.0} if tii > 10 else {}
        return self.targets != prev

    def on_data(self, data):
        if data.Bars.ContainsKey(self.qqq):
            self._wins.Add(data.Bars[self.qqq].Close)




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/011.py ---




class Price126DSub(BaseSubAlgo):
    def initialize(self):
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol

    def update_targets(self):
        h = self.algo.History(self.qqq, 126, Resolution.Daily)
        if h.empty or len(h) < 126: return False
        closes = [float(x) for x in h["close"].values]
        lo, hi = min(closes), max(closes)
        if hi == lo: return False
        pct = (closes[-1] - lo) / (hi - lo)
        prev = dict(self.targets)
        self.targets = {self.tqqq: 1.0} if pct > 0.5 else {}
        return self.targets != prev




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/012.py ---




class TrendStretchExitSub(BaseSubAlgo):
    """QQQ > SMA(200) AND stretch < 5% entry; exit on SMA breach or stretch > 20%."""
    def initialize(self):
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self._sma = self.algo.SMA("QQQ", 200, Resolution.Daily)

    def update_targets(self):
        if not self._sma.IsReady: return False
        price   = self.algo.Securities[self.qqq].Price
        sma_val = self._sma.Current.Value
        stretch = (price - sma_val) / sma_val if sma_val > 0 else 0
        prev     = dict(self.targets)
        invested = bool(self.targets)
        if not invested:
            if price > sma_val and stretch < 0.05:
                self.targets = {self.tqqq: 1.0}
        else:
            if price < sma_val or stretch > 0.20:
                self.targets = {}
        return self.targets != prev




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/013.py ---




class AntiMartingaleSub(BaseSubAlgo):
    """QQQ > SMA(200) → 50% TQQQ; pyramid +15% per 5% gain above entry, cap 100%."""
    def initialize(self):
        self.qqq       = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq      = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self._sma      = self.algo.SMA("QQQ", 200, Resolution.Daily)
        self._entry_px = None
        self._cur_w    = 0.0

    def update_targets(self):
        if not self._sma.IsReady: return False
        price = self.algo.Securities[self.qqq].Price
        bull  = price > self._sma.Current.Value
        prev  = dict(self.targets)
        if not bull:
            self.targets   = {}
            self._entry_px = None
            self._cur_w    = 0.0
        elif not self.targets:
            self.targets   = {self.tqqq: 0.5}
            self._entry_px = price
            self._cur_w    = 0.5
        else:
            steps  = (price / self._entry_px - 1) / 0.05 if self._entry_px else 0
            target = min(1.0, 0.5 + max(0, int(steps)) * 0.15)
            if abs(target - self._cur_w) > 0.05:
                self.targets = {self.tqqq: target}
                self._cur_w  = target
        return self.targets != prev




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/014.py ---




class Donchian200MidlineSub(BaseSubAlgo):
    """QQQ > midpoint of 200-day Donchian channel → 100% TQQQ; else cash."""
    def initialize(self):
        self.qqq    = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq   = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self._hi200 = self.algo.MAX("QQQ", 200, Resolution.Daily)
        self._lo200 = self.algo.MIN("QQQ", 200, Resolution.Daily)

    def update_targets(self):
        if not (self._hi200.IsReady and self._lo200.IsReady): return False
        price   = self.algo.Securities[self.qqq].Price
        midline = (self._hi200.Current.Value + self._lo200.Current.Value) / 2.0
        prev    = dict(self.targets)
        self.targets = {self.tqqq: 1.0} if price > midline else {}
        return self.targets != prev




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/015.py ---




class ROCD200TrailSub(BaseSubAlgo):
    """ROC(20)>0 AND QQQ > D200 midline AND within 7% of 20d high → 100% TQQQ."""
    def initialize(self):
        self.qqq    = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq   = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self._roc   = self.algo.ROC("QQQ", 20,  Resolution.Daily)
        self._hi200 = self.algo.MAX("QQQ", 200, Resolution.Daily)
        self._lo200 = self.algo.MIN("QQQ", 200, Resolution.Daily)
        self._hi20  = self.algo.MAX("QQQ", 20,  Resolution.Daily)

    def update_targets(self):
        if not (self._roc.IsReady and self._hi200.IsReady
                and self._lo200.IsReady and self._hi20.IsReady):
            return False
        price = self.algo.Securities[self.qqq].Price
        mid   = (self._hi200.Current.Value + self._lo200.Current.Value) / 2.0
        dd_20 = price / self._hi20.Current.Value - 1.0
        bull  = self._roc.Current.Value > 0 and price > mid
        prev  = dict(self.targets)
        self.targets = {self.tqqq: 1.0} if (bull and dd_20 > -0.07) else {}
        return self.targets != prev




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/016.py ---




class TQQQPyramidSub(BaseSubAlgo):
    """Bull: +10% TQQQ per day up to 100%; bear signal → 0% immediately."""
    def initialize(self):
        self.qqq      = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq     = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self._roc     = self.algo.ROC("QQQ", 20,  Resolution.Daily)
        self._hi200   = self.algo.MAX("QQQ", 200, Resolution.Daily)
        self._lo200   = self.algo.MIN("QQQ", 200, Resolution.Daily)
        self._exposure = 0.0

    def update_targets(self):
        if not (self._roc.IsReady and self._hi200.IsReady and self._lo200.IsReady):
            return False
        mid     = (self._hi200.Current.Value + self._lo200.Current.Value) / 2.0
        bull    = self._roc.Current.Value > 0 and self.algo.Securities[self.qqq].Price > mid
        new_exp = min(1.0, self._exposure + 0.1) if bull else 0.0
        prev    = dict(self.targets)
        if abs(new_exp - self._exposure) > 0.005:
            self._exposure = new_exp
            self.targets   = {self.tqqq: new_exp} if new_exp > 0 else {}
        return self.targets != prev




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/017.py ---




class RangeExpandedSub(BaseSubAlgo):
    """Trend (price > 200d median) + range compressed (<110% avg) → 100%; mixed → 50%; else cash."""
    def initialize(self):
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol

    def update_targets(self):
        h = self.algo.History(self.qqq, 200, Resolution.Daily)
        if h.empty or len(h) < 200: return False
        closes    = [float(x) for x in h["close"].values]
        med       = sorted(closes)[100]
        in_trend  = self.algo.Securities[self.qqq].Price > med
        recent_r  = [float(h["high"].iloc[i]) - float(h["low"].iloc[i]) for i in range(-25, 0)]
        all_r     = [float(h["high"].iloc[i]) - float(h["low"].iloc[i]) for i in range(-200, 0)]
        compressed = (sum(recent_r) / 25) < (sum(all_r) / 200) * 1.1
        if in_trend and compressed:
            wt = 1.0
        elif in_trend or compressed:
            wt = 0.5
        else:
            wt = 0.0
        prev         = dict(self.targets)
        self.targets = {self.tqqq: wt} if wt > 0 else {}
        return self.targets != prev




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/018.py ---




class MFI14HystSub(BaseSubAlgo):
    """MFI(14) > 60 → 100% TQQQ; MFI < 40 → cash; 40–60 hold (hysteresis)."""
    def initialize(self):
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self._mfi = self.algo.MFI("QQQ", 14, Resolution.Daily)

    def update_targets(self):
        if not self._mfi.IsReady: return False
        v    = self._mfi.Current.Value
        prev = dict(self.targets)
        if v > 60:
            self.targets = {self.tqqq: 1.0}
        elif v < 40:
            self.targets = {}
        return self.targets != prev




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/utils/ultAlgo.py ---





















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

        self.sub_algos = [
            LeveragedRebalanceSub(self,   "LevRebal"),
            RSIDipChampionSub(self,       "RSIDip"),
            TQQQDynamicSub(self,           "TQQQDyn"),
            ExpandingBreakoutSub(self,     "ExpandBreak"),
            TQQQSMA150Sub(self,            "TQQQSMA150"),
            IBSATRStopSub(self,            "IBSATRStop"),
            ROC20Sub(self,                 "ROC20"),
            UpDay20Sub(self,               "UpDay20"),
            TII20Sub(self,                 "TII20"),
            Price126DSub(self,             "Price126D"),
            TrendStretchExitSub(self,      "StretchExit"),
            AntiMartingaleSub(self,        "AntiMartin"),
            Donchian200MidlineSub(self,    "D200Mid"),
            ROCD200TrailSub(self,          "ROCD200Trail"),
            TQQQPyramidSub(self,           "TQQQPyramid"),
            RangeExpandedSub(self,         "RangeExp"),
            MFI14HystSub(self,             "MFI14Hyst"),
        ]

        start_equity = INITIAL_CASH / len(self.sub_algos)
        for sub in self.sub_algos:
            sub.equity              = start_equity
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
            # Report previous-year trade activity before resetting the counters.
            if hasattr(self, "_last_year"):
                prev_yr = self._last_year
                rows    = [f"  {sub.id}: {sub.trade_count_year} trades"
                           + ("  <-- ZERO-TRADE WARNING" if sub.trade_count_year == 0 else "")
                           for sub in self.sub_algos]
                self.Log(f"YEARLY TRADE REPORT ({prev_yr}):\n" + "\n".join(rows))

            self._last_year = self.Time.year
            total_v   = sum(sub.equity for sub in self.sub_algos)
            reset_val = total_v / len(self.sub_algos)
            for sub in self.sub_algos:
                sub.equity           = reset_val
                sub.trade_count_year = 0
            self.Log(f"YEARLY REBALANCE: All sub-algos reset to ${reset_val:,.0f}")

        # Each sub's update_targets returns True iff self.targets changed.
        # Subs that need a rebalance even without a target change set
        # self.force_rebalance themselves. ExecuteAggregation always runs and
        # uses its own drift gate to skip cheap days; the drift-detection is
        # an alpha source (vol harvesting across cash-heavy vs risk-heavy subs).
        update_signaled = {}
        for sub in self.sub_algos:
            signaled = sub.update_targets()
            update_signaled[sub.id] = signaled
            if signaled:
                sub.force_rebalance = True

        # Trade-activity tally — a "trade-day" is recorded if EITHER:
        #   (a) update_targets() returned True (catches no-weight-change re-asserts
        #       like LevRebal's annual rebalance flag), OR
        #   (b) targets dict differs from yesterday's snapshot (catches subs that
        #       mutate self.targets from on_data, e.g. IBSATRStop).
        for sub in self.sub_algos:
            cur          = {s: round(w, 6) for s, w in sub.targets.items() if w != 0}
            dict_changed = cur != sub._prev_targets_snap
            if dict_changed or update_signaled.get(sub.id):
                sub.trade_count       += 1
                sub.trade_count_year  += 1
                if sub.last_trade_date is None:
                    self.Log(f"FIRST TRADE: {sub.id} on {self.Time.strftime('%Y-%m-%d')}")
                sub.last_trade_date    = self.Time
            sub._prev_targets_snap = cur  # always refresh so the next diff is current

        self.ExecuteAggregation()

    def OnSecuritiesChanged(self, changes):
        for sub in self.sub_algos:
            sub.on_securities_changed(changes)

    def ExecuteAggregation(self):
        total_real = self.Portfolio.TotalPortfolioValue
        if total_real <= 0: return

        total_virtual = sum(sub.equity for sub in self.sub_algos)
        if total_virtual <= 0: return

        # Check if any sub-algo is forcing a rebalance
        force = any(sub.force_rebalance for sub in self.sub_algos)

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

        # [Change Detection] Compare with previous aggregate weights
        if not force and hasattr(self, "_prev_agg_weights"):
            # Check if all keys match and weights are within tolerance
            if set(agg_weights.keys()) == set(self._prev_agg_weights.keys()):
                significant_change = False
                for sym, weight in agg_weights.items():
                    prev_w = self._prev_agg_weights[sym]
                    if abs(weight - prev_w) > self.REBAL_DRIFT:
                        significant_change = True
                        break
                if not significant_change:
                    return # Skip execution

        self._prev_agg_weights = agg_weights.copy()

        for sym, weight in agg_weights.items():
            cur = self.Portfolio[sym].HoldingsValue / total_real
            if abs(weight - cur) > self.REBAL_DRIFT or (weight == 0 and self.Portfolio[sym].Invested):
                self.SetHoldings(sym, weight)

        for x in self.Portfolio.Values:
            if x.Invested and x.Symbol not in agg_weights:
                self.Liquidate(x.Symbol)

        # Reset force flags
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

