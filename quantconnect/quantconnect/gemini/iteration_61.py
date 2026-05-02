from AlgorithmImports import *

class EMAStretchReversion(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.ema = self.EMA(self.tqqq, 50, Resolution.Daily)
        
        self.SetWarmUp(50)

    def OnData(self, data):
        if not self.ema.IsReady: return
        
        price = float(self.Securities[self.tqqq].Price)
        ema_val = float(self.ema.Current.Value)
        
        # Stretch = (Price - EMA) / EMA
        stretch = (price - ema_val) / ema_val if ema_val > 0 else 0
        
        if self.IsWarmingUp: return

        if not self.Portfolio[self.tqqq].Invested:
            # Entry: Price is 15% or more below its 50 EMA
            if stretch < -0.15:
                self.SetHoldings(self.tqqq, 1.0)
        else:
            # Exit: Price reverts to EMA (stretch >= 0)
            if stretch >= 0:
                self.Liquidate(self.tqqq)
