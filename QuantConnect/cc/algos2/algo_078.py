from AlgorithmImports import *
from QuantConnect.Data.Market import TradeBar


class Algo078(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        tqqq = self.AddEquity("TQQQ", Resolution.Daily)
        tqqq.SetDataNormalization(DataNormalizationMode.Adjusted)

        self.macd = self.MACD("TQQQ", 12, 26, 9, MovingAverageType.Exponential)
        self.macd.Updated += self.OnMACDUpdated

        self.invested = False

    def OnMACDUpdated(self, sender, args):
        pass

    def OnData(self, data: TradeBar):
        if not self.macd.IsReady:
            return
        if not self._in_daily_schedule_window():
            return

        macd_line = self.macd.Current.Value
        signal_line = self.macd.Signal.Current.Value

        if macd_line > signal_line and not self.invested:
            self.SetHoldings("TQQQ", 1.0)
            self.invested = True
        elif macd_line < signal_line and self.invested:
            self.Liquidate("TQQQ")
            self.invested = False

    def _in_daily_schedule_window(self) -> bool:
        now = self.Time
        if now.hour == 0 and now.minute == 0:
            return True
        return False
