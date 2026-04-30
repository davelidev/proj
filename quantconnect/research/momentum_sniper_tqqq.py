from datetime import datetime, timedelta
from AlgorithmImports import *


class TQQQMomentumSniper(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.SetBenchmark("QQQ")
        
        self.sym = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.vix = self.AddData(CBOE, "VIX").Symbol
        
        # High-Conviction Indicators
        self.high10 = self.MAX(self.sym, 10, Resolution.Daily)
        self.low10 = self.MIN(self.sym, 10, Resolution.Daily)
        self.sma200 = self.SMA(self.qqq, 200, Resolution.Daily)
        
        self.SetWarmUp(200, Resolution.Daily)
        
        self.Schedule.On(
            self.DateRules.EveryDay(self.sym),
            self.TimeRules.AfterMarketOpen(self.sym, 30),
            self.Rebalance,
        )

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma200.IsReady:
            return

        price = self.Securities[self.sym].Price
        qqq_price = self.Securities[self.qqq].Price
        vix_val = self.Securities[self.vix].Price
        sma_val = self.sma200.Current.Value
        
        # Get historical closes for confirmation logic (Entry #37)
        history = self.History(self.sym, 4, Resolution.Daily)
        if len(history) < 4: return
        
        c0 = history.iloc[-1].close
        c1 = history.iloc[-2].close
        c2 = history.iloc[-3].close
        c3 = history.iloc[-4].close

        # SAFETY SHIELD: Bull Market + Moderate Volatility
        is_safe = qqq_price > sma_val and vix_val < 28

        if not self.Portfolio.Invested:
            # ENTRY #37: New High + Multi-day Momentum Confirmation
            if is_safe:
                # C > 10-day High[1] AND confirmation sequence
                if price > self.high10.Current.Value and c0 > c1 and c0 > c3 and c1 > c2:
                    self.SetHoldings(self.sym, 1.0)
                    self.Debug(f"SNIPER ENTRY at {price}")
        else:
            # EXIT: 10-day low (Reverse Breakout) OR Trend Break OR Vol Spike
            if price <= self.low10.Current.Value or qqq_price < sma_val or vix_val > 30:
                self.Liquidate(self.sym)
                self.Debug(f"SNIPER EXIT at {price}")
