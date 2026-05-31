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




class IBSATRStopSub(BaseSubAlgo):
    """IBS extreme + ATR-based stop loss on equal-weight TQQQ/SOXL/TECL basket.

    Uses update_targets (scheduled at +DAILY_OPEN_MIN after market open) rather
    than on_data: the standalone factory's on_data path delivered systematically
    worse fills. With Resolution.Daily, Securities[syms[0]] at +45 min after open
    already reflects the previous trading day's complete bar, so IBS/ATR can be
    computed cleanly here. Signal and ATR derived from TQQQ; position spread equally
    across TQQQ, SOXL, TECL.
    """

    def initialize(self):
        self.syms = [self.algo.AddEquity(t, Resolution.Daily).Symbol for t in ["TQQQ", "SOXL", "TECL"]]
        self.atr  = self.algo.ATR(self.syms[0], 14, MovingAverageType.Wilders, Resolution.Daily)
        self.entry_price = None

    def update_targets(self):
        if not self.atr.IsReady: return False
        bar = self.algo.Securities[self.syms[0]]
        h, l, c = bar.High, bar.Low, bar.Close
        if h <= l: return False
        ibs = (c - l) / (h - l)
        invested = self.syms[0] in self.targets
        atr_val = self.atr.Current.Value

        prev = dict(self.targets)
        w = 1.0 / len(self.syms)

        if not invested and ibs < 0.1:
            self.targets = {s: w for s in self.syms}
            self.entry_price = c
        elif invested:
            stop = self.entry_price - 3.0 * atr_val if self.entry_price else 0
            if ibs > 0.9 or c < stop:
                self.targets = {}
                self.entry_price = None

        return self.targets != prev




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/003.py ---




class RSIThreeVoteSub(BaseSubAlgo):
    """Equal-weight TQQQ/SOXL/TECL basket sized by n/3 dip-depth vote: RSI(2) < 20, <25, <30."""

    THRESHOLDS = [20, 25, 30]

    def initialize(self):
        self.algo.AddEquity("QQQ", Resolution.Daily)
        self.rsi2 = self.algo.RSI("QQQ", 2, MovingAverageType.Wilders, Resolution.Daily)
        self.syms = [self.algo.AddEquity(t, Resolution.Daily).Symbol for t in ["TQQQ", "SOXL", "TECL"]]

    def update_targets(self):
        if not self.rsi2.IsReady: return False
        rsi = self.rsi2.Current.Value
        n = sum(1 for t in self.THRESHOLDS if rsi < t)
        total_weight = n / float(len(self.THRESHOLDS))
        prev = dict(self.targets)
        if total_weight > 0:
            per_sym = total_weight / len(self.syms)
            self.targets = {s: per_sym for s in self.syms}
            self.force_rebalance = True
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




