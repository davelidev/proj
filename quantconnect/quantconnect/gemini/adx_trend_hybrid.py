from AlgorithmImports import *

class ADXTrend(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.sma = self.SMA(self.qqq, 200, Resolution.Daily)
        self.adx = self.ADX(self.qqq, 14, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), 
                         self.TimeRules.AfterMarketOpen(self.qqq, 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if not (self.sma.IsReady and self.adx.IsReady): return
        
        price_q = self.Securities[self.qqq].Price
        sma_val = self.sma.Current.Value
        adx_val = self.adx.Current.Value
        
        # Signal: Trend UP AND Trend is STRONG (ADX > 25)
        if price_q > sma_val and adx_val > 25:
            if not self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] STRONG TREND ON. ADX: {adx_val:.2f}. Entering TQQQ.")
                self.Liquidate(self.bil)
                self.SetHoldings(self.tqqq, 1.0)
        else:
            if self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] TREND WEAK OR DOWN. ADX: {adx_val:.2f}. Exiting.")
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
