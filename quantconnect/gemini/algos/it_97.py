from AlgorithmImports import *

class SafeHavenTrend(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.ugl = self.AddEquity("UGL", Resolution.Daily).Symbol # 2x Gold
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        
        self.sma = self.SMA(self.qqq, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay("QQQ"), 
                         self.TimeRules.AfterMarketOpen("QQQ", 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if not self.sma.IsReady: return
        
        price_q = float(self.Securities[self.qqq].Price)
        sma_val = float(self.sma.Current.Value)
        
        if price_q > sma_val:
            # Bullish Regime: TQQQ
            if not self.Portfolio[self.tqqq].Invested:
                self.SetHoldings(self.tqqq, 1.0)
                self.Liquidate(self.ugl)
                self.Liquidate(self.bil)
        else:
            # Bearish Regime: Dynamic Safe Haven (Gold vs Cash)
            hist = self.History([self.ugl, self.bil], 22, Resolution.Daily)
            if hist.empty: return
            
            try:
                g_ret = (hist.loc[self.ugl]['close'][-1] / hist.loc[self.ugl]['close'][0]) - 1
                b_ret = (hist.loc[self.bil]['close'][-1] / hist.loc[self.bil]['close'][0]) - 1
            except:
                g_ret = -1.0
                b_ret = 0
                
            if g_ret > b_ret:
                # Gold is the best haven
                if not self.Portfolio[self.ugl].Invested:
                    self.Liquidate(self.tqqq)
                    self.SetHoldings(self.ugl, 1.0)
                    self.Liquidate(self.bil)
            else:
                # Cash is the best haven
                if not self.Portfolio[self.bil].Invested:
                    self.Liquidate(self.tqqq)
                    self.Liquidate(self.ugl)
                    self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
