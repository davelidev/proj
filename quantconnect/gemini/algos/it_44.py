from AlgorithmImports import *

class TNASafeRotation(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.iwm = self.AddEquity("IWM", Resolution.Daily).Symbol
        self.tna = self.AddEquity("TNA", Resolution.Daily).Symbol
        self.vix = self.AddData(CBOE, "VIX", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.sma = self.SMA(self.iwm, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.iwm), 
                         self.TimeRules.AfterMarketOpen(self.iwm, 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if not (self.sma.IsReady and self.Securities.ContainsKey(self.vix)): return
        
        price_i = self.Securities[self.iwm].Price
        sma_val = self.sma.Current.Value
        vix_val = self.Securities[self.vix].Price
        
        # Signal: Small Cap Trend UP AND Volatility LOW
        if price_i > sma_val and vix_val < 20:
            if not self.Portfolio[self.tna].Invested:
                self.Log(f"[{self.Time}] SIGNAL ON: TNA Trend UP + VIX {vix_val:.2f}. Entering.")
                self.SetHoldings(self.tna, 1.0)
                self.Liquidate(self.bil)
        else:
            if self.Portfolio[self.tna].Invested:
                self.Log(f"[{self.Time}] SIGNAL OFF. Trend DOWN or VIX {vix_val:.2f}. Exiting.")
                self.Liquidate(self.tna)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
