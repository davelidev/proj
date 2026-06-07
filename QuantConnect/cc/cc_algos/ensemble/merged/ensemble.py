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




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/001.py ---




class LeveragedRebalanceSub(BaseSubAlgo):
    """Static 60% allocation split equally across SYMBOLS. Rebalances once per year."""

    SYMBOLS = ["TQQQ"]

    def initialize(self):
        self.basket    = [self.algo.AddEquity(t, Resolution.Daily).Symbol for t in self.SYMBOLS]
        self.last_year = None

    def update_targets(self):
        if self.algo.Time.year == self.last_year:
            return False
        self.last_year = self.algo.Time.year
        weight_per_sym = 0.6 / len(self.basket)
        self.targets = {sym: weight_per_sym for sym in self.basket}
        return True




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/002.py ---




class IBSATRStopSub(BaseSubAlgo):
    """TQQQ/SOXL/TECL basket. Enter on TQQQ IBS<0.1, exit on IBS>0.9 or 3×ATR(14) stop."""

    def initialize(self):
        self.basket      = [self.algo.AddEquity(t, Resolution.Daily).Symbol for t in ["TQQQ", "SOXL", "TECL"]]
        self.atr         = self.algo.ATR(self.basket[0], 14, MovingAverageType.Wilders, Resolution.Daily)
        self.entry_price = None

    def update_targets(self):
        if not self.atr.IsReady:
            return False

        # IBS computed on TQQQ's previous-day bar (Daily resolution).
        bar = self.algo.Securities[self.basket[0]]
        if bar.High <= bar.Low:
            return False
        ibs   = (bar.Close - bar.Low) / (bar.High - bar.Low)
        close = bar.Close

        prev     = dict(self.targets)
        invested = self.basket[0] in self.targets
        weight   = 1.0 / len(self.basket)

        if not invested and ibs < 0.1:
            self.targets = {sym: weight for sym in self.basket}
            self.entry_price = close
        elif invested:
            stop_price = (self.entry_price - 3.0 * self.atr.Current.Value) if self.entry_price else 0
            if ibs > 0.9 or close < stop_price:
                self.targets = {}
                self.entry_price = None
        return self.targets != prev




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/003.py ---




class RSIThreeVoteSub(BaseSubAlgo):
    """Equal-weight TQQQ/SOXL/TECL basket; basket weight = n/3 (weighted) where n = # of RSI(2) thresholds breached (<20, <25, <30)."""

    THRESHOLDS = [20, 25, 30]

    def initialize(self):
        self.algo.AddEquity("QQQ", Resolution.Daily)
        self.rsi    = self.algo.RSI("QQQ", 2, MovingAverageType.Wilders, Resolution.Daily)
        self.basket = [self.algo.AddEquity(t, Resolution.Daily).Symbol for t in ["TQQQ", "SOXL", "TECL"]]

    def update_targets(self):
        if not self.rsi.IsReady:
            return False
        rsi_value = self.rsi.Current.Value
        n_bullish = sum(1 for thr in self.THRESHOLDS if rsi_value < thr)
        # Weighted: pure proportional n/N
        total_w   = n_bullish / float(len(self.THRESHOLDS))

        if total_w > 0:
            per_sym = total_w / len(self.basket)
            self.targets = {sym: per_sym for sym in self.basket}
        else:
            self.targets = {}




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/004.py ---




