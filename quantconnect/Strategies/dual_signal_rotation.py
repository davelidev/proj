from datetime import datetime, timedelta
from AlgorithmImports import *

class DualSignalRotation(QCAlgorithm):
    """
    Strategy 9: Dual Signal Rotation
    
    Core Concept:
    - Combines Trend (SMA) and Mean Reversion (RSI) for entries.
    - Bull Regime (TQQQ > SMA200): 
        - Buy TQQQ if TQQQ > SMA20 OR RSI(2) < 20.
    - Bear Regime (TQQQ < SMA200): 
        - Buy SQQQ if TQQQ < SMA20 OR RSI(2) > 80.
    - Else: Cash.
    """
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tickers = ["SPY", "QQQ", "TQQQ", "SQQQ"]
        self.syms = {t: self.AddEquity(t, Resolution.Daily).Symbol for t in self.tickers}

        # Indicators
        self.rsi2 = self.RSI(self.syms["TQQQ"], 2, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi10 = {
            t: self.RSI(self.syms[t], 10, MovingAverageType.Wilders, Resolution.Daily)
            for t in ["SPY", "QQQ"]
        }
        self.sma200 = self.SMA(self.syms["TQQQ"], 200, Resolution.Daily)
        self.sma20 = self.SMA(self.syms["TQQQ"], 20, Resolution.Daily)

        self.SetWarmUp(200, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay("TQQQ"),
            self.TimeRules.AfterMarketOpen("TQQQ", 35),
            self.Rebalance,
        )

    def _pick(self) -> str:
        price = self.Securities[self.syms["TQQQ"]].Price
        s20 = self.sma20.Current.Value
        s200 = self.sma200.Current.Value
        r2 = self.rsi2.Current.Value
        
        bull = price > s200
        
        if bull:
            if price > s20 or r2 < 20:
                return "TQQQ"
        else:
            if price < s20 or r2 > 80:
                return "SQQQ"
                
        return None

    def Rebalance(self):
        if (self.IsWarmingUp 
            or not self.sma200.IsReady 
            or not self.sma20.IsReady 
            or not self.rsi2.IsReady
            or not all(i.IsReady for i in self.rsi10.values())):
            return

        pick = self._pick()
        if pick is None:
            self.Liquidate()
        else:
            self.SetHoldings(self.syms[pick], 1.0, liquidateExistingHoldings=True)
