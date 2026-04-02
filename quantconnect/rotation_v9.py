from datetime import datetime, timedelta
from AlgorithmImports import *

class RotationStrategyV9(QCAlgorithm):
    """
    Rotation V9: The Sniper
    Fixes the "Falling Knife" problem in V1/V8 by replacing the 10-day RSI panic 
    trigger with an extremely fast 2-day RSI trigger (like the Champion strategy),
    preventing us from holding 3x leverage during sustained crashes while still
    catching the massive V-shaped recoveries.
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

        # FAST 2-day RSI for sniper entries
        self.rsi2_qqq = self.RSI(self.syms["QQQ"], 2, MovingAverageType.Wilders, Resolution.Daily)
        
        self.sma_spy200 = self.SMA(self.syms["SPY"],  200, Resolution.Daily)
        self.sma_tqqq20 = self.SMA(self.syms["TQQQ"], 20,  Resolution.Daily)

        self.SetWarmUp(200, Resolution.Daily)

    def _pick(self) -> str:
        spy_price  = self.Securities[self.syms["SPY"]].Price
        tqqq_price = self.Securities[self.syms["TQQQ"]].Price

        bull = spy_price > self.sma_spy200.Current.Value
        tqqq_below_20sma = tqqq_price < self.sma_tqqq20.Current.Value
        
        # Sniper Trigger: Extreme 2-day panic (like rsi_rebalance.py)
        panic = self.rsi2_qqq.Current.Value < 20

        if bull:
            if tqqq_below_20sma:
                # Catch the flash crash
                if panic:
                    return "TQQQ"
                # Otherwise, it's just a pullback, sit in 1x QQQ to limit drawdown
                return "QQQ"
            return "TQQQ"
            
        else:
            # BEAR MARKET
            if panic:
                # V-shaped bounce play
                return "TQQQ"
            
            if tqqq_below_20sma:
                # Smooth downtrend
                return "SQQQ"

            # Bear market rally (above 20 SMA but below 200 SMA)
            # V1 held TQQQ here which caused the massive 56% DD when the rally failed.
            # We will sit in cash to protect capital.
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
