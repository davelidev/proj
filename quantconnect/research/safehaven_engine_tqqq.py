from datetime import datetime, timedelta
from AlgorithmImports import *


class TQQQSafeHavenEngine(QCAlgorithm):

    def Initialize(self):
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100_000)
        self.SetBenchmark("QQQ")
        
        # Core Assets
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.soxl = self.AddEquity("SOXL", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        # Structural Signal
        self.vix = self.AddData(CBOE, "VIX").Symbol
        self.vix3m = self.AddData(CBOE, "VIX3M").Symbol
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        
        # Indicators
        self.sma200_spy = self.SMA(self.spy, 200, Resolution.Daily)
        self.mom_tqqq = self.MOMP(self.tqqq, 21, Resolution.Daily)
        self.mom_soxl = self.MOMP(self.soxl, 21, Resolution.Daily)
        
        self.SetWarmUp(200, Resolution.Daily)
        
        self.Schedule.On(
            self.DateRules.EveryDay(self.spy),
            self.TimeRules.AfterMarketOpen(self.spy, 35),
            self.Rebalance,
        )

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma200_spy.IsReady:
            return

        spy_price = self.Securities[self.spy].Price
        vix = self.Securities[self.vix].Price
        vix3m = self.Securities[self.vix3m].Price
        
        # Structural panic switch (Backwardation)
        vix_ratio = vix / vix3m if vix3m != 0 else 1.0
        
        # THE SAFE-HAVEN SHIELD
        # Must be in long-term bull market AND no structural panic
        is_safe = spy_price > self.sma200_spy.Current.Value and vix_ratio < 1.0
        
        if is_safe:
            # ROTATION: Pick strongest if it has positive momentum
            if self.mom_soxl.Current.Value > self.mom_tqqq.Current.Value and self.mom_soxl.Current.Value > 0:
                self.SetHoldings(self.soxl, 1.0)
            elif self.mom_tqqq.Current.Value > 0:
                self.SetHoldings(self.tqqq, 1.0)
            else:
                self.SetHoldings(self.bil, 1.0)
        else:
            # SHIELD ACTIVE
            self.SetHoldings(self.bil, 1.0)
            self.Debug(f"SHIELD ACTIVE at {self.Time} (VIX Ratio: {vix_ratio:.2f})")
