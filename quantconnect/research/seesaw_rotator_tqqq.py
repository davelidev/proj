from datetime import datetime, timedelta
from AlgorithmImports import *


class TQQQSeeSawRotator(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.SetBenchmark("QQQ")
        
        # Elite Growth Pair
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.soxl = self.AddEquity("SOXL", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        # Signals
        self.vix = self.AddData(CBOE, "VIX").Symbol
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        
        # Indicators
        self.sma200_spy = self.SMA(self.spy, 200, Resolution.Daily)
        self.vix_mom = self.MOMP(self.vix, 5, Resolution.Daily)
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
        vix_momentum = self.vix_mom.Current.Value
        sma_val = self.sma200_spy.Current.Value

        # THE SEE-SAW FILTER: Bull market AND Volatility is NOT increasing
        is_safe = spy_price > sma_val and vix_momentum < 0

        if is_safe:
            # ROTATION: Pick the strongest
            if self.mom_soxl.Current.Value > self.mom_tqqq.Current.Value:
                self.SetHoldings(self.soxl, 1.0)
            else:
                self.SetHoldings(self.tqqq, 1.0)
        else:
            # SAFETY: Move to BIL
            self.SetHoldings(self.bil, 1.0)
            self.Debug(f"SEE-SAW SAFETY at {self.Time}")
