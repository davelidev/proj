from datetime import datetime, timedelta
from AlgorithmImports import *
import numpy as np

class StrategyTemplate(QCAlgorithm):
    """
    Automated Research Template: Cheat Code Optimizer
    
    Core Concept:
    - Flexible engine used to iterate 300+ combinations of RSI, SMA, VIX, and ATR stop parameters.
    - Features a structural trend filter (SMA200) and VIX/VIX3M Ratio shield.
    - Used to identify Iterations 60, 69, and 192 as elite winners.
    """
    def Initialize(self):
        # Parameters (provided via API)
        self.sma200_len = int(self.GetParameter("sma200_len", 200))
        self.rsi_trigger = float(self.GetParameter("rsi_trigger", 30))
        self.rsi_exit = float(self.GetParameter("rsi_exit", 80))
        self.vix_limit = float(self.GetParameter("vix_limit", 28))
        self.vix_ratio_limit = float(self.GetParameter("vix_ratio_limit", 1.05))
        self.use_soxl = self.GetParameter("use_soxl", "true").lower() == "true"
        self.atr_stop_mult = float(self.GetParameter("atr_stop_mult", 3.0))
        
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100_000)
        self.SetBenchmark("QQQ")
        
        # Core Assets
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        self.vix = self.AddData(CBOE, "VIX").Symbol
        self.vix3m = self.AddData(CBOE, "VIX3M").Symbol
        
        if self.use_soxl:
            self.soxl = self.AddEquity("SOXL", Resolution.Daily).Symbol
            self.mom_soxl = self.MOMP(self.soxl, 21, Resolution.Daily)
            
        # Indicators
        self.sma200 = self.SMA(self.qqq, self.sma200_len, Resolution.Daily)
        self.rsi2 = self.RSI(self.qqq, 2, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi10 = self.RSI(self.tqqq, 10, MovingAverageType.Wilders, Resolution.Daily)
        self.atr = self.ATR(self.tqqq, 14, MovingAverageType.Wilders, Resolution.Daily)
        self.mom_tqqq = self.MOMP(self.tqqq, 21, Resolution.Daily)
        
        self.SetWarmUp(self.sma200_len, Resolution.Daily)
        self.trailing_stop = 0
        
        self.Schedule.On(
            self.DateRules.EveryDay(self.qqq),
            self.TimeRules.AfterMarketOpen(self.qqq, 35),
            self.Rebalance,
        )

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma200.IsReady:
            return
            
        if not (self.Securities.ContainsKey(self.vix) and self.Securities.ContainsKey(self.vix3m)):
            return

        qqq_price = self.Securities[self.qqq].Price
        vix_val = self.Securities[self.vix].Price
        vix3m_val = self.Securities[self.vix3m].Price
        vix_ratio = vix_val / vix3m_val if vix3m_val != 0 else 1.0
        
        # 1. SHIELD CONDITIONS
        is_safe = (qqq_price > self.sma200.Current.Value and 
                   vix_val < self.vix_limit and 
                   vix_ratio < self.vix_ratio_limit)
        
        if is_safe:
            # 2. ROTATION & DIP BUY
            # Entry on RSI pullback
            if self.rsi2.Current.Value < self.rsi_trigger:
                target_sym = self.tqqq
                if self.use_soxl and self.mom_soxl.Current.Value > self.mom_tqqq.Current.Value:
                    target_sym = self.soxl
                
                if not self.Portfolio[target_sym].Invested:
                    self.SetHoldings(target_sym, 1.0)
                    self.trailing_stop = self.Securities[target_sym].Price - (self.atr_stop_mult * self.atr.Current.Value)
            
            # Update stop and check exit
            if self.Portfolio.Invested:
                # Get the invested security
                invested_sec = [s for s in self.Portfolio.Values if s.Invested][0]
                price = invested_sec.Price
                
                # Check RSI exit
                if self.rsi10.Current.Value > self.rsi_exit:
                    self.Liquidate()
                    self.trailing_stop = 0
                    return
                
                # Update trailing stop
                new_stop = price - (self.atr_stop_mult * self.atr.Current.Value)
                if new_stop > self.trailing_stop:
                    self.trailing_stop = new_stop
                
                if price < self.trailing_stop:
                    self.Liquidate()
                    self.trailing_stop = 0
        else:
            # SAFETY: Rotate to BIL
            if not self.Portfolio[self.bil].Invested:
                self.SetHoldings(self.bil, 1.0)
                self.trailing_stop = 0
