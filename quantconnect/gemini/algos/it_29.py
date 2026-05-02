from AlgorithmImports import *

class TQQQTNARotation(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.iwm = self.AddEquity("IWM", Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.tna = self.AddEquity("TNA", Resolution.Daily).Symbol
        
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), 
                         self.TimeRules.AfterMarketOpen(self.qqq, 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(22)

    def Rebalance(self):
        if self.Time.weekday() != 0: return # Mondays
        if self.IsWarmingUp: return
        
        hist = self.History([self.qqq, self.iwm], 22, Resolution.Daily)
        if hist.empty: return
        
        try:
            q_prices = hist.loc[self.qqq]['close'].values
            i_prices = hist.loc[self.iwm]['close'].values
            q_roc = (q_prices[-1] / q_prices[0]) - 1
            i_roc = (i_prices[-1] / i_prices[0]) - 1
        except:
            return
            
        if q_roc > i_roc:
            if not self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] TECH LEADERSHIP. Rotating to TQQQ.")
                self.Liquidate(self.tna)
                self.SetHoldings(self.tqqq, 1.0)
        else:
            if not self.Portfolio[self.tna].Invested:
                self.Log(f"[{self.Time}] SMALL CAP LEADERSHIP. Rotating to TNA.")
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.tna, 1.0)

    def OnData(self, data):
        pass
