from AlgorithmImports import *
import numpy as np

class TQQQSOXLRotation(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.soxl = self.AddEquity("SOXL", Resolution.Daily).Symbol
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        
        # Indicators
        self.ema_tqqq = self.EMA(self.tqqq, 50, Resolution.Daily)
        self.ema_soxl = self.EMA(self.soxl, 50, Resolution.Daily)
        self.spy_sma = self.SMA(self.spy, 200, Resolution.Daily)
        
        # Custom indicator for SR and SA
        self.sr_history = RollingWindow[float](200)
        
        # Volatility (Standard Deviation of daily returns)
        self.std_tqqq = self.STD(self.tqqq, 20, Resolution.Daily)
        self.std_soxl = self.STD(self.soxl, 20, Resolution.Daily)

    def OnData(self, data):
        if not (self.ema_tqqq.IsReady and self.ema_soxl.IsReady and self.std_tqqq.IsReady and self.spy_sma.IsReady):
            return

        # 1. Calculate Strategic Ratio (SR)
        sr = self.ema_soxl.Current.Value / self.ema_tqqq.Current.Value
        self.sr_history.Add(sr)
        
        if not self.sr_history.IsReady:
            return

        # 2. Market Regime Filter
        if self.Securities[self.spy].Price < self.spy_sma.Current.Value:
            self.Liquidate()
            return
            
        # 3. Calculate Strategic Anchor (SA) - 200 day SMA of SR
        sa = sum(self.sr_history) / self.sr_history.Count
        
        # 4. Relative Strength (RS)
        rs = sr / sa
        
        # 5. Final Ratio (FR) with Volatility Adjustment
        # Note: 2.5 is a common scaling factor used in this specific community strategy
        vol_ratio = self.std_soxl.Current.Value / (2.5 * self.std_tqqq.Current.Value) if self.std_tqqq.Current.Value != 0 else 1
        fr = rs / vol_ratio if vol_ratio != 0 else 1
        
        # 6. Execution Logic
        if fr >= 1.10:
            self.SetHoldings(self.soxl, 1.0)
        elif fr <= 0.90:
            self.SetHoldings(self.tqqq, 1.0)
        else:
            # Linear scaling between 0.9 and 1.1
            soxl_weight = (fr - 0.90) / 0.20
            self.SetHoldings(self.soxl, soxl_weight)
            self.SetHoldings(self.tqqq, 1.0 - soxl_weight)
