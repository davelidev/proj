from AlgorithmImports import *

class Algo079(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.symbols = {
            "AAPL": self.AddEquity("AAPL", Resolution.Daily).Symbol,
            "MSFT": self.AddEquity("MSFT", Resolution.Daily).Symbol,
            "NVDA": self.AddEquity("NVDA", Resolution.Daily).Symbol,
            "GOOGL": self.AddEquity("GOOGL", Resolution.Daily).Symbol,
            "AMZN": self.AddEquity("AMZN", Resolution.Daily).Symbol,
        }
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol

        self.atrs = {ticker: self.ATR(sym, 14) for ticker, sym in self.symbols.items()}
        self.sma200 = self.SMA(self.qqq, 200)

        self.month = -1
        self.SetWarmUp(200, Resolution.Daily)

    def OnData(self, data: Slice):
        if self.IsWarmingMode:
            return

        if not self.sma200.IsReady:
            return

        for atr in self.atrs.values():
            if not atr.IsReady:
                return

        if self.Time.month == self.month:
            return
        self.month = self.Time.month

        qqq_price = self.Securities[self.qqq].Close
        if qqq_price == 0:
            return

        if qqq_price < self.sma200.Current.Value:
            for ticker in self.symbols:
                self.Liquidate(self.symbols[ticker])
            return

        inv_atrs = []
        for ticker, sym in self.symbols.items():
            atr_val = self.atrs[ticker].Current.Value
            if atr_val <= 0:
                return
            inv_atrs.append(1.0 / atr_val)

        total_inv = sum(inv_atrs)
        weights = [inv / total_inv for inv in inv_atrs]

        for (ticker, sym), w in zip(self.symbols.items(), weights):
            self.SetHoldings(sym, w)
