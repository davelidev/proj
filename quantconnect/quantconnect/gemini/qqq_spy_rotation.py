from AlgorithmImports import *

class TechRelativeStrength(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.sma = self.SMA(self.qqq, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), 
                         self.TimeRules.AfterMarketOpen(self.qqq, 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if not self.sma.IsReady: return
        
        # 3-month (63 trading days) Momentum
        hist = self.History([self.qqq, self.spy], 64, Resolution.Daily)
        if hist.empty: return
        
        try:
            q_prices = hist.loc[self.qqq]['close'].values
            s_prices = hist.loc[self.spy]['close'].values
            q_mom = (q_prices[-1] / q_prices[0]) - 1
            s_mom = (s_prices[-1] / s_prices[0]) - 1
        except:
            return
            
        price_q = self.Securities[self.qqq].Price
        sma_val = self.sma.Current.Value
        
        # Logic: Tech is stronger than SPY AND Trend is UP
        if q_mom > s_mom and price_q > sma_val:
            if not self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] TECH LEADERSHIP (Q:{q_mom:.1%} > S:{s_mom:.1%}). Entering TQQQ.")
                self.SetHoldings(self.tqqq, 1.0)
        else:
            if self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] TECH WEAKNESS OR BEAR. Exiting to Cash.")
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
