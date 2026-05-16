from AlgorithmImports import *

class DI_Cross(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.adx=self.ADX(self.qqq, 14, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily)
        self.last_di_sign=None

    def Rebalance(self):
        if self.IsWarmingUp or not self.adx.IsReady: return
        h=self.History(self.qqq, 200, Resolution.Daily)
        if h.empty or len(h)<200: return
        c=[float(x) for x in h["close"].values]; med=sorted(c)[100]
        in_trend=self.Securities[self.qqq].Price>med
        p=self.adx.PositiveDirectionalIndex.Current.Value; n=self.adx.NegativeDirectionalIndex.Current.Value
        cur_sign = 1 if p > n else -1
        if self.last_di_sign is None:
            self.last_di_sign = cur_sign
            return
        if cur_sign == 1 and self.last_di_sign == -1 and in_trend:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq,1.0)
        elif cur_sign == -1 and self.last_di_sign == 1:
            if not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil,1.0)
        self.last_di_sign = cur_sign

    def OnData(self, data): pass
