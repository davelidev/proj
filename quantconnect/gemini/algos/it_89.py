from AlgorithmImports import *

class DonchianReversion(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.donchian = self.DCH(self.tqqq, 20, 20, Resolution.Daily)
        self.rsi = self.RSI(self.tqqq, 2, MovingAverageType.Wilders, Resolution.Daily)
        
        self.SetWarmUp(20)

    def OnData(self, data):
        if not (self.donchian.IsReady and self.rsi.IsReady): return
        
        price = float(self.Securities[self.tqqq].Price)
        lower = float(self.donchian.LowerBand.Current.Value)
        upper = float(self.donchian.UpperBand.Current.Value)
        rsi_val = float(self.rsi.Current.Value)
        
        if self.IsWarmingUp: return

        if not self.Portfolio[self.tqqq].Invested:
            # Entry: Touch 20-day Low AND RSI2 < 25
            if price <= lower and rsi_val < 25:
                self.SetHoldings(self.tqqq, 1.0)
        else:
            # Exit: Touch 20-day High
            if price >= upper:
                self.Liquidate(self.tqqq)
