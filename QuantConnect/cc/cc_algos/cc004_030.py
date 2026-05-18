from AlgorithmImports import *

class ThreeState_MomentumAccel_Top1Defense(QCAlgorithm):
    """3-state momentum acceleration + Top-1 mega-cap defense:
       BULL (ROC>0 AND ROC accel AND QQQ>D200mid) → 100% TQQQ
       MIXED → 50% TQQQ + 50% Top-1
       BEAR → 100% Top-1
    """
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelection, self.FineSelection)

        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol

        self.roc   = self.ROC(self.qqq, 20, Resolution.Daily)
        self.roc_window = RollingWindow[float](11)
        self.hi200 = self.MAX(self.qqq, 200, Resolution.Daily)
        self.lo200 = self.MIN(self.qqq, 200, Resolution.Daily)
        self.roc.Updated += self._roc_updated
        self.SetWarmUp(230, Resolution.Daily)

        self.symbols = []
        self.state = None
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Rebalance)

    def _roc_updated(self, _, pt):
        self.roc_window.Add(pt.Value)

    def CoarseSelection(self, coarse):
        return [x.Symbol for x in sorted(coarse, key=lambda x: x.DollarVolume, reverse=True)[:100]]

    def FineSelection(self, fine):
        self.symbols = [x.Symbol for x in sorted(fine, key=lambda x: x.MarketCap, reverse=True)[:1]]
        return self.symbols

    def Rebalance(self):
        if self.IsWarmingUp or not (self.roc.IsReady and self.roc_window.IsReady and self.hi200.IsReady and self.lo200.IsReady):
            return
        if not self.symbols: return
        top1 = self.symbols[0]
        roc_now = self.roc_window[0]
        roc_10  = self.roc_window[10]
        mid = (self.hi200.Current.Value + self.lo200.Current.Value) / 2.0
        m_up    = roc_now > 0
        m_accel = roc_now > roc_10
        d_bull  = self.Securities[self.qqq].Price > mid

        if m_up and m_accel and d_bull:
            ns, wt, wm = "BULL", 1.0, 0.0
        elif (m_up or d_bull):
            ns, wt, wm = "MIXED", 0.5, 0.5
        else:
            ns, wt, wm = "BEAR", 0.0, 1.0

        if ns != self.state:
            for sym in list(self.Securities.Keys):
                if sym in (self.qqq, self.tqqq, top1): continue
                if self.Portfolio[sym].Invested: self.Liquidate(sym)
            self.SetHoldings(self.tqqq, wt)
            self.SetHoldings(top1, wm)
            self.state = ns

    def OnData(self, data): pass
