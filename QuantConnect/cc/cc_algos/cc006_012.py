from AlgorithmImports import *

class HeikinAshiTrend(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(40, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq, 20, Resolution.Daily)
        if h.empty or len(h)<20: return
        opens=[float(x) for x in h["open"].values]
        highs=[float(x) for x in h["high"].values]
        lows=[float(x) for x in h["low"].values]
        closes=[float(x) for x in h["close"].values]
        # compute HA bars
        ha_o=[(opens[0]+closes[0])/2]
        ha_c=[(opens[0]+highs[0]+lows[0]+closes[0])/4]
        for i in range(1,len(closes)):
            cur_o=(ha_o[-1]+ha_c[-1])/2
            cur_c=(opens[i]+highs[i]+lows[i]+closes[i])/4
            ha_o.append(cur_o); ha_c.append(cur_c)
        # 3 consecutive green HA
        green = all(ha_c[-i] > ha_o[-i] for i in range(1,4))
        red = all(ha_c[-i] < ha_o[-i] for i in range(1,4))
        if green:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq,1.0)
        elif red:
            if not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil,1.0)

    def OnData(self, data): pass
