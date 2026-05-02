from AlgorithmImports import *

class VWAPReversion(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        
        # We'll use a manual rolling VWAP calculation as the Daily built-in is Intraday only
        self.window = RollingWindow[TradeBar](20)
        
        self.SetWarmUp(20)

    def OnData(self, data):
        if not data.Bars.ContainsKey(self.tqqq): return
        
        bar = data.Bars[self.tqqq]
        self.window.Add(bar)
        
        if self.IsWarmingUp or not self.window.IsReady: return

        # 1. Calculate 20-day VWAP manually
        # VWAP = sum(TypicalPrice * Volume) / sum(Volume)
        sum_pv = 0
        sum_v = 0
        for b in self.window:
            typical_price = (b.High + b.Low + b.Close) / 3.0
            sum_pv += typical_price * b.Volume
            sum_v += b.Volume
        
        vwap = sum_pv / sum_v if sum_v > 0 else 0
        price = float(bar.Close)
        
        if vwap == 0: return
        
        # 2. Trading Logic
        if not self.Portfolio[self.tqqq].Invested:
            # Entry: Price is 10% or more below 20-day VWAP
            if (price / vwap) < 0.90:
                self.SetHoldings(self.tqqq, 1.0)
        else:
            # Exit: Price recovers to VWAP
            if price >= vwap:
                self.Liquidate(self.tqqq)
