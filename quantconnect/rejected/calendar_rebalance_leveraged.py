from datetime import datetime, timedelta
from AlgorithmImports import *

class CalendarRebalanceLeveraged(QCAlgorithm):
    def Initialize(self):
        # 12 year backtest
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100000)

        # High-beta basket
        self.assets = ["TQQQ", "SOXL", "TMF"]
        self.symbols = [self.AddEquity(t, Resolution.Daily).Symbol for t in self.assets]
        
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        self.sma_spy = self.SMA(self.spy, 200, Resolution.Daily)
        
        # Rebalance weekly on Monday
        self.Schedule.On(self.DateRules.Every(DayOfWeek.Monday), 
                         self.TimeRules.AfterMarketOpen(self.assets[0], 35), 
                         self.Rebalance)
        
        self.SetWarmUp(200)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma_spy.IsReady:
            return

        spy_price = self.Securities[self.spy].Price
        is_bull = spy_price > self.sma_spy.Current.Value
        
        if is_bull:
            # Bull Market: Allocate to best momentum asset over last 5 days
            momentum = {}
            for s in self.symbols:
                hist = self.History(s, 5, Resolution.Daily)
                if not hist.empty:
                    mom = (hist['close'].iloc[-1] / hist['close'].iloc[0]) - 1
                    momentum[s] = mom
            
            if momentum:
                best_s = max(momentum, key=momentum.get)
                if not self.Portfolio[best_s].Invested:
                    self.Log(f"Weekly Bull: {best_s.Value} 5d Mom {momentum[best_s]:.2%}. Rebalancing.")
                    self.Liquidate()
                    self.SetHoldings(best_s, 1.0)
        else:
            # Bear Market: Stay in TMF or Cash
            if not self.Portfolio[self.symbols[2]].Invested: # TMF
                self.Log("Weekly Bear: Moving to TMF.")
                self.Liquidate()
                self.SetHoldings(self.symbols[2], 1.0)
