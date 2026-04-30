from datetime import datetime, timedelta
from AlgorithmImports import *

class AlphaShieldHybrid(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.SetBenchmark("QQQ")
        
        # Core Growth
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.soxl = self.AddEquity("SOXL", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        
        # High-Conviction Shields
        self.vix = self.AddData(CBOE, "VIX").Symbol
        self.vix3m = self.AddData(CBOE, "VIX3M").Symbol
        self.sma200 = self.SMA(self.qqq, 200, Resolution.Daily)
        self.rsi2 = self.RSI(self.qqq, 2, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi10 = self.RSI(self.tqqq, 10, MovingAverageType.Wilders, Resolution.Daily)
        
        self.SetWarmUp(200, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.AfterMarketOpen("QQQ", 35), self.Rebalance)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma200.IsReady: return
        if not (self.Securities.ContainsKey(self.vix) and self.Securities.ContainsKey(self.vix3m)): return

        qqq_price = self.Securities[self.qqq].Price
        vix_ratio = self.Securities[self.vix].Price / self.Securities[self.vix3m].Price if self.Securities[self.vix3m].Price != 0 else 1.0
        sma_val = self.sma200.Current.Value
        r2 = self.rsi2.Current.Value
        r10 = self.rsi10.Current.Value

        # THE HYBRID SHIELD: Bull trend AND No structural panic
        is_safe = qqq_price > sma_val and vix_ratio < 1.05

        if is_safe:
            if not self.Portfolio.Invested:
                # ENTRY on high-conviction dip
                if r2 < 25:
                    self.SetHoldings(self.tqqq, 1.0)
                    self.Debug(f"ALPHA SHIELD ENTRY at {qqq_price}")
            else:
                # DYNAMIC LEVERAGE / PROFIT LOCK
                if r10 > 80:
                    self.Liquidate() # Lock in gains before the pullback
                    self.Debug(f"ALPHA SHIELD PROFIT LOCK at {qqq_price}")
        else:
            # SAFETY: Move to Cash
            if self.Portfolio.Invested:
                self.Liquidate()
                self.Debug(f"ALPHA SHIELD EXIT: Panic/Trend Break at {qqq_price}")
