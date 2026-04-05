from AlgorithmImports import *

class RotationStrategy(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2015, 1, 1)
        self.SetCash(100_000)

        self.Schedule.On(
            self.DateRules.EveryDay("QQQ"),
            self.TimeRules.AfterMarketOpen("QQQ", 35),
            self.Rebalance,
        )

        # Subscribe only to tickers actively used in the strategy
        tickers = ["SPY", "QQQ", "TQQQ", "SQQQ"]
        self.syms = {t: self.AddEquity(t, Resolution.Daily).Symbol for t in tickers}

        self.rsi10 = {
            t: self.RSI(self.syms[t], 10, MovingAverageType.Wilders, Resolution.Daily)
            for t in tickers
        }
        self.sma_spy200 = self.SMA(self.syms["SPY"],  200, Resolution.Daily)
        self.sma_tqqq20 = self.SMA(self.syms["TQQQ"], 20,  Resolution.Daily)

        self.SetWarmUp(200, Resolution.Daily)

    def _pick(self) -> str:
        rsi10 = self.rsi10
        spy_price  = self.Securities[self.syms["SPY"]].Price
        tqqq_price = self.Securities[self.syms["TQQQ"]].Price

        sharp_crash = (rsi10["QQQ"].Current.Value < 30 or rsi10["SPY"].Current.Value < 30)
        short_term_bear = tqqq_price < self.sma_tqqq20.Current.Value
        long_term_bear = spy_price < self.sma_spy200.Current.Value

        # Ride the trend down during long term and short term bear market, but not a sharp crash
        if long_term_bear and short_term_bear and not sharp_crash:
            return "SQQQ"

        # Default to buy
        return "TQQQ"

    def Rebalance(self):
        if (self.IsWarmingUp 
            or not self.sma_spy200.IsReady 
            or not self.sma_tqqq20.IsReady 
            or not all(i.IsReady for i in self.rsi10.values())):
            return

        pick = self._pick()
        self.Debug(f"[Rebalance] → {pick}")
        self.SetHoldings(self.syms[pick], 1.0, liquidateExistingHoldings=True)

    def OnData(self, data):
        pass
