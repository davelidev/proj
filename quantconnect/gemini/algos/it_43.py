from AlgorithmImports import *

class MarketBreadthTrend(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.rsi_spy = self.RSI(self.spy, 14, MovingAverageType.Wilders, Resolution.Daily)
        self.sma_spy = self.SMA(self.spy, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.spy), 
                         self.TimeRules.AfterMarketOpen(self.spy, 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if not (self.rsi_spy.IsReady and self.sma_spy.IsReady): return
        
        rsi_val = self.rsi_spy.Current.Value
        price_spy = self.Securities[self.spy].Price
        sma_val = self.sma_spy.Current.Value
        
        # Logic: Healthy Breadth (RSI between 50 and 75) AND macro bull (Price > SMA)
        if 50 < rsi_val < 75 and price_spy > sma_val:
            if not self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] HEALTHY BREADTH. RSI: {rsi_val:.2f}. Entering TQQQ.")
                self.SetHoldings(self.tqqq, 1.0)
                self.Liquidate(self.bil)
        else:
            if self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] BREADTH WEAK OR OVEREXTENDED. RSI: {rsi_val:.2f}. Exiting.")
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
