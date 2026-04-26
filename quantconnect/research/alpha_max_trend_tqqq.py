from datetime import datetime, timedelta
from AlgorithmImports import *


class TQQQAlphaMaxTrend(QCAlgorithm):

    def Initialize(self):
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100_000)
        self.SetBenchmark("QQQ")
        
        self.sym = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        
        # High-Conviction Indicators
        self.sma20 = self.SMA(self.sym, 20, Resolution.Daily)
        self.sma50 = self.SMA(self.sym, 50, Resolution.Daily)
        self.sma200 = self.SMA(self.sym, 200, Resolution.Daily)
        self.rsi10 = self.RSI(self.sym, 10, MovingAverageType.Wilders, Resolution.Daily)
        self.atr = self.ATR(self.sym, 14, MovingAverageType.Wilders, Resolution.Daily)
        
        self.SetWarmUp(200, Resolution.Daily)
        
        self.Schedule.On(
            self.DateRules.EveryDay(self.sym),
            self.TimeRules.AfterMarketOpen(self.sym, 30),
            self.Rebalance,
        )
        
        self.trailing_stop = 0

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma200.IsReady:
            return

        price = self.Securities[self.sym].Price
        s20 = self.sma20.Current.Value
        s50 = self.sma50.Current.Value
        s200 = self.sma200.Current.Value
        r10 = self.rsi10.Current.Value
        atr_val = self.atr.Current.Value

        if not self.Portfolio.Invested:
            # ENTRY: Major trend is up (Price > s200) AND short-term dip (RSI < 40)
            # Confirmed by being above mid-term SMA50
            if price > s200 and price > s50 and r10 < 40:
                self.SetHoldings(self.sym, 1.0)
                self.trailing_stop = price - (3 * atr_val)
                self.Debug(f"ALPHA ENTRY at {price}")
        else:
            # EXIT: 
            # 1. Update trailing stop
            new_stop = price - (3 * atr_val)
            if new_stop > self.trailing_stop:
                self.trailing_stop = new_stop
            
            # 2. Exit on trend break (Price < s50) OR trailing stop
            if price < s50 or price < self.trailing_stop:
                self.Liquidate(self.sym)
                self.Debug(f"ALPHA EXIT at {price}")
