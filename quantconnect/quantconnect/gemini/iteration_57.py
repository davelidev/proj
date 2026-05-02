from AlgorithmImports import *

class TechSpyMomentum(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.sma50 = self.SMA(self.tqqq, 50, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), 
                         self.TimeRules.AfterMarketOpen(self.qqq, 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(50)

    def Rebalance(self):
        if not self.sma50.IsReady: return
        
        # 1-month ROC
        hist = self.History([self.qqq, self.spy], 22, Resolution.Daily)
        if hist.empty: return
        
        try:
            q_ret = (hist.loc[self.qqq]['close'][-1] / hist.loc[self.qqq]['close'][0]) - 1
            s_ret = (hist.loc[self.spy]['close'][-1] / hist.loc[self.spy]['close'][0]) - 1
        except:
            return
            
        price_t = self.Securities[self.tqqq].Price
        sma_val = self.sma50.Current.Value
        
        if q_ret > s_ret and price_t > sma_val:
            if not self.Portfolio[self.tqqq].Invested:
                self.SetHoldings(self.tqqq, 1.0)
                self.Liquidate(self.bil)
        else:
            if self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)
