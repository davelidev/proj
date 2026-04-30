from datetime import datetime, timedelta
from AlgorithmImports import *

class TQQQExpandingNoTrailing(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.SetBenchmark("QQQ")
        
        self.sym = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        
        self.adx = self.ADX(self.qqq, 10, Resolution.Daily)
        self.sma200 = self.SMA(self.qqq, 200, Resolution.Daily)
        
        self.SetWarmUp(200, Resolution.Daily)

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
            # Bull Market + Expanding Range + Trending (ADX>20)
            if qqq_price > s200 and r1 > r2 and adx_val > 20:
                self.SetHoldings(self.sym, 1.0)
        else:
            # Only exit if the macro trend breaks
            if qqq_price < s200:
                self.Liquidate(self.sym)
