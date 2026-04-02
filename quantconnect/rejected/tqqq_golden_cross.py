from datetime import datetime, timedelta
from AlgorithmImports import *

class TQQQGoldenCross(QCAlgorithm):
    def Initialize(self):
        # 12 year backtest
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        
        # 50/200 Golden Cross
        self.fast = self.SMA(self.tqqq, 50, Resolution.Daily)
        self.slow = self.SMA(self.tqqq, 200, Resolution.Daily)
        
        self.SetWarmUp(200)

    def OnData(self, data):
        if self.IsWarmingUp or not self.slow.IsReady:
            return

        # Simple Golden Cross Logic
        if self.fast.Current.Value > self.slow.Current.Value:
            if not self.Portfolio[self.tqqq].Invested:
                self.Log(f"Golden Cross! Buying TQQQ.")
                self.SetHoldings(self.tqqq, 1.0)
        else:
            if self.Portfolio[self.tqqq].Invested:
                self.Log(f"Death Cross! Liquidating.")
                self.Liquidate()
