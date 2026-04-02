from datetime import datetime, timedelta
from AlgorithmImports import *

class RotationStrategyV17(QCAlgorithm):
    """
    Rotation V17: The QLD Downshift
    Builds on the successful V9 "Sniper" framework (67% CAGR / 44% DD).
    During bull market pullbacks (TQQQ < 20 SMA), instead of downshifting all the way 
    to 1x QQQ, it downshifts to 2x QLD. This retains more of the compounding growth 
    while still reducing the brutal volatility drag of 3x TQQQ during chop.
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

        tickers = ["SPY", "QQQ", "TQQQ", "QLD", "SQQQ", "BIL"]
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
            if tqqq_below_20sma:
                if panic:
                    return "TQQQ" # Catch the bounce
                return "QLD" # 2x leverage to survive the chop
            return "TQQQ"
            
        else:
            # BEAR MARKET
            if panic:
                return "TQQQ"
            if tqqq_below_20sma:
                return "SQQQ"
            return "BIL" # Bear market rally, wait in cash

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma_spy200.IsReady or not self.rsi2_qqq.IsReady:
            return

        pick = self._pick()
        if not self.Portfolio[self.syms[pick]].Invested:
            self.Debug(f"[Rebalance] → Switching to {pick}")
            self.SetHoldings(self.syms[pick], 1.0, liquidateExistingHoldings=True)

    def OnData(self, data):
        pass
