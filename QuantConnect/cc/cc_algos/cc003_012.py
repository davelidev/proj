from AlgorithmImports import *

class StochasticCross(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil  = self.AddEquity("BIL",  Resolution.Daily).Symbol

        # Stochastic(14, 3, 3) — Lane's classic slow stochastic
        self.sto = self.STO(self.qqq, 14, 3, 3, Resolution.Daily)

        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Rebalance)
        self.SetWarmUp(30, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sto.IsReady:
            return
        k = self.sto.StochK.Current.Value
        d = self.sto.StochD.Current.Value

        # %K crosses above %D from oversold → long
        if k > d and k < 80:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil)
                self.SetHoldings(self.tqqq, 1.0)
        elif k < d and k > 20:
            if not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
