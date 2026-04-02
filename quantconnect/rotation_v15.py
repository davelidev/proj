from datetime import datetime, timedelta
from AlgorithmImports import *

class RotationStrategyV15(QCAlgorithm):
    """
    Rotation V15: The Holy Grail Attempt
    Combines the aggressive 100% TQQQ exposure of V1 during Bull Markets 
    with the highly protective Cash/SQQQ/TQQQ rotation of V9 during Bear Markets.
    """
    def Initialize(self):
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100_000)

        self.Schedule.On(
            self.DateRules.EveryDay("QQQ"),
            self.TimeRules.AfterMarketOpen("QQQ", 35),
            self.Rebalance,
        )

        tickers = ["SPY", "QQQ", "TQQQ", "SQQQ", "BIL"]
        self.syms = {t: self.AddEquity(t, Resolution.Daily).Symbol for t in tickers}

        self.rsi2_qqq = self.RSI(self.syms["QQQ"], 2, MovingAverageType.Wilders, Resolution.Daily)
        self.sma_spy200 = self.SMA(self.syms["SPY"],  200, Resolution.Daily)
        self.sma_tqqq20 = self.SMA(self.syms["TQQQ"], 20,  Resolution.Daily)

        self.SetWarmUp(200, Resolution.Daily)

    def _pick(self) -> str:
        spy_price  = self.Securities[self.syms["SPY"]].Price
        tqqq_price = self.Securities[self.syms["TQQQ"]].Price

        bull = spy_price > self.sma_spy200.Current.Value
        tqqq_below_20sma = tqqq_price < self.sma_tqqq20.Current.Value
        panic = self.rsi2_qqq.Current.Value < 20

        if bull:
            # Aggressive Bull Market: 100% TQQQ.
            # We don't downshift here because 3x leverage recovers fast if SPY > 200 SMA.
            return "TQQQ"
            
        else:
            # Bear Market Defense
            if panic:
                # V-shaped bounce play
                return "TQQQ"
            
            if tqqq_below_20sma:
                # Smooth downtrend
                return "SQQQ"

            # Bear market rally (above 20 SMA but below 200 SMA)
            # Sit in cash to avoid getting crushed when the rally fails
            return "BIL"

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma_spy200.IsReady or not self.rsi2_qqq.IsReady:
            return

        pick = self._pick()
        if not self.Portfolio[self.syms[pick]].Invested:
            self.Debug(f"[Rebalance] → Switching to {pick} (RSI: {self.rsi2_qqq.Current.Value:.2f})")
            self.SetHoldings(self.syms[pick], 1.0, liquidateExistingHoldings=True)

    def OnData(self, data):
        pass
