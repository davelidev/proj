from AlgorithmImports import *

class MFI14Hyst(QCAlgorithm):
    """MFI(14) > 60 -> 100% TQQQ; MFI < 40 -> cash; 40-60 hold (hysteresis)."""
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.mfi  = self.MFI(self.qqq, 14, Resolution.Daily)
        self.SetWarmUp(252, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq, 45), self.Rebalance)

    def Rebalance(self):
        if self.IsWarmingUp or not self.mfi.IsReady: return
        v = self.mfi.Current.Value
        if v > 60:   self.SetHoldings(self.tqqq, 1.0)
        elif v < 40 and self.Portfolio[self.tqqq].Invested: self.Liquidate(self.tqqq)
