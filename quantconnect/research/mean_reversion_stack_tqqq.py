from datetime import datetime, timedelta
from AlgorithmImports import *


class TQQQMeanReversionStack(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.SetBenchmark("QQQ")
        
        self.sym = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        
        # Manual ConnorsRSI Components
        self.rsi_price = self.RSI(self.sym, 3, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi_streak = self.RSI(self.sym, 2, MovingAverageType.Wilders, Resolution.Daily) # Simplified streak proxy
        self.bb = self.BB(self.sym, 20, 2, MovingAverageType.Simple, Resolution.Daily)
        self.sma200 = self.SMA(self.sym, 200, Resolution.Daily)
        self.sma20 = self.SMA(self.sym, 20, Resolution.Daily)
        
        self.SetWarmUp(200, Resolution.Daily)
        
        self.Schedule.On(
            self.DateRules.EveryDay(self.sym),
            self.TimeRules.AfterMarketOpen(self.sym, 35),
            self.Rebalance,
        )

    def Rebalance(self):
        if self.IsWarmingUp or not self.rsi_price.IsReady or not self.bb.IsReady:
            return

        price = self.Securities[self.sym].Price
        # Composite oversold signal using RSI(3) as a base
        rsi_val = self.rsi_price.Current.Value
        lower_bb = self.bb.LowerBand.Current.Value
        sma200_val = self.sma200.Current.Value
        sma20_val = self.sma20.Current.Value

        if not self.Portfolio.Invested:
            # ENTRY: Bull market + Stacked Oversold
            if price > sma200_val and rsi_val < 15 and price < lower_bb:
                self.SetHoldings(self.sym, 1.0)
        else:
            # EXIT: Recovery to SMA20 or Trend Break
            if price > sma20_val or price < sma200_val:
                self.Liquidate(self.sym)
