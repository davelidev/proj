from AlgorithmImports import *

class VortexTrend(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil  = self.AddEquity("BIL",  Resolution.Daily).Symbol

        # Manual Vortex Indicator (period 14): sums of |H-L_prev| and |L-H_prev| over TR.
        self.period = 14
        self.prev_bar = None  # (high, low, close)
        self.vm_plus  = RollingWindow[float](self.period)
        self.vm_minus = RollingWindow[float](self.period)
        self.tr_win   = RollingWindow[float](self.period)

        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Rebalance)
        self.SetWarmUp(25, Resolution.Daily)

    def _ingest_bar(self, bar):
        if self.prev_bar is None:
            self.prev_bar = bar
            return
        ph, pl, pc = self.prev_bar
        h, l, c    = bar
        vmp = abs(h - pl)
        vmm = abs(l - ph)
        tr  = max(h - l, abs(h - pc), abs(l - pc))
        self.vm_plus.Add(vmp)
        self.vm_minus.Add(vmm)
        self.tr_win.Add(tr)
        self.prev_bar = bar

    def OnData(self, data):
        if self.qqq in data.Bars:
            b = data.Bars[self.qqq]
            self._ingest_bar((b.High, b.Low, b.Close))

    def Rebalance(self):
        if self.IsWarmingUp or not (self.vm_plus.IsReady and self.vm_minus.IsReady and self.tr_win.IsReady):
            return
        sum_tr = sum(self.tr_win[i] for i in range(self.period))
        if sum_tr <= 0:
            return
        vi_plus  = sum(self.vm_plus[i]  for i in range(self.period)) / sum_tr
        vi_minus = sum(self.vm_minus[i] for i in range(self.period)) / sum_tr

        if vi_plus > vi_minus and vi_plus > 1.0:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil)
                self.SetHoldings(self.tqqq, 1.0)
        elif vi_minus > vi_plus and vi_minus > 1.0:
            if not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)
