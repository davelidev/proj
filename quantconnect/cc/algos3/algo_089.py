from AlgorithmImports import *

class Algo089(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        
        # Add equity symbols
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        self.rsp = self.AddEquity("RSP", Resolution.Daily).Symbol
        
        # 200-day SMA indicators
        self.sma_spy = self.SMA(self.spy, 200, Resolution.Daily)
        self.sma_rsp = self.SMA(self.rsp, 200, Resolution.Daily)
        
        # Warm up indicators
        self.SetWarmUp(200)
        
    def OnData(self, data):
        if self.IsWarmingUp:
            return
        
        if not (self.sma_spy.IsReady and self.sma_rsp.IsReady):
            return
        
        # Price condition: SPY above its 200-day SMA
        spy_close = self.Securities[self.spy].Close
        price_up = spy_close > self.sma_spy.Current.Value
        
        # Breadth condition: RSP below its 200-day SMA (weakening breadth)
        rsp_close = self.Securities[self.rsp].Close
        breadth_down = rsp_close < self.sma_rsp.Current.Value
        
        # Determine target weights (no leverage, weights ≤ 1)
        if price_up and breadth_down:
            # Breadth divergence: reduce equity exposure
            weight_spy = 0.3
            weight_rsp = 0.1
        else:
            # Normal conditions: full allocation
            weight_spy = 0.5
            weight_rsp = 0.5
        
        # Rebalance portfolio
        self.SetHoldings(self.spy, weight_spy)
        self.SetHoldings(self.rsp, weight_rsp)