from datetime import datetime, timedelta
from AlgorithmImports import *

class RotationStrategyV18(QCAlgorithm):
    """
    Rotation V18: The Holy Grail Refined
    Builds on the incredibly successful 'a_5.py' (169% CAGR, 47% DD), but removes 
    the toxic UVXY allocation during overbought bull markets, replacing it with Cash (BIL) 
    to further reduce drawdown and volatility decay.
    """
    def Initialize(self):
        
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.Schedule.On(
            self.DateRules.EveryDay("TQQQ"),
            self.TimeRules.AfterMarketOpen("TQQQ", 35), # Avoid opening bell chop
            self.Rebalance,
        )

        tickers = ["TQQQ", "TECL", "SOXL", "SQQQ", "BIL"]
        self.syms = {t: self.AddEquity(t, Resolution.Daily).Symbol for t in tickers}

        self.rsi_tqqq = self.RSI(self.syms["TQQQ"], 10, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi_soxl = self.RSI(self.syms["SOXL"], 10, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi_sqqq = self.RSI(self.syms["SQQQ"], 10, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi_bil  = self.RSI(self.syms["BIL"],  10, MovingAverageType.Wilders, Resolution.Daily)

        self.sma_200 = self.SMA(self.syms["TQQQ"], 200, Resolution.Daily)
        self.sma_20  = self.SMA(self.syms["TQQQ"], 20, Resolution.Daily)

        self.SetWarmUp(200, Resolution.Daily)

    def _pick(self) -> str:
        tqqq_price = self.Securities[self.syms["TQQQ"]].Price

        if tqqq_price > self.sma_200.Current.Value:
            # Bull Market
            if self.rsi_tqqq.Current.Value > 79:
                # Extreme overbought - secure profits to cash instead of toxic UVXY
                return "BIL"
            return "TQQQ"
        else:
            # Bear Market
            if self.rsi_tqqq.Current.Value < 31:
                return "TECL" # Tech bounce
            if self.rsi_soxl.Current.Value < 30:
                return "SOXL" # Semi bounce
            
            if tqqq_price < self.sma_20.Current.Value:
                # Downtrend: choose between shorting (SQQQ) or hiding in cash (BIL)
                # based on short-term momentum (RSI)
                if self.rsi_sqqq.Current.Value > self.rsi_bil.Current.Value:
                    return "SQQQ"
                return "BIL"
            
            # Bear market rally: hold the momentum
            return "TQQQ"

    def Rebalance(self):
        if (self.IsWarmingUp 
            or not self.sma_200.IsReady 
            or not self.sma_20.IsReady 
            or not self.rsi_tqqq.IsReady 
            or not self.rsi_soxl.IsReady 
            or not self.rsi_sqqq.IsReady):
            return

        pick = self._pick()
        if not self.Portfolio[self.syms[pick]].Invested:
            self.Debug(f"[Rebalance] → Switching to {pick}")
            self.SetHoldings(self.syms[pick], 1.0, liquidateExistingHoldings=True)

    def OnData(self, data):
        pass
