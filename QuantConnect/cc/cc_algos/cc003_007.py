from AlgorithmImports import *

class Aroon25ChandelierExit(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil  = self.AddEquity("BIL",  Resolution.Daily).Symbol

        self.aroon  = self.AROON(self.qqq, 25, Resolution.Daily)
        self.atr    = self.ATR(self.qqq, 22, MovingAverageType.Wilders, Resolution.Daily)
        self.high22 = self.MAX(self.qqq, 22, Resolution.Daily)

        self.trail_stop = None  # highest-seen Chandelier stop while long

        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Rebalance)
        self.SetWarmUp(35, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp or not (self.aroon.IsReady and self.atr.IsReady and self.high22.IsReady):
            return
        up    = self.aroon.AroonUp.Current.Value
        dn    = self.aroon.AroonDown.Current.Value
        price = self.Securities[self.qqq].Price
        ch_stop = self.high22.Current.Value - 3.0 * self.atr.Current.Value

        long_tqqq = self.Portfolio[self.tqqq].Invested

        if long_tqqq:
            # update trailing stop upward only
            self.trail_stop = ch_stop if self.trail_stop is None else max(self.trail_stop, ch_stop)
            # exit on Chandelier break OR Aroon bearish flip
            if price < self.trail_stop or (dn > 70 and dn > up):
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)
                self.trail_stop = None
        else:
            # entry: Aroon bullish
            if up > 70 and up > dn:
                self.Liquidate(self.bil)
                self.SetHoldings(self.tqqq, 1.0)
                self.trail_stop = ch_stop

    def OnData(self, data):
        pass
