from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class MFI14HystSub(BaseSubAlgo):
    """
    Entry: QQQ MFI(14)>60 → 100% TQQQ. Hold when MFI between 40–60.
    Exit: MFI<40.
    """

    def initialize(self):
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Minute).Symbol
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Minute).Symbol
        self.mfi  = MoneyFlowIndex(14)


    def update_targets(self):
        # Get today's QQQ TradeBar proxy
        bar = self.get_daily_bar(self.qqq)
        if bar is None:
            return False
        self.mfi.Update(bar)

        if self.algo.IsWarmingUp:
            return False

        if not self.mfi.IsReady:
            return False

        mfi_value = self.mfi.Current.Value
        if mfi_value > 60:
            self.targets = {self.tqqq: 1.0}
        elif mfi_value < 40:
            self.targets = {}
        # else: 40 ≤ MFI ≤ 60 → hold current position


MFI14HystAlgo = _make_standalone(MFI14HystSub)
