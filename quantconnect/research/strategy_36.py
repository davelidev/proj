from datetime import datetime, timedelta
from AlgorithmImports import *

class TQQQTECLSOXLRotator(QCAlgorithm):
    """
    Strategy 36: Triple-LETF Rotator (TQQQ/SOXL/TECL)

Core Concept:
- Multi-asset momentum rotation among three 3x leveraged ETFs.
- Uses Expanding Range signals and ADX trend filters.
- Rotates daily to the asset with strongest 21-day momentum.
    """
    def Initialize(self):
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100_000)
        self.SetBenchmark("QQQ")
        
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.soxl = self.AddEquity("SOXL", Resolution.Daily).Symbol
        self.tecl = self.AddEquity("TECL", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        
        self.adx = self.ADX(self.qqq, 10, Resolution.Daily)
        self.sma200 = self.SMA(self.qqq, 200, Resolution.Daily)
        
        self.atr_tqqq = self.ATR(self.tqqq, 14, MovingAverageType.Wilders, Resolution.Daily)
        self.atr_soxl = self.ATR(self.soxl, 14, MovingAverageType.Wilders, Resolution.Daily)
        self.atr_tecl = self.ATR(self.tecl, 14, MovingAverageType.Wilders, Resolution.Daily)
        
        self.mom_tqqq = self.MOMP(self.tqqq, 21, Resolution.Daily)
        self.mom_soxl = self.MOMP(self.soxl, 21, Resolution.Daily)
        self.mom_tecl = self.MOMP(self.tecl, 21, Resolution.Daily)
        
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
                # Find best momentum
                m_t = self.mom_tqqq.Current.Value
                m_s = self.mom_soxl.Current.Value
                m_te = self.mom_tecl.Current.Value
                
                best_mom = max(m_t, m_s, m_te)
                
                if adx_val > 30:
                    if best_mom == m_s:
                        self.SetHoldings(self.soxl, 1.0)
                        self.trailing_stop = self.Securities[self.soxl].Price - (3.0 * self.atr_soxl.Current.Value)
                    elif best_mom == m_te:
                        self.SetHoldings(self.tecl, 1.0)
                        self.trailing_stop = self.Securities[self.tecl].Price - (3.0 * self.atr_tecl.Current.Value)
                    else:
                        self.SetHoldings(self.tqqq, 1.0)
                        self.trailing_stop = self.Securities[self.tqqq].Price - (3.0 * self.atr_tqqq.Current.Value)
                else:
                    self.SetHoldings(self.tqqq, 1.0)
                    self.trailing_stop = self.Securities[self.tqqq].Price - (3.0 * self.atr_tqqq.Current.Value)
        else:
            invested_sym = None
            for sym in [self.tqqq, self.soxl, self.tecl]:
                if self.Portfolio[sym].Invested:
                    invested_sym = sym
                    break
                    
            if invested_sym:
                price = self.Securities[invested_sym].Price
                atr = self.atr_soxl if invested_sym == self.soxl else (self.atr_tecl if invested_sym == self.tecl else self.atr_tqqq)
                
                new_stop = price - (3.0 * atr.Current.Value)
                if new_stop > self.trailing_stop:
                    self.trailing_stop = new_stop
                    
                if price < self.trailing_stop or qqq_price < s200:
                    self.Liquidate()
