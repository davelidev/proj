from AlgorithmImports import *

class VolumeIntensityReversion(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.vol_sma = self.SMA(self.tqqq, 20, Resolution.Daily, Field.Volume)
        self.price_min = self.MIN(self.tqqq, 5, Resolution.Daily)
        self.price_sma = self.SMA(self.tqqq, 5, Resolution.Daily)
        
        self.SetWarmUp(20)

    def OnData(self, data):
        if not (self.vol_sma.IsReady and self.price_min.IsReady): return
        if not data.Bars.ContainsKey(self.tqqq): return
        
        bar = data.Bars[self.tqqq]
        price = float(bar.Close)
        volume = float(bar.Volume)
        avg_vol = float(self.vol_sma.Current.Value)
        min_price = float(self.price_min.Current.Value)
        
        # Volume Intensity = Current Volume / Avg Volume
        intensity = volume / avg_vol if avg_vol > 0 else 1.0
        
        if self.IsWarmingUp: return

        if not self.Portfolio[self.tqqq].Invested:
            # Entry: 5-day Low AND Volume Spike (Intensity > 2.0)
            if price <= min_price and intensity > 2.0:
                self.SetHoldings(self.tqqq, 1.0)
        else:
            # Exit: Price recovers to 5-day SMA
            if price >= self.price_sma.Current.Value:
                self.Liquidate(self.tqqq)
