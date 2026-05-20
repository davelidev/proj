from datetime import datetime, timedelta
from AlgorithmImports import *

class TQQQSOXLVixRatio110(QCAlgorithm):
    """
    Strategy 38: Alpha-Max Expanding Rotator
    
    Core Concept:
    - Entering trades based on Expanding Volatility (Range1 > Range2) and strong ADX (>20).
    - Rotates between TQQQ and SOXL based on 21-day momentum.
    - Features a structural 'Kill Switch' based on VIX/VIX3M Ratio > 1.10 (Backwardation).
    """
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.SetBenchmark("QQQ")
        
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.soxl = self.AddEquity("SOXL", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        
        self.vix = self.AddData(CBOE, "VIX").Symbol
        self.vix3m = self.AddData(CBOE, "VIX3M").Symbol
        
        self.adx = self.ADX(self.qqq, 10, Resolution.Daily)
        self.sma200 = self.SMA(self.qqq, 200, Resolution.Daily)
        self.atr_tqqq = self.ATR(self.tqqq, 14, MovingAverageType.Wilders, Resolution.Daily)
        self.atr_soxl = self.ATR(self.soxl, 14, MovingAverageType.Wilders, Resolution.Daily)
        
        self.mom_tqqq = self.MOMP(self.tqqq, 21, Resolution.Daily)
        self.mom_soxl = self.MOMP(self.soxl, 21, Resolution.Daily)
        
        self.SetWarmUp(200, Resolution.Daily)
        self.trailing_stop = 0

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
        
        # Kill Switch at Extreme Backwardation (>1.10)
        if vix_ratio > 1.10:
            self.Liquidate()
            return
            
        if not self.Portfolio.Invested:
            if qqq_price > s200 and r1 > r2 and adx_val > 25:
                if adx_val > 30 and self.mom_soxl.Current.Value > self.mom_tqqq.Current.Value:
                    self.SetHoldings(self.soxl, 1.0)
                    self.trailing_stop = self.Securities[self.soxl].Price - (3.0 * self.atr_soxl.Current.Value)
                else:
                    self.SetHoldings(self.tqqq, 1.0)
                    self.trailing_stop = self.Securities[self.tqqq].Price - (3.0 * self.atr_tqqq.Current.Value)
        else:
            if self.Portfolio[self.soxl].Invested:
                price = self.Securities[self.soxl].Price
                new_stop = price - (3.0 * self.atr_soxl.Current.Value)
                if new_stop > self.trailing_stop:
                    self.trailing_stop = new_stop
                if price < self.trailing_stop or qqq_price < s200:
                    self.Liquidate()
            elif self.Portfolio[self.tqqq].Invested:
                price = self.Securities[self.tqqq].Price
                new_stop = price - (3.0 * self.atr_tqqq.Current.Value)
                if new_stop > self.trailing_stop:
                    self.trailing_stop = new_stop
                if price < self.trailing_stop or qqq_price < s200:
                    self.Liquidate()
