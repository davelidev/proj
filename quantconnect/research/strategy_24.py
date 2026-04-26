from datetime import datetime, timedelta
from AlgorithmImports import *

class ChampionDipRotation(QCAlgorithm):
    def Initialize(self):
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100_000)
        
        # High-Alpha Signal Pair
        self.tickers = ["NVDA", "SOXL"]
        self.symbols = [self.AddEquity(t, Resolution.Daily).Symbol for t in self.tickers]
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        
        self.rsi2 = {s: self.RSI(s, 2, MovingAverageType.Wilders, Resolution.Daily) for s in self.symbols}
        self.sma200 = self.SMA(self.qqq, 200, Resolution.Daily)
        
        self.SetWarmUp(200, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.AfterMarketOpen("QQQ", 30), self.Rebalance)
        
        self.stop_loss_pct = 0.075 # Hard 7.5% stop for high leverage protection

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma200.IsReady: return
        
        qqq_price = self.Securities[self.qqq].Price
        sma200_val = self.sma200.Current.Value
        
        # BULL REGIME ONLY
        if qqq_price > sma200_val:
            if not self.Portfolio.Invested:
                # Find extreme oversold signal
                triggered = [s for s in self.symbols if self.rsi2[s].Current.Value < 15]
                
                if triggered:
                    # Target SOXL for the highest bounce potential
                    target = self.symbols[1] if triggered[0].Value == "NVDA" else triggered[0]
                    self.SetHoldings(target, 1.0)
                    self.Debug(f"CHAMPION ENTRY: {target.Value} at {self.Securities[target].Price}")
            else:
                # FAST EXIT: RSI recovers on QQQ
                if self.RSI(self.qqq, 2).Current.Value > 65:
                    self.Liquidate()
        else:
            self.Liquidate()

    def OnOrderEvent(self, orderEvent):
        # Attach hard stop on entry
        if orderEvent.Status == OrderStatus.Filled and orderEvent.Direction == OrderDirection.Buy:
            stop_price = orderEvent.FillPrice * (1 - self.stop_loss_pct)
            self.StopMarketOrder(orderEvent.Symbol, -orderEvent.FillQuantity, stop_price)
