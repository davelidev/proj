from datetime import datetime, timedelta
from AlgorithmImports import *

class AlphaTitanSwing(QCAlgorithm):
    def Initialize(self):
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100_000)
        self.SetBenchmark("QQQ")
        
        # Core Assets
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        # High-Growth Indicators
        self.sma200 = self.SMA(self.qqq, 200, Resolution.Daily)
        self.rsi2 = self.RSI(self.qqq, 2, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi10 = self.RSI(self.tqqq, 10, MovingAverageType.Wilders, Resolution.Daily)
        
        self.SetWarmUp(200, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.AfterMarketOpen("TQQQ", 35), self.Rebalance)
        self.stop_loss_pct = 0.065 # Aggressive 6.5% hard stop

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma200.IsReady: return

        qqq_price = self.Securities[self.qqq].Price
        sma_val = self.sma200.Current.Value
        r2 = self.rsi2.Current.Value
        r10 = self.rsi10.Current.Value

        # THE TITAN SHIELD: Bull Market Trend
        if qqq_price > sma_val:
            if not self.Portfolio[self.tqqq].Invested:
                # ENTRY on high-conviction dip
                if r2 < 20:
                    self.SetHoldings(self.tqqq, 1.0)
            else:
                # PROFIT PROTECTION BUFFER: 
                # De-leverage to 50% if overextended, stay at 100% otherwise
                if r10 > 75:
                    self.SetHoldings(self.tqqq, 0.5)
                # Hard Profit Lock
                if r10 > 85:
                    self.Liquidate(self.tqqq)
        else:
            # SAFETY: Move to BIL
            self.Liquidate()

    def OnOrderEvent(self, orderEvent):
        # Attach hard stop on full entry
        if orderEvent.Status == OrderStatus.Filled and orderEvent.Direction == OrderDirection.Buy:
            stop_price = orderEvent.FillPrice * (1 - self.stop_loss_pct)
            self.StopMarketOrder(self.tqqq, -orderEvent.FillQuantity, stop_price)
