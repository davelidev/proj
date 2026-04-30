from datetime import datetime, timedelta
from AlgorithmImports import *
import numpy as np

class StrategyTemplateV2(QCAlgorithm):
    def Initialize(self):
        # Parameters (provided via API)
        self.sma_len = int(self.GetParameter("sma_len", 200))
        self.rsi_trigger = float(self.GetParameter("rsi_trigger", 25))
        self.vix_limit = float(self.GetParameter("vix_limit", 28))
        self.tail_thresh = float(self.GetParameter("tail_thresh", 0.5)) # Entry #36 logic
        self.atr_kill_mult = float(self.GetParameter("atr_kill_mult", 2.0)) # Chapter 6 logic
        self.exit_days = int(self.GetParameter("exit_days", 5)) # Tip #1 fixed exit
        
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        
        # Assets
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.vix = self.AddData(CBOE, "VIX").Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        # Indicators
        self.sma = self.SMA(self.qqq, self.sma_len, Resolution.Daily)
        self.rsi = self.RSI(self.qqq, 2, MovingAverageType.Wilders, Resolution.Daily)
        self.atr = self.ATR(self.tqqq, 14, MovingAverageType.Wilders, Resolution.Daily)
        
        self.SetWarmUp(self.sma_len, Resolution.Daily)
        self.entry_date = datetime.min

    def OnData(self, data):
        if self.IsWarmingUp or not self.sma.IsReady:
            return
            
        qqq_price = self.Securities[self.qqq].Price
        vix_val = self.Securities[self.vix].Price
        price = self.Securities[self.tqqq].Price
        atr_val = self.atr.Current.Value
        
        # 1. HIGH VOLATILITY KILL SWITCH (Chapter 6)
        # If range of current bar is too large relative to ATR, stay out
        current_range = self.Securities[self.tqqq].High - self.Securities[self.tqqq].Low
        is_vol_kill = current_range > (self.atr_kill_mult * atr_val)
        
        # 2. BIG TAIL BARS (Entry #36)
        # Ratio of bottom tail to total range
        bull_tail = (min(self.Securities[self.tqqq].Open, self.Securities[self.tqqq].Close) - self.Securities[self.tqqq].Low) / (current_range if current_range > 0 else 1)
        is_bull_tail = bull_tail > self.tail_thresh

        # 3. REGIME SHIELD
        is_safe = qqq_price > self.sma.Current.Value and vix_val < self.vix_limit and not is_vol_kill

        if not self.Portfolio.Invested:
            # ENTRY: Safe Regime + (RSI Dip OR Bull Tail)
            if is_safe and (self.rsi.Current.Value < self.rsi_trigger or is_bull_tail):
                self.SetHoldings(self.tqqq, 1.0)
                self.entry_date = self.Time
        else:
            # EXIT: Fixed Time Exit (Cheat Code Tip #1) OR Trend Break
            days_held = (self.Time - self.entry_date).days
            if days_held >= self.exit_days or qqq_price < self.sma.Current.Value:
                self.Liquidate()
