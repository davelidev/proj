from datetime import datetime, timedelta
from AlgorithmImports import *

class TQQQOptimizedSMA(QCAlgorithm):
    def Initialize(self):
        # 12 year backtest
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100000)
        
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        
        # 48/49 SMA Crossover (Optimized parameters from community research)
        self.fast = self.SMA(self.tqqq, 48, Resolution.Daily)
        self.slow = self.SMA(self.tqqq, 49, Resolution.Daily)
        
        self.SetWarmUp(50)

    def OnData(self, data):
        if self.IsWarmingUp or not self.slow.IsReady:
            return
        
        if self.fast.Current.Value > self.slow.Current.Value:
            if not self.Portfolio[self.tqqq].Invested:
                self.SetHoldings(self.tqqq, 1.0)
        else:
            if self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.tqqq)
