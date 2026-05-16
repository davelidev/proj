from AlgorithmImports import *

class OBVSlope(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        # On-Balance Volume rolling window
        self.obv_win=RollingWindow[float](21)
        self.cum_obv=0.0
        self.prev_close=None
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(40, Resolution.Daily)

    def OnData(self, data):
        if self.qqq in data.Bars:
            b=data.Bars[self.qqq]
            if self.prev_close is not None:
                sign = 1 if b.Close>self.prev_close else (-1 if b.Close<self.prev_close else 0)
                self.cum_obv += sign * b.Volume
            self.obv_win.Add(self.cum_obv)
            self.prev_close=b.Close

    def Rebalance(self):
        if self.IsWarmingUp or not self.obv_win.IsReady: return
        obv_now=self.obv_win[0]; obv_20=self.obv_win[20]
        bull = obv_now > obv_20  # OBV rising = accumulation
        if bull:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq,1.0)
        else:
            if not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil,1.0)

    def OnData(self, data): pass