class TQQQDynamicSub(BaseSubAlgo):
    """Three-tier TQQQ sizing gated by SMA(200). Above SMA: 100% on RSI(2) < 30 dip, 50% default, 20% on RSI(14) > 70 overbought. Below SMA: flat."""

    def initialize(self):
        self.sym    = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.rsi2   = self.algo.RSI(self.sym,  2, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi14  = self.algo.RSI(self.sym, 14, MovingAverageType.Wilders, Resolution.Daily)
        self.sma200 = self.algo.SMA(self.sym, 200, Resolution.Daily)

    def update_targets(self):
        if not (self.rsi14.IsReady and self.sma200.IsReady): return False
        price = self.algo.Securities[self.sym].Price

        prev = dict(self.targets)
        current_w = self.targets.get(self.sym, 0)

        if price > self.sma200.Current.Value:
            if self.rsi14.Current.Value > 70:
                self.targets[self.sym] = 0.2
            elif self.rsi2.Current.Value < 30:
                self.targets[self.sym] = 1.0
            elif current_w == 0:
                self.targets[self.sym] = 0.5
        else:
            self.targets = {}

        return self.targets != prev




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/006.py ---




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




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/007.py ---




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




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/008.py ---




class SMAFiveVoteSub(BaseSubAlgo):
    """TQQQ position = n/5 where n = # of (SMA20, SMA50, SMA100, SMA150, SMA200) that QQQ price is above."""

    PERIODS = [20, 50, 100, 150, 200]

    def initialize(self):
        self.sym  = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.smas = [self.algo.SMA(self.qqq, n, Resolution.Daily) for n in self.PERIODS]

    def update_targets(self):
        if not self.smas[-1].IsReady: return False
        prev  = dict(self.targets)
        price = self.algo.Securities[self.qqq].Price
        n     = sum(price > sma.Current.Value for sma in self.smas)
        weight = n / float(len(self.PERIODS))
        if weight > 0:
            self.targets[self.sym] = weight
        else:
            self.targets.pop(self.sym, None)
        return self.targets != prev




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/009.py ---




class DonchianFourVoteSub(BaseSubAlgo):
    """TQQQ position = n/4 where n = # of Donchian midlines (50,100,150,200) that QQQ price is above."""

    PERIODS = [50, 100, 150, 200]

    def initialize(self):
        self.sym = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.hi  = [self.algo.MAX(self.qqq, n, Resolution.Daily) for n in self.PERIODS]
        self.lo  = [self.algo.MIN(self.qqq, n, Resolution.Daily) for n in self.PERIODS]

    def update_targets(self):
        if not self.hi[-1].IsReady: return False
        prev  = dict(self.targets)
        price = self.algo.Securities[self.qqq].Price
        n = sum(
            price > (self.hi[i].Current.Value + self.lo[i].Current.Value) / 2.0
            for i in range(len(self.PERIODS))
            if self.hi[i].IsReady
        )
        weight = n / float(len(self.PERIODS))
        if weight > 0:
            self.targets[self.sym] = weight
        else:
            self.targets.pop(self.sym, None)
        return self.targets != prev




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/010.py ---




class ThreeVoteSub(BaseSubAlgo):
    """TQQQ weight = n/3 where n = bullish count among ROC(20)>0, UpDay(20)>10, TII(20)>10."""

    def initialize(self):
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol

    def update_targets(self):
        h = self.algo.History(self.qqq, 21, Resolution.Daily)
        if h.empty or len(h) < 21: return False
        c = [float(x) for x in h["close"].values]

        sig_roc = c[-1] > c[0]

        up_days = sum(1 for i in range(1, len(c)) if c[i] > c[i-1])
        sig_upday = up_days > 10

        c20 = c[-20:]
        sma = sum(c20) / 20
        tii = sum(1 for x in c20 if x > sma)
        sig_tii = tii > 10

        n = sig_roc + sig_upday + sig_tii
        weight = n / 3.0
        prev = dict(self.targets)
        if weight > 0:
            self.targets[self.tqqq] = weight
        else:
            self.targets.pop(self.tqqq, None)
        return self.targets != prev




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/011.py ---




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




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/012.py ---




class GoldenCrossATRSub(BaseSubAlgo):
    """EMA(50) > EMA(200) entry; ratcheting 3×ATR(14) trailing stop on TQQQ."""

    ATR_MULT = 3.0

    def initialize(self):
        self.qqq     = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq    = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self._ema50  = self.algo.EMA(self.qqq, 50,  Resolution.Daily)
        self._ema200 = self.algo.EMA(self.qqq, 200, Resolution.Daily)
        self._atr    = self.algo.ATR(self.tqqq, 14, MovingAverageType.Wilders, Resolution.Daily)
        self._trail  = 0.0

    def on_data(self, data):
        return self.update_targets()

    def update_targets(self):
        if not (self._ema50.IsReady and self._ema200.IsReady and self._atr.IsReady):
            return False
        tprice = self.algo.Securities[self.tqqq].Price
        bull   = self._ema50.Current.Value > self._ema200.Current.Value
        prev   = dict(self.targets)

        if not self.targets:
            if bull:
                self.targets = {self.tqqq: 1.0}
                self._trail  = tprice - self.ATR_MULT * self._atr.Current.Value
        else:
            new_trail = tprice - self.ATR_MULT * self._atr.Current.Value
            if new_trail > self._trail: self._trail = new_trail
            if tprice < self._trail or not bull:
                self.targets = {}
                self._trail  = 0.0
        return self.targets != prev




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/013.py ---




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




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/014.py ---




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
            LeveragedRebalanceSub(self,    "LevRebal"),       #  1
            IBSATRStopSub(self,            "IBSATRStop"),     #  2
            RSIThreeVoteSub(self,          "RSI3Vote"),       #  3
            ExpandingBreakoutSub(self,     "ExpandBreak"),    #  4
            TQQQDynamicSub(self,           "TQQQDyn"),        #  5
            TQQQSMA150Sub(self,            "TQQQSMA150"),     #  6
            AntiMartingaleSub(self,        "AntiMartin"),     #  7
            SMAFiveVoteSub(self,           "SMAFiveVote"),    #  8
            DonchianFourVoteSub(self,      "D4Vote"),         #  9
            ThreeVoteSub(self,             "3Vote"),          # 10
            TrendStretchExitSub(self,      "StretchExit"),    # 11
            GoldenCrossATRSub(self,        "GoldXATR"),       # 12
            RangeExpandedSub(self,         "RangeExp"),       # 13
            MFI14HystSub(self,             "MFI14Hyst"),      # 14
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

        update_signaled = {}
        for sub in self.sub_algos:
            signaled = sub.update_targets()
            update_signaled[sub.id] = signaled
            if signaled:
                sub.force_rebalance = True

        for sub in self.sub_algos:
            cur          = {s: round(w, 6) for s, w in sub.targets.items() if w != 0}
            dict_changed = cur != sub._prev_targets_snap
            if dict_changed or update_signaled.get(sub.id):
                sub.trade_count       += 1
                sub.trade_count_year  += 1
                if sub.last_trade_date is None:
                    self.Log(f"FIRST TRADE: {sub.id} on {self.Time.strftime('%Y-%m-%d')}")
                sub.last_trade_date    = self.Time
            sub._prev_targets_snap = cur

        self.ExecuteAggregation()

    def OnSecuritiesChanged(self, changes):
        for sub in self.sub_algos:
            sub.on_securities_changed(changes)

    def ExecuteAggregation(self):
        total_real = self.Portfolio.TotalPortfolioValue
        if total_real <= 0: return

        total_virtual = sum(sub.equity for sub in self.sub_algos)
        if total_virtual <= 0: return

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

        if not force and hasattr(self, "_prev_agg_weights"):
            if set(agg_weights.keys()) == set(self._prev_agg_weights.keys()):
                significant_change = False
                for sym, weight in agg_weights.items():
                    prev_w = self._prev_agg_weights[sym]
                    if abs(weight - prev_w) > self.REBAL_DRIFT:
                        significant_change = True
                        break
                if not significant_change:
                    return

        self._prev_agg_weights = agg_weights.copy()

        for sym, weight in agg_weights.items():
            cur = self.Portfolio[sym].HoldingsValue / total_real
            if abs(weight - cur) > self.REBAL_DRIFT or (weight == 0 and self.Portfolio[sym].Invested):
                self.SetHoldings(sym, weight)

        for x in self.Portfolio.Values:
            if x.Invested and x.Symbol not in agg_weights:
                self.Liquidate(x.Symbol)

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

