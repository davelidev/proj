from AlgorithmImports import *

class Algo072(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.nvda = self.AddEquity("NVDA", Resolution.Daily).Symbol

        self.sma = self.SMA(self.nvda, 150, Resolution.Daily)
        self.atr = self.ATR(self.nvda, 14, MovingAverageType.Simple, Resolution.Daily)

        self.SetWarmUp(200, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay(self.nvda),
            self.TimeRules.AfterMarketOpen(self.nvda, 1),
            self.Rebalance
        )

        self.peak_price = 0.0

    def Rebalance(self):
        if self.IsWarmingUp:
            return
        if not self.sma.IsReady or not self.atr.IsReady:
            return

        nvda = self.nvda
        close = self.Securities[nvda].Close
        sma_val = self.sma.Current.Value
        atr_val = self.atr.Current.Value
        high = self.Securities[nvda].High
        low = self.Securities[nvda].Low

        ibs = (close - low) / (high - low) if high > low else 0.5
        in_trend = close > sma_val

        if in_trend:
            if not self.Portfolio.Invested:
                self.SetHoldings(nvda, 1.0)
                self.peak_price = close
            else:
                if self.peak_price == 0.0:
                    self.peak_price = close
                self.peak_price = max(self.peak_price, close)
                if close < self.peak_price - 5.0 * atr_val:
                    self.Liquidate(nvda)
                    self.peak_price = 0.0
        else:
            if self.Portfolio.Invested and self.peak_price > 0.0:
                self.Liquidate(nvda)
                self.peak_price = 0.0

            if not self.Portfolio.Invested and ibs < 0.05:
                self.SetHoldings(nvda, 1.0)
            elif self.Portfolio.Invested and ibs > 0.70:
                self.Liquidate(nvda)
