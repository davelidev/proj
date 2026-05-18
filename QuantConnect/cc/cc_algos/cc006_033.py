from AlgorithmImports import *

class CrabelStretch(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.lo10=self.MIN(self.qqq,10,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(30, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp or not self.lo10.IsReady: return
        h=self.History(self.qqq, 11, Resolution.Daily)
        if h.empty or len(h)<11: return
        opens=[float(x) for x in h["open"].values]
        lows=[float(x) for x in h["low"].values]
        # Crabel stretch: smaller of (open-low) over recent days
        smaller=[min(opens[i]-lows[i], 0.0) for i in range(10)]
        # Use median of (open-low) absolute values
        v=sorted(abs(opens[i]-lows[i]) for i in range(10))
        stretch = v[5]
        prev_close = float(h["close"].iloc[-2])
        long_trigger = prev_close + stretch
        price = self.Securities[self.qqq].Price
        if not self.Portfolio[self.tqqq].Invested:
            if price > long_trigger:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq, 1.0)
        else:
            if price <= self.lo10.Current.Value*1.001:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil, 1.0)

    def OnData(self, data): pass