class RangeBreakoutSub(BaseSubAlgo):
    """QQQ > SMA(200) + range expanding + ADX(10) > 25 → 100% TQQQ. Exits: 3×ATR trail, 20d high, or trend break."""

    def initialize(self):
        self.tqqq    = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq     = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.adx     = self.algo.ADX(self.qqq, 10, Resolution.Daily)
        self.sma200  = self.algo.SMA(self.qqq, 200, Resolution.Daily)
        self.atr     = self.algo.ATR(self.tqqq, 14, MovingAverageType.Wilders, Resolution.Daily)
        self.hi20    = self.algo.MAX(self.tqqq, 20, Resolution.Daily)
        self.trail   = 0.0

    def on_data(self, data):
        return self.update_targets()

    def update_targets(self):
        if not (self.adx.IsReady and self.sma200.IsReady and self.hi20.IsReady):
            return False
        tqqq_price = self.algo.Securities[self.tqqq].Price
        qqq_price  = self.algo.Securities[self.qqq].Price
        sma200     = self.sma200.Current.Value
        adx        = self.adx.Current.Value
        hi20       = self.hi20.Current.Value

        # Range expansion: yesterday's QQQ range > the day before's. Skip today's
        # just-closed bar (iloc[-1]) — acts on settled prior bars only.
        hist = self.algo.History(self.qqq, 3, Resolution.Daily)
        if len(hist) < 3:
            return False
        range_of = lambda bar: bar.high - bar.low
        range_expanding = range_of(hist.iloc[-2]) > range_of(hist.iloc[-3])

        prev = dict(self.targets)
        if not self.targets:
            # Entry
            if qqq_price > sma200 and range_expanding and adx > 25:
                self.targets = {self.tqqq: 1.0}
                self.trail   = tqqq_price - 3.0 * self.atr.Current.Value
        else:
            # Trail ratchets up only
            new_trail = tqqq_price - 3.0 * self.atr.Current.Value
            if new_trail > self.trail:
                self.trail = new_trail
            # Exit on take-profit, stop, or trend break
            if tqqq_price >= hi20 or tqqq_price < self.trail or qqq_price < sma200:
                self.targets = {}
                self.trail   = 0.0
        return self.targets != prev




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/005.py ---




