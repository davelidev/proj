from datetime import datetime, timedelta
from AlgorithmImports import *

class StrategyTemplateV3(QCAlgorithm):
    def Initialize(self):
        # Parameters for Optimization
        self.adx_thresh = float(self.GetParameter("adx_thresh", 20))
        self.vix_ratio_limit = float(self.GetParameter("vix_ratio_limit", 1.05))
        self.atr_mult = float(self.GetParameter("atr_mult", 3.0))
        self.mom_period = int(self.GetParameter("mom_period", 21))
        
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        
        # Core Assets
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.soxl = self.AddEquity("SOXL", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.vix = self.AddData(CBOE, "VIX").Symbol
        self.vix3m = self.AddData(CBOE, "VIX3M").Symbol
        
        # Indicators
        self.adx = self.ADX(self.qqq, 10, Resolution.Daily)
        self.sma200 = self.SMA(self.qqq, 200, Resolution.Daily)
        self.mom_tqqq = self.MOMP(self.tqqq, self.mom_period, Resolution.Daily)
        self.mom_soxl = self.MOMP(self.soxl, self.mom_period, Resolution.Daily)
        self.atr_tqqq = self.ATR(self.tqqq, 14, MovingAverageType.Wilders, Resolution.Daily)
        self.atr_soxl = self.ATR(self.soxl, 14, MovingAverageType.Wilders, Resolution.Daily)
        
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
        
        # Structural Panic Switch
        if vix_ratio > self.vix_ratio_limit or qqq_price < s200:
            self.Liquidate()
            self.trailing_stop = 0
            return
            
        hist = self.History(self.qqq, 3, Resolution.Daily)
        if len(hist) < 3: return
        r2 = hist.iloc[-3].high - hist.iloc[-3].low
        r1 = hist.iloc[-2].high - hist.iloc[-2].low

        if not self.Portfolio.Invested:
            # Expanding Range + Trend Confirmation
            if r1 > r2 and adx_val > self.adx_thresh:
                # Rotate to strongest
                if self.mom_soxl.Current.Value > self.mom_tqqq.Current.Value:
                    self.SetHoldings(self.soxl, 1.0)
                    self.trailing_stop = self.Securities[self.soxl].Price - (self.atr_mult * self.atr_soxl.Current.Value)
                else:
                    self.SetHoldings(self.tqqq, 1.0)
                    self.trailing_stop = self.Securities[self.tqqq].Price - (self.atr_mult * self.atr_tqqq.Current.Value)
        else:
            invested_sym = self.tqqq if self.Portfolio[self.tqqq].Invested else self.soxl
            price = self.Securities[invested_sym].Price
            atr = self.atr_tqqq if invested_sym == self.tqqq else self.atr_soxl
            
            # Update Trailing Stop
            new_stop = price - (self.atr_mult * atr.Current.Value)
            if new_stop > self.trailing_stop:
                self.trailing_stop = new_stop
                
            if price < self.trailing_stop:
                self.Liquidate()
                self.trailing_stop = 0
