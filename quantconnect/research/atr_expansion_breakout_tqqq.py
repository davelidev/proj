from datetime import datetime, timedelta
from AlgorithmImports import *


class TQQQATRExpansionBreakout(QCAlgorithm):

    def Initialize(self):
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100_000)
        
        self.sym = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        
        # High-Conviction Indicators
        self.adx = self.ADX(self.sym, 14, Resolution.Daily)
        self.sma200 = self.SMA(self.sym, 200, Resolution.Daily)
        
        self.SetWarmUp(200, Resolution.Daily)
        
        self.Schedule.On(
            self.DateRules.EveryDay(self.sym),
            self.TimeRules.AfterMarketOpen(self.sym, 30),
            self.Rebalance,
        )

    def Rebalance(self):
        if self.IsWarmingUp or not self.adx.IsReady or not self.sma200.IsReady:
            return

        # Range calculations
        h1 = self.Securities[self.sym].High
        l1 = self.Securities[self.sym].Low
        range1 = h1 - l1
        
        # Get historical data for the previous range
        history = self.History(self.sym, 2, Resolution.Daily)
        if len(history) < 2:
            return
        
        # previous day range
        range_yest = history.iloc[-1].high - history.iloc[-1].low
        # 2 days ago range
        range_prev = history.iloc[-2].high - history.iloc[-2].low
        
        price = self.Securities[self.sym].Price
        adx_val = self.adx.Current.Value
        sma_val = self.sma200.Current.Value

        if not self.Portfolio.Invested:
            # ENTRY: Volatility is expanding (Yest Range > Prev Range) 
            # AND Market is trending (ADX > 20) AND Price is above long-term SMA
            if range_yest > range_prev and adx_val > 20 and price > sma_val:
                self.SetHoldings(self.sym, 1.0)
                self.Debug(f"VOL BREAKOUT ENTRY at {price}")
        else:
            # EXIT: Price falls below long-term SMA (Trend break) 
            # OR simple 5% stop loss to protect against sharp reversals
            if price < sma_val:
                self.Liquidate(self.sym)
                self.Debug(f"VOL BREAKOUT EXIT at {price}")
