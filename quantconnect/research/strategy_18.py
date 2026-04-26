from datetime import datetime, timedelta
from AlgorithmImports import *

class TQQQExpandingFastExit(QCAlgorithm):
    def Initialize(self):
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100_000)
        self.SetBenchmark("QQQ")
        
        self.sym = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        
        self.adx = self.ADX(self.qqq, 10, Resolution.Daily)
        self.sma200 = self.SMA(self.qqq, 200, Resolution.Daily)
        self.atr = self.ATR(self.sym, 14, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi2 = self.RSI(self.sym, 2, MovingAverageType.Wilders, Resolution.Daily)
        
        self.SetWarmUp(200, Resolution.Daily)
        self.trailing_stop = 0

    def OnData(self, data):
        if self.IsWarmingUp or not self.adx.IsReady or not self.sma200.IsReady:
            return

        price = self.Securities[self.sym].Price
        qqq_price = self.Securities[self.qqq].Price
        s200 = self.sma200.Current.Value
        adx_val = self.adx.Current.Value
        
        hist = self.History(self.sym, 3, Resolution.Daily)
        if len(hist) < 3: return
        
        r2 = hist.iloc[-3].high - hist.iloc[-3].low
        r1 = hist.iloc[-2].high - hist.iloc[-2].low
        
        if not self.Portfolio.Invested:
            if qqq_price > s200 and r1 > r2 and adx_val > 20:
                self.SetHoldings(self.sym, 1.0)
                self.trailing_stop = price - (2.5 * self.atr.Current.Value)
        else:
            new_stop = price - (2.5 * self.atr.Current.Value)
            if new_stop > self.trailing_stop:
                self.trailing_stop = new_stop
                
            # Added fast RSI exit to lock in profits quicker
            if price < self.trailing_stop or qqq_price < s200 or self.rsi2.Current.Value > 80:
                self.Liquidate(self.sym)
