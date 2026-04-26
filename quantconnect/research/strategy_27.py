from datetime import datetime, timedelta
from AlgorithmImports import *

class ChampionSectorShield(QCAlgorithm):
    def Initialize(self):
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100_000)
        self.SetBenchmark("QQQ")
        
        # Performance Pair
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.soxl = self.AddEquity("SOXL", Resolution.Daily).Symbol
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        
        # Structural Indicators
        self.vix = self.AddData(CBOE, "VIX").Symbol
        self.vix3m = self.AddData(CBOE, "VIX3M").Symbol
        self.sma200_spy = self.SMA(self.spy, 200, Resolution.Daily)
        self.mom_tqqq = self.MOMP(self.tqqq, 21, Resolution.Daily)
        self.mom_soxl = self.MOMP(self.soxl, 21, Resolution.Daily)
        
        self.SetWarmUp(200, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.AfterMarketOpen("TQQQ", 35), self.Rebalance)
        self.stop_loss_pct = 0.10

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma200_spy.IsReady: return
        if not (self.Securities.ContainsKey(self.vix) and self.Securities.ContainsKey(self.vix3m)): return

        spy_price = self.Securities[self.spy].Price
        vix_ratio = self.Securities[self.vix].Price / self.Securities[self.vix3m].Price if self.Securities[self.vix3m].Price != 0 else 1.0
        sma_val = self.sma200_spy.Current.Value

        # THE CHAMPION SHIELD: Bull Market + Structural Contango
        is_safe = spy_price > sma_val and vix_ratio < 1.05

        if is_safe:
            # ROTATION: strongest 1-month momentum
            if self.mom_soxl.Current.Value > self.mom_tqqq.Current.Value:
                self.SetHoldings(self.soxl, 1.0)
            else:
                self.SetHoldings(self.tqqq, 1.0)
        else:
            # SAFETY: Move to BIL/Cash
            self.Liquidate()

    def OnOrderEvent(self, orderEvent):
        # Attach hard stop on entry
        if orderEvent.Status == OrderStatus.Filled and orderEvent.Direction == OrderDirection.Buy:
            stop_price = orderEvent.FillPrice * (1 - self.stop_loss_pct)
            self.StopMarketOrder(orderEvent.Symbol, -orderEvent.FillQuantity, stop_price)
