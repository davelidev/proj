from datetime import datetime, timedelta
from AlgorithmImports import *

class EliteAlphaShield(QCAlgorithm):
    def Initialize(self):
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100_000)
        self.SetBenchmark("QQQ")
        
        # Growth Asset
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        # Dual-Fear Shields
        self.vix = self.AddData(CBOE, "VIX").Symbol
        self.vix3m = self.AddData(CBOE, "VIX3M").Symbol
        self.sma200 = self.SMA(self.qqq, 200, Resolution.Daily)
        self.vix_mom = self.MOMP(self.vix, 1, Resolution.Daily) # 1-day VIX change
        
        # Triggers
        self.rsi2 = self.RSI(self.qqq, 2, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi10 = self.RSI(self.tqqq, 10, MovingAverageType.Wilders, Resolution.Daily)
        
        self.SetWarmUp(200, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.AfterMarketOpen("QQQ", 35), self.Rebalance)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma200.IsReady: return
        if not (self.Securities.ContainsKey(self.vix) and self.Securities.ContainsKey(self.vix3m)): return

        qqq_price = self.Securities[self.qqq].Price
        vix_val = self.Securities[self.vix].Price
        vix_ratio = vix_val / self.Securities[self.vix3m].Price if self.Securities[self.vix3m].Price != 0 else 1.0
        vix_spike = self.vix_mom.Current.Value
        sma_val = self.sma200.Current.Value

        # THE ELITE SHIELD: 
        # 1. Long-term Trend is Up
        # 2. VIX structure is in Contango (Safe)
        # 3. No massive volatility spikes
        is_safe = qqq_price > sma_val and vix_ratio < 1.02 and vix_spike < 0.10

        if is_safe:
            if not self.Portfolio.Invested:
                # ENTRY on high-conviction dip
                if self.rsi2.Current.Value < 25:
                    self.SetHoldings(self.tqqq, 1.0)
            else:
                # DYNAMIC PROFIT LOCK
                if self.rsi10.Current.Value > 80:
                    self.Liquidate()
        else:
            # SAFETY: Move to BIL
            if self.Portfolio.Invested:
                self.Liquidate()
                self.Debug(f"ELITE SHIELD EXIT: VIX Ratio {vix_ratio:.2f}, Spike {vix_spike:.2f}")
