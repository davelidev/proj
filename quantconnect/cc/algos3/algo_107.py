from AlgorithmImports import *

class Algo107(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.symbol = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.atr = self.ATR(self.symbol, 14, Resolution.Daily)

        self.trailingStop = None
        self.entryDone = False

    def OnData(self, data):
        if not data.ContainsKey(self.symbol) or data[self.symbol] is None:
            return

        if not self.atr.IsReady:
            return

        current_price = data[self.symbol].Close
        atr_value = self.atr.Current.Value

        # Entry on the first day ATR is ready
        if not self.entryDone:
            self.SetHoldings(self.symbol, 1.0)
            self.entryDone = True
            self.trailingStop = current_price - 2.0 * atr_value
            self.Debug(f"Initial entry at {current_price}, stop set to {self.trailingStop}")
            return

        # If we are still invested, manage the trailing stop
        if self.Portfolio[self.symbol].Invested:
            new_stop = current_price - 2.0 * atr_value
            if new_stop > self.trailingStop:
                self.trailingStop = new_stop

            if current_price < self.trailingStop:
                self.Liquidate(self.symbol)
                self.Debug(f"Trailing stop hit at {current_price}, stop was {self.trailingStop}")
        # else: do nothing after exit