from AlgorithmImports import *
import numpy as np

class CorrelationHedge(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.tlt = self.AddEquity("TLT", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.sma = self.SMA(self.qqq, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), 
                         self.TimeRules.AfterMarketOpen(self.qqq, 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if not self.sma.IsReady: return
        
        price_q = self.Securities[self.qqq].Price
        sma_val = self.sma.Current.Value
        
        if price_q > sma_val:
            # Bullish Regime
            if not self.Portfolio[self.tqqq].Invested:
                self.SetHoldings(self.tqqq, 1.0)
                self.Liquidate(self.tlt)
                self.Liquidate(self.bil)
        else:
            # Bearish Regime: Calculate Correlation to choose hedge
            hist = self.History([self.qqq, self.tlt], 22, Resolution.Daily)
            if hist.empty: return
            
            try:
                q_ret = hist.loc[self.qqq]['close'].pct_change().dropna()
                t_ret = hist.loc[self.tlt]['close'].pct_change().dropna()
                correlation = q_ret.corr(t_ret)
            except:
                correlation = 1.0 # Default to cash if calc fails
                
            if correlation < 0:
                # Bonds are hedging tech: Hold TLT
                if not self.Portfolio[self.tlt].Invested:
                    self.Liquidate(self.tqqq)
                    self.SetHoldings(self.tlt, 1.0)
                    self.Liquidate(self.bil)
            else:
                # Bonds are moving with tech: Hold Cash
                if not self.Portfolio[self.bil].Invested:
                    self.Liquidate(self.tqqq)
                    self.Liquidate(self.tlt)
                    self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
