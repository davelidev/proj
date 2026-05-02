from AlgorithmImports import *

class OBVDivergence(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.obv = self.OBV(self.tqqq, Resolution.Daily)
        
        # Windows to track lows
        self.price_window = RollingWindow[float](20)
        self.obv_window = RollingWindow[float](20)
        
        self.SetWarmUp(20)

    def OnData(self, data):
        if not self.obv.IsReady: return
        
        price = float(self.Securities[self.tqqq].Price)
        obv_val = float(self.obv.Current.Value)
        
        self.price_window.Add(price)
        self.obv_window.Add(obv_val)
        
        if self.IsWarmingUp or not (self.price_window.IsReady and self.obv_window.IsReady): return

        if not self.Portfolio[self.tqqq].Invested:
            # Entry: OBV Divergence (Lower Low in Price, Higher Low in OBV)
            # Find min price in window
            min_price = min(self.price_window)
            min_obv = min(self.obv_window)
            
            # Simple divergence check
            if price == min_price and obv_val > min_obv:
                self.SetHoldings(self.tqqq, 1.0)
        else:
            # Exit: Price recovers to 20-day high
            if price >= max(self.price_window):
                self.Liquidate(self.tqqq)
