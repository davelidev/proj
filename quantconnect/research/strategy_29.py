from datetime import datetime, timedelta
from AlgorithmImports import *

class TQQQExpandingVixRatio(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.SetBenchmark("QQQ")
        
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.vix = self.AddData(CBOE, "VIX").Symbol
        self.vix3m = self.AddData(CBOE, "VIX3M").Symbol
        
        self.adx = self.ADX(self.qqq, 14, Resolution.Daily)
        self.sma200 = self.SMA(self.qqq, 200, Resolution.Daily)
        
        self.SetWarmUp(200, Resolution.Daily)

    def OnData(self, data):
        if self.IsWarmingUp or not self.adx.IsReady or not self.sma200.IsReady:
            return
        if not (self.Securities.ContainsKey(self.vix) and self.Securities.ContainsKey(self.vix3m)): return

        qqq_price = self.Securities[self.qqq].Price
        s200 = self.sma200.Current.Value
        adx_val = self.adx.Current.Value
        vix_val = self.Securities[self.vix].Price
        vix3m_val = self.Securities[self.vix3m].Price
        
        vix_ratio = vix_val / vix3m_val if vix3m_val != 0 else 1.0
        
        hist_qqq = self.History(self.qqq, 3, Resolution.Daily)
        if len(hist_qqq) < 3: return
        
        r2 = hist_qqq.iloc[-3].high - hist_qqq.iloc[-3].low
        r1 = hist_qqq.iloc[-2].high - hist_qqq.iloc[-2].low
        
        # Kill Switch
        if vix_ratio > 1.0 or qqq_price < s200:
            self.Liquidate()
            return
            
        if not self.Portfolio.Invested:
            if r1 > r2 and adx_val > 20:
                self.SetHoldings(self.tqqq, 1.0)
