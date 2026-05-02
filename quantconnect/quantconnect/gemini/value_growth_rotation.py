from AlgorithmImports import *

class ValueGrowthRotation(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.iwd = self.AddEquity("IWD", Resolution.Daily).Symbol # Value
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.sma_qqq = self.SMA(self.qqq, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), 
                         self.TimeRules.AfterMarketOpen(self.qqq, 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(64)

    def Rebalance(self):
        if self.Time.weekday() != 0: return # Mondays
        if self.IsWarmingUp or not self.sma_qqq.IsReady: return
        
        hist = self.History([self.qqq, self.iwd], 64, Resolution.Daily)
        if hist.empty: return
        
        try:
            q_prices = hist.loc[self.qqq]['close'].values
            v_prices = hist.loc[self.iwd]['close'].values
            q_roc = (q_prices[-1] / q_prices[0]) - 1
            v_roc = (v_prices[-1] / v_prices[0]) - 1
        except:
            return
            
        price_q = self.Securities[self.qqq].Price
        sma_val = self.sma_qqq.Current.Value
        
        # Logic: Growth > Value AND Trend UP
        if q_roc > v_roc and price_q > sma_val:
            if not self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] GROWTH LEADERSHIP. Entering TQQQ.")
                self.SetHoldings(self.tqqq, 1.0)
                self.Liquidate(self.bil)
        else:
            if self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] VALUE LEADERSHIP OR BEAR. Exiting.")
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