class SMA200RSITiersSub(BaseSubAlgo):
    """SMA(200) regime + RSI tiers. Above SMA: 100% on RSI(2)<30 dip, 20% on RSI(14)>70 overbought, else 50%. Below SMA: cash."""

    def initialize(self):
        self.tqqq   = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.rsi2   = self.algo.RSI(self.tqqq,  2, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi14  = self.algo.RSI(self.tqqq, 14, MovingAverageType.Wilders, Resolution.Daily)
        self.sma200 = self.algo.SMA(self.tqqq, 200, Resolution.Daily)

    def update_targets(self):
        if not (self.rsi14.IsReady and self.sma200.IsReady):
            return False
        price       = self.algo.Securities[self.tqqq].Price
        in_uptrend  = price > self.sma200.Current.Value
        current_w   = self.targets.get(self.tqqq, 0)

        prev = dict(self.targets)
        if in_uptrend:
            if self.rsi14.Current.Value > 70:
                self.targets[self.tqqq] = 0.2  # overbought trim
            elif self.rsi2.Current.Value < 30:
                self.targets[self.tqqq] = 1.0  # dip buy
            elif current_w == 0:
                self.targets[self.tqqq] = 0.5  # default entry
            # else: hold current weight
        else:
            self.targets = {}
        return self.targets != prev




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/006.py ---




class SMA200PyramidSub(BaseSubAlgo):
    """QQQ > SMA(200): start at 50% TQQQ, add +15% per 5% gain above entry (cap 100%). Below SMA: cash."""

    def initialize(self):
        self.qqq         = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq        = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.sma200      = self.algo.SMA("QQQ", 200, Resolution.Daily)
        self.entry_price = None
        self.current_w   = 0.0

    def update_targets(self):
        if not self.sma200.IsReady:
            return False
        price      = self.algo.Securities[self.qqq].Price
        in_uptrend = price > self.sma200.Current.Value
        prev       = dict(self.targets)

        if not in_uptrend:
            self.targets     = {}
            self.entry_price = None
            self.current_w   = 0.0
        elif not self.targets:
            # Initial entry at 50%
            self.targets     = {self.tqqq: 0.5}
            self.entry_price = price
            self.current_w   = 0.5
        else:
            # Pyramid: +15% size per 5% price gain above entry
            steps    = int((price / self.entry_price - 1) / 0.05) if self.entry_price else 0
            target_w = min(1.0, 0.5 + max(0, steps) * 0.15)
            if abs(target_w - self.current_w) > 0.05:
                self.targets = {self.tqqq: target_w}
                self.current_w = target_w
        return self.targets != prev




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/007.py ---




class SMAFiveVoteSub(BaseSubAlgo):
    """TQQQ weight = n/8 over SMA periods (20, 50, 100, 150×4, 200) — proportional to # of SMAs exceeded. SMA(150) quadrupled since it tested best individually."""

    PERIODS = [20, 50, 100, 150, 150, 150, 150, 200]

    def initialize(self):
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.smas = [self.algo.SMA(self.qqq, p, Resolution.Daily) for p in self.PERIODS]

    def update_targets(self):
        if not self.smas[-1].IsReady:
            return False
        price     = self.algo.Securities[self.qqq].Price
        n_bullish = sum(1 for sma in self.smas if price > sma.Current.Value)
        # Weighted: pure proportional n/N
        weight    = n_bullish / float(len(self.PERIODS))

        prev = dict(self.targets)
        if weight > 0:
            self.targets[self.tqqq] = weight
        else:
            self.targets.pop(self.tqqq, None)
        return self.targets != prev




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/008.py ---




class DonchianFiveVoteSub(BaseSubAlgo):
    """TQQQ weight = n/5 over Donchian midlines (50, 100, 150, 200, 250) — proportional to # of midlines exceeded."""

    PERIODS = [50, 100, 150, 200, 250]

    def initialize(self):
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.highs = [self.algo.MAX(self.qqq, p, Resolution.Daily) for p in self.PERIODS]
        self.lows  = [self.algo.MIN(self.qqq, p, Resolution.Daily) for p in self.PERIODS]

    def update_targets(self):
        if not self.highs[-1].IsReady:
            return False
        price = self.algo.Securities[self.qqq].Price
        # Midline of each Donchian channel = (period high + period low) / 2
        n_bullish = sum(
            1 for i in range(len(self.PERIODS))
            if self.highs[i].IsReady
            and price > (self.highs[i].Current.Value + self.lows[i].Current.Value) / 2.0
        )
        # Weighted: pure proportional n/N
        weight = n_bullish / float(len(self.PERIODS))

        prev = dict(self.targets)
        if weight > 0:
            self.targets[self.tqqq] = weight
        else:
            self.targets.pop(self.tqqq, None)
        return self.targets != prev




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/009.py ---




class MomentumVoteSub(BaseSubAlgo):
    """TQQQ weight = n/3 where n = bullish count among ROC(20)>0, UpDay(20)>10, TII(20)>10."""

    def initialize(self):
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol

    def update_targets(self):
        hist = self.algo.History(self.qqq, 21, Resolution.Daily)
        if hist.empty or len(hist) < 21:
            return False
        closes = [float(x) for x in hist["close"].values]

        # ROC(20): is today's close higher than 20 days ago?
        sig_roc = closes[-1] > closes[0]

        # UpDay(20): more than half of last 20 day-to-day changes positive
        up_days = sum(1 for i in range(1, len(closes)) if closes[i] > closes[i-1])
        sig_upday = up_days > 10

        # TII(20): more than half of last 20 closes above their SMA(20)
        last_20 = closes[-20:]
        sma_20  = sum(last_20) / 20
        n_above = sum(1 for c in last_20 if c > sma_20)
        sig_tii = n_above > 10

        n_bullish = sig_roc + sig_upday + sig_tii
        # Weighted: pure n/3
        weight = n_bullish / 3.0

        prev = dict(self.targets)
        if weight > 0:
            self.targets[self.tqqq] = weight
        else:
            self.targets.pop(self.tqqq, None)
        return self.targets != prev




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/010.py ---




class TrendStretchExitSub(BaseSubAlgo):
    """Enter on QQQ > SMA(200) with stretch < 5%; exit when below SMA or stretch > 20%."""

    def initialize(self):
        self.qqq    = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq   = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.sma200 = self.algo.SMA("QQQ", 200, Resolution.Daily)

    def update_targets(self):
        if not self.sma200.IsReady:
            return False
        price   = self.algo.Securities[self.qqq].Price
        sma     = self.sma200.Current.Value
        stretch = (price - sma) / sma if sma > 0 else 0

        prev     = dict(self.targets)
        invested = bool(self.targets)
        if not invested:
            # Enter only at a low-stretch entry above the trend
            if price > sma and stretch < 0.05:
                self.targets = {self.tqqq: 1.0}
        else:
            # Exit on trend break or extreme overbought stretch
            if price < sma or stretch > 0.20:
                self.targets = {}
        return self.targets != prev




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/011.py ---




class GoldenCrossATRSub(BaseSubAlgo):
    """Enter on EMA(50) > EMA(200) of QQQ. Exit on crossback or 3×ATR(14) trailing stop on TQQQ."""

    ATR_MULT = 3.0

    def initialize(self):
        self.qqq    = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq   = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.ema50  = self.algo.EMA(self.qqq, 50,  Resolution.Daily)
        self.ema200 = self.algo.EMA(self.qqq, 200, Resolution.Daily)
        self.atr    = self.algo.ATR(self.tqqq, 14, MovingAverageType.Wilders, Resolution.Daily)
        self.trail  = 0.0

    def on_data(self, data):
        return self.update_targets()

    def update_targets(self):
        if not (self.ema50.IsReady and self.ema200.IsReady and self.atr.IsReady):
            return False
        price    = self.algo.Securities[self.tqqq].Price
        in_trend = self.ema50.Current.Value > self.ema200.Current.Value

        prev = dict(self.targets)
        if not self.targets:
            if in_trend:
                self.targets = {self.tqqq: 1.0}
                self.trail   = price - self.ATR_MULT * self.atr.Current.Value
        else:
            # Trail ratchets up only
            new_trail = price - self.ATR_MULT * self.atr.Current.Value
            if new_trail > self.trail:
                self.trail = new_trail
            if price < self.trail or not in_trend:
                self.targets = {}
                self.trail   = 0.0
        return self.targets != prev




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/012.py ---




class RangeCompressedSub(BaseSubAlgo):
    """Trend (price > 200d median) AND compressed range (25d avg < 110% of 200d avg) → 100%; only one true → 50%; else cash."""

    def initialize(self):
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol

    def update_targets(self):
        hist = self.algo.History(self.qqq, 200, Resolution.Daily)
        if hist.empty or len(hist) < 200:
            return False
        closes      = [float(x) for x in hist["close"].values]
        median_200d = sorted(closes)[100]
        in_trend    = self.algo.Securities[self.qqq].Price > median_200d

        # Range = high-low for each daily bar
        ranges_25d  = [float(hist["high"].iloc[i]) - float(hist["low"].iloc[i]) for i in range(-25, 0)]
        ranges_200d = [float(hist["high"].iloc[i]) - float(hist["low"].iloc[i]) for i in range(-200, 0)]
        avg_25      = sum(ranges_25d)  / 25
        avg_200     = sum(ranges_200d) / 200
        compressed  = avg_25 < avg_200 * 1.1

        if in_trend and compressed:
            weight = 1.0
        elif in_trend or compressed:
            weight = 0.5
        else:
            weight = 0.0

        prev = dict(self.targets)
        self.targets = {self.tqqq: weight} if weight > 0 else {}
        return self.targets != prev




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/013.py ---




class MFI14HystSub(BaseSubAlgo):
    """MFI(14) hysteresis: enter at >60, exit at <40; between 40-60 hold current position."""

    def initialize(self):
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.mfi  = self.algo.MFI("QQQ", 14, Resolution.Daily)

    def update_targets(self):
        if not self.mfi.IsReady:
            return False
        mfi_value = self.mfi.Current.Value
        prev = dict(self.targets)
        if mfi_value > 60:
            self.targets = {self.tqqq: 1.0}
        elif mfi_value < 40:
            self.targets = {}
        # else: 40 ≤ MFI ≤ 60 → hold current position
        return self.targets != prev




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/014.py ---





class VolRegime20Sub(BaseSubAlgo):
    """20-day realized vol regime (20%/30% thresholds): vol<20% → 100% TQQQ, 20-30% → 50%, vol>30% → cash."""

    LOW_VOL  = 0.20
    HIGH_VOL = 0.30

    def initialize(self):
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol

    def update_targets(self):
        hist = self.algo.History(self.qqq, 21, Resolution.Daily)
        if hist.empty or len(hist) < 21:
            return False
        closes = [float(x) for x in hist["close"].values]
        rets   = [(closes[i] / closes[i-1]) - 1 for i in range(1, len(closes))]
        mean   = sum(rets) / len(rets)
        var    = sum((r - mean)**2 for r in rets) / (len(rets) - 1)
        ann_vol = math.sqrt(var) * math.sqrt(252)

        if ann_vol < self.LOW_VOL:
            weight = 1.0
        elif ann_vol < self.HIGH_VOL:
            weight = 0.5
        else:
            weight = 0.0

        prev = dict(self.targets)
        if weight > 0:
            self.targets = {self.tqqq: weight}
        else:
            self.targets = {}
        return self.targets != prev




# --- Content from /Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/utils/ultAlgo.py ---


















class CashReserveSub(BaseSubAlgo):
    """Holds 100% BIL. Weight controls the cash reserve fraction."""
    def initialize(self):
        self.bil = self.algo.AddEquity("BIL", Resolution.Daily).Symbol
        self.targets = {self.bil: 1.0}


class UltimateAlgo(QCAlgorithm):
    REBAL_DRIFT       = 0.005  # skip SetHoldings if per-symbol drift < this
    BIL_MIN_REMAINING = 0.01   # route idle capital to BIL above this fraction

    def Initialize(self):
        self.SetStartDate(*START_DATE)
        self.SetEndDate(*END_DATE)
        self.SetCash(INITIAL_CASH)
        self.bil         = self.AddEquity("BIL", Resolution.Daily).Symbol
        self.last_prices = {}
        self._last_year  = None

        sub_specs = [
            (LeveragedRebalanceSub,  "LevRebal",       10),
            (IBSATRStopSub,          "IBSBasket",      20),
            (RSIThreeVoteSub,        "RSI2DipVote",    20),
            (RangeBreakoutSub,       "RangeBreak",     10),
            (SMA200RSITiersSub,      "SMA200Tiers",    10),
            (SMA200PyramidSub,       "SMA200Pyramid",  10),
            (SMAFiveVoteSub,         "SMA5Vote",       15),
            (DonchianFiveVoteSub,    "D5Vote",         15),
            (MomentumVoteSub,        "MomVote",        10),
            (TrendStretchExitSub,    "StretchExit",    10),
            (GoldenCrossATRSub,      "GoldXATR",       10),
            (RangeCompressedSub,     "RangeCompr",     10),
            (MFI14HystSub,           "MFI14Hyst",      10),
            (VolRegime20Sub,         "VolReg20",       10),
            (CashReserveSub,         "CashReserve",     5),
        ]
        total_w = sum(w for _, _, w in sub_specs)
        self.sub_algos = []
        for cls, name, w in sub_specs:
            sub = cls(self, name)
            sub.weight             = w
            sub.equity             = INITIAL_CASH * w / total_w
            sub.active             = True   # set False permanently if equity hits 0
            sub.trade_count        = 0
            sub._prev_targets_snap = {}
            sub.initialize()
            self.sub_algos.append(sub)

        self.SetWarmUp(WARMUP_DAYS, Resolution.Daily)
        self.Schedule.On(
            self.DateRules.EveryDay(SCHEDULE_TICKER),
            self.TimeRules.AfterMarketOpen(SCHEDULE_TICKER, DAILY_OPEN_MIN),
            self.PerformDailyUpdate,
        )

    def _alive(self):
        return [s for s in self.sub_algos if s.active]

    def PerformDailyUpdate(self):
        if self.IsWarmingUp: return
        self._update_virtual_accounting()
        self._maybe_yearly_reset()
        for sub in self._alive():
            sub.update_targets()
        self._track_trade_counts()
        self._execute_aggregation()

    def _update_virtual_accounting(self):
        if not self.last_prices:
            for x in self.Securities.Values:
                if x.Price > 0: self.last_prices[x.Symbol] = x.Price
            return

        bil_price  = self.Securities[self.bil].Price
        bil_last   = self.last_prices.get(self.bil, bil_price)
        bil_return = (bil_price / bil_last) - 1 if bil_last > 0 else 0

        for sub in self._alive():
            profit = 0
            for sym, weight in sub.targets.items():
                price = self.Securities[sym].Price
                last  = self.last_prices.get(sym, price)
                if last > 0:
                    profit += weight * ((price / last) - 1)
            cash_weight = max(0, 1.0 - sum(sub.targets.values()))
            profit += cash_weight * bil_return
            sub.equity *= (1 + profit)
            if sub.equity <= 0:
                sub.active = False
                sub.targets = {}
                self.Log(f"SUB DISABLED: {sub.id} virtual equity hit zero — locked out permanently")

        for x in self.Securities.Values:
            if x.Price > 0: self.last_prices[x.Symbol] = x.Price

    def _maybe_yearly_reset(self):
        if self.Time.year == self._last_year: return
        self._last_year = self.Time.year
        alive = self._alive()
        if not alive: return
        total_v = sum(s.equity for s in alive)
        total_w = sum(s.weight for s in alive)
        for sub in alive:
            sub.equity = total_v * sub.weight / total_w
        self.Log(f"YEARLY REBALANCE: total=${total_v:,.0f} across {len(alive)} active subs")

    def _track_trade_counts(self):
        for sub in self._alive():
            cur = {s: round(w, 6) for s, w in sub.targets.items() if w != 0}
            if cur != sub._prev_targets_snap:
                sub.trade_count += 1
                sub._prev_targets_snap = cur

    def _execute_aggregation(self):
        total_real = self.Portfolio.TotalPortfolioValue
        if total_real <= 0: return
        alive = self._alive()
        total_v = sum(s.equity for s in alive)
        if total_v <= 0: return

        # Aggregate: each active sub's targets contribute proportional to its virtual share
        agg = {}
        for sub in alive:
            share = sub.equity / total_v
            for sym, w in sub.targets.items():
                agg[sym] = agg.get(sym, 0) + w * share

        # Route remaining uninvested capital to BIL
        remaining = max(0, 1.0 - sum(agg.values()))
        if remaining > self.BIL_MIN_REMAINING:
            agg[self.bil] = agg.get(self.bil, 0) + remaining

        # Execute: SetHoldings for symbols whose actual position drifted from target
        for sym, w in agg.items():
            cur = self.Portfolio[sym].HoldingsValue / total_real
            if abs(w - cur) > self.REBAL_DRIFT:
                self.SetHoldings(sym, w)

        # Liquidate any held symbol no longer in aggregated targets
        for x in self.Portfolio.Values:
            if x.Invested and x.Symbol not in agg:
                self.Liquidate(x.Symbol)

    def OnEndOfAlgorithm(self):
        for sub in self.sub_algos:
            self.SetRuntimeStatistic(f"trades_{sub.id}", str(sub.trade_count))

