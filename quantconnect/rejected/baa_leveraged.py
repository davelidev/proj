from datetime import datetime, timedelta
from AlgorithmImports import *
import numpy as np

class BAALeveraged(QCAlgorithm):
    def Initialize(self):
        # 12 year backtest
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100000)
        
        # BAA-G Canary Universe (Crash sensors)
        self.canary = ["SPY", "VEU", "BND", "DBC"]
        
        # BAA-G Offensive: TQQQ/SOXL for high CAGR
        self.offensive = ["TQQQ", "SOXL"]
        
        # BAA-G Defensive: TIP, TLT, BIL
        self.defensive = ["TIP", "TLT", "BIL"]
        
        self.symbols = {}
        for ticker in list(set(self.canary + self.offensive + self.defensive)):
            self.symbols[ticker] = self.AddEquity(ticker, Resolution.Daily).Symbol

        # Rebalance on the last trading day of the month
        self.Schedule.On(self.DateRules.MonthEnd("SPY"), 
                         self.TimeRules.BeforeMarketClose("SPY", 10), 
                         self.Rebalance)
        
        self.SetWarmUp(253)

    def Rebalance(self):
        if self.IsWarmingUp:
            return

        # 1. Calculate Momentum Scores for Canary Universe
        canary_positive = True
        for ticker in self.canary:
            score = self.GetMomentumScore(self.symbols[ticker])
            if score <= 0:
                canary_positive = False
                break
        
        # 2. Determine Regime
        # BAA-G logic: "Safe" only if ALL canary assets are positive.
        if canary_positive:
            # Risk-On: Split between top offensive assets
            self.Log("BAA Regime: SAFE. Allocating to Offensive LETFs.")
            self.LiquidateOtherThan(self.offensive)
            for ticker in self.offensive:
                self.SetHoldings(self.symbols[ticker], 1.0 / len(self.offensive))
        else:
            # Risk-Off: Pick the best defensive asset (Relative Momentum)
            best_defensive = self.GetBestRelativeMomentum(self.defensive)
            self.Log(f"BAA Regime: CRASH. Allocating to {best_defensive}.")
            self.LiquidateOtherThan([best_defensive])
            self.SetHoldings(self.symbols[best_defensive], 1.0)

    def LiquidateOtherThan(self, tickers):
        target_symbols = [self.symbols[t] for t in tickers]
        for holdings in self.Portfolio.Values:
            if holdings.Invested and holdings.Symbol not in target_symbols:
                self.Liquidate(holdings.Symbol)

    def GetMomentumScore(self, symbol):
        """13612W Momentum Score: 12*r1 + 4*r3 + 2*r6 + r12"""
        history = self.History(symbol, 253, Resolution.Daily)
        if history.empty or len(history) < 253:
            return 0
        
        prices = history['close'].values
        p0 = prices[-1]
        r1 = (p0 / prices[-22]) - 1
        r3 = (p0 / prices[-64]) - 1
        r6 = (p0 / prices[-127]) - 1
        r12 = (p0 / prices[-253]) - 1
        
        return (12 * r1) + (4 * r3) + (2 * r6) + r12

    def GetBestRelativeMomentum(self, tickers):
        """Pick asset with highest price relative to its 12-month SMA"""
        scores = {}
        for ticker in tickers:
            symbol = self.symbols[ticker]
            history = self.History(symbol, 252, Resolution.Daily)
            if not history.empty:
                scores[ticker] = history['close'].iloc[-1] / history['close'].mean()
        
        if not scores: return "BIL"
        return max(scores, key=scores.get)
