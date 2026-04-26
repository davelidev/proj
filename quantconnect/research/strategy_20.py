from datetime import datetime, timedelta
from AlgorithmImports import *

class TQQQFridayTurbo(QCAlgorithm):
    def Initialize(self):
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100_000)
        
        self.sym = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        
        self.high = self.MAX(self.sym, 25, Resolution.Daily)
        self.sma200 = self.SMA(self.qqq, 200, Resolution.Daily)
        self.rsi10 = self.RSI(self.sym, 10, MovingAverageType.Wilders, Resolution.Daily)
        
        self.SetWarmUp(200, Resolution.Daily)
        self.trigger_on_friday = False

    def OnData(self, data):
        if self.IsWarmingUp or not self.sma200.IsReady: return
        
        price = self.Securities[self.sym].Price
        qqq_price = self.Securities[self.qqq].Price
        day = self.Time.weekday()
        
        # Friday: Identify the breakout
        if day == 4:
            if price >= self.high.Current.Value and qqq_price > self.sma200.Current.Value:
                self.trigger_on_friday = True
            else:
                self.trigger_on_friday = False
        
        # Monday: Enter 100% TQQQ
        if day == 0 and self.trigger_on_friday:
            if not self.Portfolio.Invested:
                self.SetHoldings(self.sym, 1.0)
                self.trigger_on_friday = False
        
        # Dynamic Exit: RSI10 exhaustion
        if self.Portfolio.Invested:
            if self.rsi10.Current.Value > 80 or qqq_price < self.sma200.Current.Value:
                self.Liquidate(self.sym)
