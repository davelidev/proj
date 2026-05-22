from AlgorithmImports import *
from datetime import datetime


class Algo059(QCAlgorithm):
    """#059 — 4-state TQQQ/SOXL/UVIX rotation: 3-of-4 SMA(202) vote; RSI(15) > 72 → UVIX; RSI(8) bear bounce → SOXL; else cash."""

    UVIX_LIVE = datetime(2022, 3, 30)

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        res = Resolution.Daily
        self._spy  = self.AddEquity("SPY",  res).Symbol
        self._qqq  = self.AddEquity("QQQ",  res).Symbol
        self._smh  = self.AddEquity("SMH",  res).Symbol
        self._tqqq = self.AddEquity("TQQQ", res).Symbol
        self._soxl = self.AddEquity("SOXL", res).Symbol
        self._uvix = self.AddEquity("UVIX", res).Symbol
        self._uvxy = self.AddEquity("UVXY", res).Symbol

        self._spy_sma  = self.SMA(self._spy,  202, res)
        self._qqq_sma  = self.SMA(self._qqq,  202, res)
        self._smh_sma  = self.SMA(self._smh,  202, res)
        self._soxl_sma = self.SMA(self._soxl, 202, res)

        self._rsi_qqq8 = self.RSI(self._qqq, 8,  MovingAverageType.Wilders, res)
        self._rsi_smh8 = self.RSI(self._smh, 8,  MovingAverageType.Wilders, res)
        self._rsi_spy15  = self.RSI(self._spy,  15, MovingAverageType.Wilders, res)
        self._rsi_qqq15  = self.RSI(self._qqq,  15, MovingAverageType.Wilders, res)
        self._rsi_smh15  = self.RSI(self._smh,  15, MovingAverageType.Wilders, res)
        self._rsi_soxl15 = self.RSI(self._soxl, 15, MovingAverageType.Wilders, res)

        self.SetWarmUp(215, res)
        self._position = "INIT"

        self.Schedule.On(
            self.DateRules.EveryDay(self._spy),
            self.TimeRules.BeforeMarketClose(self._spy, 15),
            self._rebalance,
        )

    @property
    def _ready(self):
        return (not self.IsWarmingUp
                and self._spy_sma.IsReady and self._qqq_sma.IsReady
                and self._smh_sma.IsReady and self._soxl_sma.IsReady
                and self._rsi_qqq8.IsReady and self._rsi_smh8.IsReady
                and self._rsi_spy15.IsReady and self._rsi_qqq15.IsReady
                and self._rsi_smh15.IsReady and self._rsi_soxl15.IsReady)

    def _vol_etf(self):
        try:
            if (self.Time >= self.UVIX_LIVE
                    and self.Securities[self._uvix].HasData
                    and self.Securities[self._uvix].Price > 0):
                return self._uvix
        except Exception:
            pass
        return self._uvxy

    def _apply(self, weights):
        targets = set(weights)
        for h in self.Portfolio.Values:
            if h.Invested and h.Symbol not in targets:
                self.Liquidate(h.Symbol)
        for sym, w in weights.items():
            self.SetHoldings(sym, w)

    def _rebalance(self):
        if not self._ready: return

        votes = sum([
            self.Securities[self._spy].Price  > self._spy_sma.Current.Value,
            self.Securities[self._qqq].Price  > self._qqq_sma.Current.Value,
            self.Securities[self._smh].Price  > self._smh_sma.Current.Value,
            self.Securities[self._soxl].Price > self._soxl_sma.Current.Value,
        ])
        bull = votes >= 3

        overbought = (self._rsi_spy15.Current.Value  > 72 or
                      self._rsi_qqq15.Current.Value  > 72 or
                      self._rsi_smh15.Current.Value  > 72 or
                      self._rsi_soxl15.Current.Value > 72)

        if bull:
            if overbought:
                vol = self._vol_etf()
                weights = {vol: 1.0}
            else:
                weights = {self._tqqq: 0.5, self._soxl: 0.5}
        else:
            if self._rsi_qqq8.Current.Value < 29 or self._rsi_smh8.Current.Value < 31:
                weights = {self._soxl: 1.0}
            else:
                weights = {}

        self._apply(weights)

    def OnData(self, data): pass
