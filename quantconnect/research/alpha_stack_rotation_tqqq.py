from datetime import datetime, timedelta
from AlgorithmImports import *


class TQQQAlphaStackRotation(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.SetBenchmark("QQQ")
        
        # Performance Pair
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.soxl = self.AddEquity("SOXL", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.vix = self.AddData(CBOE, "VIX").Symbol
        
        # Indicators
        self.sma200 = self.SMA(self.qqq, 200, Resolution.Daily)
        self.mom_tqqq = self.MOMP(self.tqqq, 21, Resolution.Daily)
        self.mom_soxl = self.MOMP(self.soxl, 21, Resolution.Daily)
        
        self.SetWarmUp(200, Resolution.Daily)
        
        self.Schedule.On(
            self.DateRules.EveryDay(self.qqq),
            self.TimeRules.AfterMarketOpen(self.qqq, 35),
            self.Rebalance,
        )

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma200.IsReady:
            return

        qqq_price = self.Securities[self.qqq].Price
        vix_val = self.Securities[self.vix].Price
        sma_val = self.sma200.Current.Value

        # ALPHA SHIELD: Bull Market + Low Volatility Stress
        is_high_conviction = qqq_price > sma_val and vix_val < 26 # Tighter vol shield for SOXL

        if is_high_conviction:
            # ROTATION: Pick the strongest sector
            if self.mom_soxl.Current.Value > self.mom_tqqq.Current.Value:
                self.SetHoldings(self.soxl, 1.0)
            else:
                self.SetHoldings(self.tqqq, 1.0)
        else:
            # SAFETY: Sit in Cash
            self.Liquidate()
            self.Debug(f"ALPHA SHIELD ACTIVE at {self.Time}")
