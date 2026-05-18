from datetime import datetime, timedelta
from AlgorithmImports import *

class DefensiveRotation(QCAlgorithm):
    """
    Defensive Rotation: Tactical rotation strategy using cash gates and 
    inverse positions to protect capital during high-volatility regimes 
    and bear markets.
    
    Core Concept:
    - Bull Market (TQQQ > SMA200): Hold TQQQ.
    - Bear Market (TQQQ < SMA200):
        - If TQQQ > SMA20 (Sideways/Bear Rally): Hold Cash.
        - If TQQQ <= SMA20 (Active Downtrend): Hold SQQQ.
    - Sharp Crash (RSI < 30): Hold Cash as a defensive gate.
    """
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        # Tickers for logic and trading
        self.tickers = ["SPY", "QQQ", "TQQQ", "SQQQ"]
        self.syms = {t: self.AddEquity(t, Resolution.Daily).Symbol for t in self.tickers}

        # Indicators
        self.rsi10 = {
            t: self.RSI(self.syms[t], 10, MovingAverageType.Wilders, Resolution.Daily)
            for t in ["SPY", "QQQ"]
        }
        self.sma_tqqq200 = self.SMA(self.syms["TQQQ"], 200, Resolution.Daily)
        self.sma_tqqq20 = self.SMA(self.syms["TQQQ"], 20, Resolution.Daily)

        self.SetWarmUp(200, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay("TQQQ"),
            self.TimeRules.AfterMarketOpen("TQQQ", 35),
            self.Rebalance,
        )

        # Indicators
        self.rsi2 = self.RSI(self.syms["TQQQ"], 2, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi10 = {
            t: self.RSI(self.syms[t], 10, MovingAverageType.Wilders, Resolution.Daily)
            for t in ["SPY", "QQQ"]
        }
        self.sma_tqqq200 = self.SMA(self.syms["TQQQ"], 200, Resolution.Daily)
        self.sma_tqqq20 = self.SMA(self.syms["TQQQ"], 20, Resolution.Daily)

        self.SetWarmUp(200, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay("TQQQ"),
            self.TimeRules.AfterMarketOpen("TQQQ", 35),
            self.Rebalance,
        )

    def _pick(self) -> str:
        tqqq_price = self.Securities[self.syms["TQQQ"]].Price
        sma20 = self.sma_tqqq20.Current.Value
        sma200 = self.sma_tqqq200.Current.Value
        r2 = self.rsi2.Current.Value
        r10 = self.rsi10["QQQ"].Current.Value
        
        # Sharp Crash Gate (RSI10 < 30) -> Rotate to Cash
        if r10 < 30 or self.rsi10["SPY"].Current.Value < 30:
            return None

        # Long Term Regime Filter
        bull_market = tqqq_price > sma200
        bear_market = tqqq_price <= sma200

        # Logic: 
        if bull_market:
            # Buy TQQQ if trending up OR deep RSI(2) oversold bounce
            if tqqq_price > sma20 or r2 < 20:
                return "TQQQ"
        elif bear_market:
            # Buy SQQQ if trending down OR RSI(2) overbought exhaustion
            if tqqq_price < sma20 or r2 > 80:
                return "SQQQ"
                
        return None

    def Rebalance(self):
        if (self.IsWarmingUp 
            or not self.sma_tqqq200.IsReady 
            or not self.sma_tqqq20.IsReady 
            or not self.rsi2.IsReady
            or not all(i.IsReady for i in self.rsi10.values())):
            return

        pick = self._pick()
        self.Debug(f"[Rebalance] {self.Time} -> {pick}")
        
        if pick is None:
            self.Liquidate()
        else:
            self.SetHoldings(self.syms[pick], 1.0, liquidateExistingHoldings=True)
