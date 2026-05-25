from AlgorithmImports import *

class ExpandingBreakout(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.sym    = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq    = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.adx    = self.ADX(self.qqq,  10, Resolution.Daily)
        self.sma200 = self.SMA(self.qqq,  200, Resolution.Daily)
        self.atr    = self.ATR(self.sym,  14, MovingAverageType.Wilders, Resolution.Daily)
        self.max20  = self.MAX(self.sym,  20, Resolution.Daily)
        self.SetWarmUp(252, Resolution.Daily)
        self._stop  = 0

    def OnData(self, data):
        if self.IsWarmingUp: return
        if not (self.adx.IsReady and self.sma200.IsReady and self.max20.IsReady): return
        price = self.Securities[self.sym].Price
        qqq_p = self.Securities[self.qqq].Price
        s200  = self.sma200.Current.Value
        if not self._stop:
            hist = self.History(self.qqq, 3, Resolution.Daily)
            if len(hist) < 3: return
            r2 = hist.iloc[-3].high - hist.iloc[-3].low
            r1 = hist.iloc[-2].high - hist.iloc[-2].low
            if qqq_p > s200 and r1 > r2 and self.adx.Current.Value > 25:
                self.SetHoldings(self.sym, 1.0)
                self._stop = price - 3.0 * self.atr.Current.Value
        else:
            new_stop = price - 3.0 * self.atr.Current.Value
            if new_stop > self._stop: self._stop = new_stop
            if price >= self.max20.Current.Value or price < self._stop or qqq_p < s200:
                self.Liquidate(self.sym)
                self._stop = 0
