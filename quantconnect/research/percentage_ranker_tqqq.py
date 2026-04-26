from datetime import datetime, timedelta
from AlgorithmImports import *
import numpy as np


class TQQQPercentageRanker(QCAlgorithm):

    def Initialize(self):
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100_000)
        self.SetBenchmark("QQQ")
        
        self.sym = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        
        # Indicators
        self.adx = self.ADX(self.sym, 14, Resolution.Daily)
        self.sma200 = self.SMA(self.sym, 200, Resolution.Daily)
        
        # We'll use a manual sliding window for percentile
        self.window = RollingWindow[float](25)
        
        self.SetWarmUp(200, Resolution.Daily)
        
        self.Schedule.On(
            self.DateRules.EveryDay(self.sym),
            self.TimeRules.AfterMarketOpen(self.sym, 35),
            self.Rebalance,
        )

    def OnData(self, data):
        # Improved data access with safety check
        if data.Bars.ContainsKey(self.sym) and data.Bars[self.sym] is not None:
            self.window.Add(data.Bars[self.sym].Close)

    def Rebalance(self):
        if self.IsWarmingUp or not self.adx.IsReady or not self.window.IsReady:
            return

        price = self.Securities[self.sym].Price
        adx_val = self.adx.Current.Value
        sma_val = self.sma200.Current.Value
        
        # Calculate percentiles
        closes = [x for x in self.window]
        p75 = np.percentile(closes, 75)
        p25 = np.percentile(closes, 25)

        if not self.Portfolio.Invested:
            # ENTRY: Bull market AND Trending (20 < ADX < 30) AND breaking high percentile
            if price > sma_val and adx_val > 20 and adx_val < 30 and price > p75:
                self.SetHoldings(self.sym, 1.0)
                self.Debug(f"RANKER ENTRY at {price}")
        else:
            # EXIT: Falling below 25th percentile OR Trend Break
            if price < p25 or price < sma_val:
                self.Liquidate(self.sym)
                self.Debug(f"RANKER EXIT at {price}")
