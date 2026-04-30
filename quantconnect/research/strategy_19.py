from datetime import datetime, timedelta
from AlgorithmImports import *

class TQQQAsymmetricBreakout(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.SetBenchmark("QQQ")
        
        self.sym = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        
        self.sma200 = self.SMA(self.qqq, 200, Resolution.Daily)
        self.atr = self.ATR(self.sym, 14, MovingAverageType.Wilders, Resolution.Daily)
        
        self.SetWarmUp(200, Resolution.Daily)
        self.trailing_stop = 0

    def OnData(self, data):
        if self.IsWarmingUp or not self.sma200.IsReady:
            return

        price = self.Securities[self.sym].Price
        qqq_price = self.Securities[self.qqq].Price
        s200 = self.sma200.Current.Value
        
        hist = self.History(self.sym, 2, Resolution.Daily)
        if len(hist) < 2: return
        
        prev_close = hist.iloc[-2].close
        today_open = hist.iloc[-1].open # Approximation for daily bars
        
        if not self.Portfolio.Invested:
            # Asymmetric Condition: Gap up open indicates momentum
            if qqq_price > s200 and today_open >= prev_close:
                self.SetHoldings(self.sym, 1.0)
                self.trailing_stop = price - (3 * self.atr.Current.Value)
        else:
            new_stop = price - (3 * self.atr.Current.Value)
            if new_stop > self.trailing_stop:
                self.trailing_stop = new_stop
                
            if price < self.trailing_stop or qqq_price < s200:
                self.Liquidate(self.sym)
