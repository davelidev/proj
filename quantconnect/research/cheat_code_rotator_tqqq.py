from datetime import datetime, timedelta
from AlgorithmImports import *


class TQQQCheatCodeRotator(QCAlgorithm):
    """
    Strategy 11: Cheat Code Rotator (TQQQ)
    
    Core Concept:
    - Pure application of Kevin Davey's 'Cheat Code' filters.
    - Structural Filter: QQQ > 200 SMA (Bull Regime).
    - Volatility Shield: VIX < 28 (Safe Environment).
    - Entry Trigger: RSI(2) < 30 (Extreme Short-Term Dip).
    - Exit Trigger: RSI(10) > 80 (Overbought Exhaustion).
    """
    def Initialize(self):
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100_000)
        self.SetBenchmark("QQQ")
        
        self.sym = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.vix = self.AddData(CBOE, "VIX").Symbol
        
        # High-Conviction Cheat Code Indicators
        self.sma200 = self.SMA(self.qqq, 200, Resolution.Daily)
        self.rsi2 = self.RSI(self.qqq, 2, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi10 = self.RSI(self.qqq, 10, MovingAverageType.Wilders, Resolution.Daily)
        
        self.SetWarmUp(200, Resolution.Daily)
        
        self.Schedule.On(
            self.DateRules.EveryDay(self.qqq),
            self.TimeRules.AfterMarketOpen(self.qqq, 35),
            self.Rebalance,
        )

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma200.IsReady:
            return

        qqq_price = self.Securities[self.qqq].Price
        vix_val = self.Securities[self.vix].Price
        sma_val = self.sma200.Current.Value
        r2 = self.rsi2.Current.Value
        r10 = self.rsi10.Current.Value

        # CHEAT CODE REGIME: Bull Trend + Safe Volatility
        is_safe_bull = qqq_price > sma_val and vix_val < 28

        if not self.Portfolio.Invested:
            # ENTRY: Bull market dip
            if is_safe_bull and r2 < 30:
                self.SetHoldings(self.sym, 1.0)
                self.Debug(f"CHEAT ENTRY: Bull Dip at {qqq_price}")
        else:
            # EXIT: Overbought exhaustion OR structural trend break OR Vol Panic
            # RSI10 > 80 is a strong profit-taking signal for TQQQ
            if r10 > 80 or qqq_price < sma_val or vix_val > 32:
                self.Liquidate(self.sym)
                self.Debug(f"CHEAT EXIT: Shield/Profit at {qqq_price}")
