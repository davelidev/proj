from datetime import datetime, timedelta
from AlgorithmImports import *

class RotationStrategyV13(QCAlgorithm):
    """
    Rotation V13: Dual Momentum TQQQ / TMF
    Uses classic dual momentum. In a bull market, holds TQQQ.
    In a bear market, holds TMF (3x Treasuries) if bonds are trending up,
    otherwise sits in Cash to avoid the 2022 stock/bond correlated crash.
    """
    def Initialize(self):
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100_000)

        self.Schedule.On(
            self.DateRules.EveryDay("SPY"),
            self.TimeRules.AfterMarketOpen("SPY", 35),
            self.Rebalance,
        )

        tickers = ["SPY", "TLT", "TQQQ", "TMF", "BIL"]
        self.syms = {t: self.AddEquity(t, Resolution.Daily).Symbol for t in tickers}

        self.sma_spy200 = self.SMA(self.syms["SPY"], 200, Resolution.Daily)
        self.sma_tlt200 = self.SMA(self.syms["TLT"], 200, Resolution.Daily)

        self.SetWarmUp(200, Resolution.Daily)

    def _pick(self) -> str:
        spy_price = self.Securities[self.syms["SPY"]].Price
        tlt_price = self.Securities[self.syms["TLT"]].Price

        bull = spy_price > self.sma_spy200.Current.Value
        bonds_bull = tlt_price > self.sma_tlt200.Current.Value

        if bull:
            return "TQQQ"
        else:
            # Bear Market for Stocks
            if bonds_bull:
                # Flight to safety working
                return "TMF"
            else:
                # 2022 scenario: both crashing
                return "BIL"

    def Rebalance(self):
        if (self.IsWarmingUp 
            or not self.sma_spy200.IsReady 
            or not self.sma_tlt200.IsReady):
            return

        pick = self._pick()
        self.Debug(f"[Rebalance] → {pick}")
        
        if not self.Portfolio[self.syms[pick]].Invested:
            self.SetHoldings(self.syms[pick], 1.0, liquidateExistingHoldings=True)

    def OnData(self, data):
        pass
