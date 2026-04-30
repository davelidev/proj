from datetime import datetime, timedelta
from AlgorithmImports import *

class TQQQExpandingStrongVix(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.SetBenchmark("QQQ")
        
        self.sym = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.vix = self.AddData(CBOE, "VIX").Symbol
        self.vix3m = self.AddData(CBOE, "VIX3M").Symbol
        
        self.adx = self.ADX(self.qqq, 10, Resolution.Daily)
        self.sma200 = self.SMA(self.qqq, 200, Resolution.Daily)
        self.atr = self.ATR(self.sym, 14, MovingAverageType.Wilders, Resolution.Daily)
        
        self.SetWarmUp(200, Resolution.Daily)
        self.trailing_stop = 0

    def OnData(self, data):
        if self.IsWarmingUp or not self.adx.IsReady or not self.sma200.IsReady:
            return
        if not (self.Securities.ContainsKey(self.vix) and self.Securities.ContainsKey(self.vix3m)): return

        price = self.Securities[self.sym].Price
        qqq_price = self.Securities[self.qqq].Price
        s200 = self.sma200.Current.Value
        adx_val = self.adx.Current.Value
        vix_val = self.Securities[self.vix].Price
        vix3m_val = self.Securities[self.vix3m].Price
        
        vix_ratio = vix_val / vix3m_val if vix3m_val != 0 else 1.0
        
        hist = self.History(self.sym, 3, Resolution.Daily)
        if len(hist) < 3: return
        
        r2 = hist.iloc[-3].high - hist.iloc[-3].low
        r1 = hist.iloc[-2].high - hist.iloc[-2].low
        
        if vix_ratio > 1.0:
            self.Liquidate(self.sym)
            return
            
        if not self.Portfolio.Invested:
            if qqq_price > s200 and r1 > r2 and adx_val > 25:
                self.SetHoldings(self.sym, 1.0)
                self.trailing_stop = price - (3.0 * self.atr.Current.Value)
        else:
            new_stop = price - (3.0 * self.atr.Current.Value)
            if new_stop > self.trailing_stop:
                self.trailing_stop = new_stop
                
            if price < self.trailing_stop or qqq_price < s200:
                self.Liquidate(self.sym)
