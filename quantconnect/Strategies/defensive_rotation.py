from datetime import datetime, timedelta
from AlgorithmImports import *

class RotationStrategyV3(QCAlgorithm):
    """
    Rotation Strategy V3: Enhanced Macro Rotation
    
    Core Concept:
    - Bull Market: Hold TQQQ.
    - Bear Market (SPY < SMA200):
        - If TQQQ > SMA20 (Sideways/Bear Rally): Hold IEF (Bonds).
        - If TQQQ <= SMA20 (Active Downtrend): Hold SQQQ.
    - Sharp Crash (RSI < 30): Hold BIL (Cash) as a defensive gate.
    """
    def Initialize(self):
        # 12 year backtest to match other strategies
        
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.Schedule.On(
            self.DateRules.EveryDay("QQQ"),
            self.TimeRules.AfterMarketOpen("QQQ", 35),
            self.Rebalance,
        )

        # Tickers required for V3 logic
        tickers = ["SPY", "QQQ", "TQQQ", "SQQQ", "BIL", "IEF"]
        self.syms = {t: self.AddEquity(t, Resolution.Daily).Symbol for t in tickers}

        # Indicators
        self.rsi10 = {
            t: self.RSI(self.syms[t], 10, MovingAverageType.Wilders, Resolution.Daily)
            for t in ["SPY", "QQQ"]
        }
        self.sma_spy200 = self.SMA(self.syms["SPY"], 200, Resolution.Daily)
        self.sma_tqqq20 = self.SMA(self.syms["TQQQ"], 20, Resolution.Daily)

        self.SetWarmUp(200, Resolution.Daily)

    def _pick(self) -> str:
        spy_price = self.Securities[self.syms["SPY"]].Price
        tqqq_price = self.Securities[self.syms["TQQQ"]].Price
        
        # Sharp Crash Gate (RSI < 30) -> Rotate to BIL (Cash)
        # We check both SPY and QQQ RSI for maximum safety
        if self.rsi10["QQQ"].Current.Value < 30 or self.rsi10["SPY"].Current.Value < 30:
            return "BIL"

        # Long Term Regime Filter
        bull_market = spy_price > self.sma_spy200.Current.Value

        if bull_market:
            # Bull Market: Default to high-beta tech
            return "TQQQ"
        else:
            # Bear Market: Check for Sideways vs. Active Downtrend
            sideways_or_rally = tqqq_price > self.sma_tqqq20.Current.Value
            
            if sideways_or_rally:
                # Sideways Bear Market -> Rotate to IEF (Bonds)
                return "IEF"
            else:
                # Active Bear Market Downtrend -> Rotate to SQQQ (Short)
                return "SQQQ"

    def Rebalance(self):
        if (self.IsWarmingUp 
            or not self.sma_spy200.IsReady 
            or not self.sma_tqqq20.IsReady 
            or not all(i.IsReady for i in self.rsi10.values())):
            return

        pick = self._pick()
        self.Debug(f"[Rebalance] {self.Time} \u2192 {pick}")
        self.SetHoldings(self.syms[pick], 1.0, liquidateExistingHoldings=True)

    def OnData(self, data):
        pass
