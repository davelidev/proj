from datetime import datetime, timedelta
from AlgorithmImports import *

class TQQQExpandingSoxlRotator(QCAlgorithm):
    """
    Strategy 35: Expanding SOXL Rotator

Core Concept:
- Focused rotation between TQQQ and SOXL based on volatility expansion.
- Includes an ADX > 30 'Turbo' filter to identify high-momentum trends.
- Exits on 2.5 ATR trailing stop.
    """
    def Initialize(self):
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100_000)
        self.SetBenchmark("QQQ")
        
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.soxl = self.AddEquity("SOXL", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        
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

        qqq_price = self.Securities[self.qqq].Price
        s200 = self.sma200.Current.Value
        adx_val = self.adx.Current.Value
        
        hist_qqq = self.History(self.qqq, 3, Resolution.Daily)
        if len(hist_qqq) < 3: return
        
        r2 = hist_qqq.iloc[-3].high - hist_qqq.iloc[-3].low
        r1 = hist_qqq.iloc[-2].high - hist_qqq.iloc[-2].low
        
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
