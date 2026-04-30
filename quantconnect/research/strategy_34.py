from datetime import datetime, timedelta
from AlgorithmImports import *

class TQQQExpandingHighExit(QCAlgorithm):
    """
    Strategy 34: Expanding High Exit

Core Concept:
- Classic Expanding Breakout logic but with a fixed profit target.
- Exits positions when price hits a 20-day high instead of using a trailing stop.
- Designed to lock in gains faster in choppy markets.
    """
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.SetBenchmark("QQQ")
        
        self.sym = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        
        self.adx = self.ADX(self.qqq, 10, Resolution.Daily)
        self.sma200 = self.SMA(self.qqq, 200, Resolution.Daily)
        self.atr = self.ATR(self.sym, 14, MovingAverageType.Wilders, Resolution.Daily)
        self.max_exit = self.MAX(self.sym, 20, Resolution.Daily)
        
        self.SetWarmUp(200, Resolution.Daily)
        self.trailing_stop = 0

    def OnData(self, data):
        if self.IsWarmingUp or not self.adx.IsReady or not self.sma200.IsReady or not self.max_exit.IsReady:
            return

        price = self.Securities[self.sym].Price
        qqq_price = self.Securities[self.qqq].Price
        s200 = self.sma200.Current.Value
        adx_val = self.adx.Current.Value
        max_val = self.max_exit.Current.Value
        
        hist = self.History(self.sym, 3, Resolution.Daily)
        if len(hist) < 3: return
        
        r2 = hist.iloc[-3].high - hist.iloc[-3].low
        r1 = hist.iloc[-2].high - hist.iloc[-2].low
        
        if not self.Portfolio.Invested:
            if qqq_price > s200 and r1 > r2 and adx_val > 25:
                self.SetHoldings(self.sym, 1.0)
                self.trailing_stop = price - (3.0 * self.atr.Current.Value)
        else:
            new_stop = price - (3.0 * self.atr.Current.Value)
            if new_stop > self.trailing_stop:
                self.trailing_stop = new_stop
                
            if price >= max_val or price < self.trailing_stop or qqq_price < s200:
                self.Liquidate(self.sym)
