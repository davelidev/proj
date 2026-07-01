from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class GoldenCrossATRSub(BaseSubAlgo):
    """Enter TQQQ on EMA(50)>EMA(200) of QQQ while QQQ 20d realized vol is low
    (annualized < VOL_MAX). Exit on crossback, vol spike, or 3xATR(14) trailing
    stop on TQQQ. Rebalanced daily 10 mins before close."""

    ATR_MULT = 3.0
    VOL_MAX  = 0.30

    def initialize(self):
        self.qqq    = self.algo.AddEquity("QQQ",  Resolution.Minute).Symbol
        self.tqqq   = self.algo.AddEquity("TQQQ", Resolution.Minute).Symbol
        self.ema50  = ExponentialMovingAverage(50)
        self.ema200 = ExponentialMovingAverage(200)
        self.atr    = AverageTrueRange(14, MovingAverageType.Wilders)
        self.trail  = 0.0

        # Warm up indicators
        history_qqq = self.algo.History[TradeBar](self.qqq, 220, Resolution.Daily)
        for bar in history_qqq:
            self.ema50.Update(bar.EndTime, bar.Close)
            self.ema200.Update(bar.EndTime, bar.Close)

        history_tqqq = self.algo.History[TradeBar](self.tqqq, 220, Resolution.Daily)
        for bar in history_tqqq:
            self.atr.Update(bar)

    def update_targets(self):
        # Get today's TQQQ TradeBar proxy first; skip the day entirely if no
        # minute data, so the QQQ EMAs and the TQQQ ATR stay in lock-step.
        bar_tqqq = self.get_daily_bar(self.tqqq)
        if bar_tqqq is None:
            return False

        # Update QQQ EMAs with today's close at 3:50 PM
        today_close_qqq = self.algo.Securities[self.qqq].Price
        self.ema50.Update(self.algo.Time, today_close_qqq)
        self.ema200.Update(self.algo.Time, today_close_qqq)
        self.atr.Update(bar_tqqq)

        if self.algo.IsWarmingUp:
            return False
        if not (self.ema50.IsReady and self.ema200.IsReady and self.atr.IsReady):
            return False

        # Vol gate: annualized 20-day realized vol of QQQ
        hist_qqq = self.algo.History(self.qqq, 21, Resolution.Daily)
        if len(hist_qqq) < 21:
            return False
        qc = list(hist_qqq['close'])
        rets = [qc[i] / qc[i - 1] - 1 for i in range(1, len(qc))]
        mean = sum(rets) / len(rets)
        var = sum((r - mean) ** 2 for r in rets) / (len(rets) - 1)
        vol = (var ** 0.5) * (252 ** 0.5)
        low_vol = vol < self.VOL_MAX

        price    = bar_tqqq.Close
        in_trend = self.ema50.Current.Value > self.ema200.Current.Value

        prev = dict(self.targets)
        if not self.targets:
            if in_trend and low_vol:
                self.targets = {self.tqqq: 1.0}
                self.trail   = price - self.ATR_MULT * self.atr.Current.Value
        else:
            # Trail ratchets up only; exit on stop, crossback, or vol spike
            new_trail = price - self.ATR_MULT * self.atr.Current.Value
            if new_trail > self.trail:
                self.trail = new_trail
            if price < self.trail or not in_trend or not low_vol:
                self.targets = {}
                self.trail   = 0.0
        return self.targets != prev


GoldenCrossATRAlgo = _make_standalone(GoldenCrossATRSub)
