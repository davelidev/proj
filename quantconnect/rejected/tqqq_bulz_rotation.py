from datetime import datetime, timedelta
from AlgorithmImports import *

class TQQQBULZRotation(QCAlgorithm):
    def Initialize(self):
        # 12 year backtest
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100000)

        # Assets
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bulz = self.AddEquity("BULZ", Resolution.Daily).Symbol
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.sma_spy = self.SMA(self.spy, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.MonthStart(self.spy), 
                         self.TimeRules.AfterMarketOpen(self.spy, 35), 
                         self.Rebalance)
        
        self.SetWarmUp(252)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma_spy.IsReady:
            return

        spy_price = self.Securities[self.spy].Price
        is_bull = spy_price > self.sma_spy.Current.Value
        
        if is_bull:
            # Bull Market: Rotation between highest alpha engines
            momentum = {}
            for s in [self.tqqq, self.bulz]:
                if not self.Securities[s].HasData: continue
                hist = self.History(s, 252, Resolution.Daily)
                if not hist.empty:
                    mom = (hist['close'].iloc[-1] / hist['close'].iloc[0]) - 1
                    momentum[s] = mom
            
            if momentum:
                best = max(momentum, key=momentum.get)
                if not self.Portfolio[best].Invested:
                    self.Log(f"Bull Market. Winner: {best.Value}. Allocating.")
                    self.Liquidate()
                    self.SetHoldings(best, 1.0)
        else:
            if not self.Portfolio[self.bil].Invested:
                self.Log("Bear Market. Moving to BIL.")
                self.Liquidate()
                self.SetHoldings(self.bil, 1.0)
