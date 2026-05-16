from AlgorithmImports import *

class ADXDirectional(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil  = self.AddEquity("BIL",  Resolution.Daily).Symbol

        self.adx = self.ADX(self.qqq, 14, Resolution.Daily)

        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Rebalance)
        self.SetWarmUp(35, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp or not self.adx.IsReady:
            return
        adx_val = self.adx.Current.Value
        pdi     = self.adx.PositiveDirectionalIndex.Current.Value
        ndi     = self.adx.NegativeDirectionalIndex.Current.Value

        # Wilder DI system: trade with the dominant DI when ADX confirms trend strength
        if adx_val > 20 and pdi > ndi:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil)
                self.SetHoldings(self.tqqq, 1.0)
        elif adx_val > 20 and ndi > pdi:
            if not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
