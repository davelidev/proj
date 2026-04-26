from datetime import datetime, timedelta
from AlgorithmImports import *


class TQQQFridayHighest(QCAlgorithm):

    def Initialize(self):
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100_000)
        
        self.sym = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        
        # Indicator for highest close of last 20 days
        self.high = self.MAX(self.sym, 20, Resolution.Daily)
        
        self.SetWarmUp(20, Resolution.Daily)
        
        # Check every day but logic only triggers on Monday/Wednesday
        self.Schedule.On(
            self.DateRules.EveryDay(self.sym),
            self.TimeRules.AfterMarketOpen(self.sym, 30),
            self.Rebalance,
        )
        
        self.trigger_on_friday = False

    def Rebalance(self):
        if self.IsWarmingUp or not self.high.IsReady:
            return

        price = self.Securities[self.sym].Price
        day = self.Time.weekday() # 0 is Monday, 4 is Friday

        # On Friday, check if it's the highest close
        if day == 4:
            if price >= self.high.Current.Value:
                self.trigger_on_friday = True
            else:
                self.trigger_on_friday = False

        # On Monday, enter if triggered on Friday
        if day == 0 and self.trigger_on_friday:
            if not self.Portfolio.Invested:
                self.SetHoldings(self.sym, 1.0)
                self.Debug(f"ENTRY: Monday follow-through at {price}")
                self.trigger_on_friday = False

        # On Wednesday, exit (Fixed bar exit concept)
        if day == 2:
            if self.Portfolio.Invested:
                self.Liquidate(self.sym)
                self.Debug(f"EXIT: Mid-week profit take at {price}")
