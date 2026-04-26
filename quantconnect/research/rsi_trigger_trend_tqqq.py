from datetime import datetime, timedelta
from AlgorithmImports import *


class TQQQRSITriggerTrend(QCAlgorithm):

    def Initialize(self):
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100_000)
        
        self.sym = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        
        # Indicators
        self.rsi = self.RSI(self.sym, 5, MovingAverageType.Wilders, Resolution.Daily)
        self.sma50 = self.SMA(self.sym, 50, Resolution.Daily)
        self.sma200 = self.SMA(self.sym, 200, Resolution.Daily)
        
        self.SetWarmUp(200, Resolution.Daily)
        
        self.Schedule.On(
            self.DateRules.EveryDay(self.sym),
            self.TimeRules.AfterMarketOpen(self.sym, 30),
            self.Rebalance,
        )

    def Rebalance(self):
        if self.IsWarmingUp or not self.rsi.IsReady or not self.sma50.IsReady:
            return

        price = self.Securities[self.sym].Price
        rsi_val = self.rsi.Current.Value
        sma50_val = self.sma50.Current.Value
        sma200_val = self.sma200.Current.Value

        if not self.Portfolio.Invested:
            # ENTRY: Major trend up (SMA200) AND Medium trend up (SMA50) AND Oversold
            if price > sma200_val and price > sma50_val and rsi_val < 30:
                self.SetHoldings(self.sym, 1.0)
                self.Debug(f"ENTRY: RSI Trigger at {price}")
        else:
            # EXIT: RSI Overbought OR Trend Break
            if rsi_val > 70 or price < sma200_val:
                self.Liquidate(self.sym)
                self.Debug(f"EXIT: Profit Taken/Safety at {price}")
