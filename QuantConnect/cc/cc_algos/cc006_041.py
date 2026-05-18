from AlgorithmImports import *

class WilliamsVIXFix(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.hi22=self.MAX(self.qqq, 22, Resolution.Daily)
        self.aroon=self.AROON(self.qqq, 25, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(35, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp or not (self.hi22.IsReady and self.aroon.IsReady): return
        # Williams VIX Fix: (highest_close_22 - low_today) / highest_close_22 × 100
        price=self.Securities[self.qqq].Price
        wvf=(self.hi22.Current.Value - price)/self.hi22.Current.Value*100
        regime_bull = self.aroon.AroonUp.Current.Value > self.aroon.AroonDown.Current.Value
        # high WVF = oversold; buy when WVF > 8 (panic level) AND regime still bullish
        if not self.Portfolio[self.tqqq].Invested:
            if wvf > 8 and regime_bull:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq, 1.0)
        else:
            if wvf < 2:  # vol contracted; take profit
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil, 1.0)

    def OnData(self, data): pass
