from datetime import datetime, timedelta
from AlgorithmImports import *

class HighOctaneRSISwing(QCAlgorithm):
    """
    Strategy 22: High-Octane RSI Swing
    
    Core Concept:
    - Target highest-alpha tech leaders (NVDA, AMD, TSLA) for signal generation.
    - Entry: When any leader is extremely oversold (RSI2 < 20) during a bull regime (QQQ > 200 SMA).
    - Position: 100% TQQQ to capture the high-beta mean reversion spike.
    - Exit: Fast profit taking on QQQ RSI recovery or structural trend break.
    """
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        
        # High-Beta Signal Stocks
        self.tickers = ["NVDA", "AMD", "TSLA"]
        self.symbols = [self.AddEquity(t, Resolution.Daily).Symbol for t in self.tickers]
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        
        self.rsi2 = {s: self.RSI(s, 2, MovingAverageType.Wilders, Resolution.Daily) for s in self.symbols}
        self.sma200 = self.SMA(self.qqq, 200, Resolution.Daily)
        
        self.SetWarmUp(200, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.AfterMarketOpen("TQQQ", 30), self.Rebalance)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma200.IsReady: return
        
        qqq_price = self.Securities[self.qqq].Price
        sma200_val = self.sma200.Current.Value
        
        # Bull Regime Only
        if qqq_price > sma200_val:
            if not self.Portfolio.Invested:
                # If ANY of our momentum leaders are extremely oversold, go 100% TQQQ
                oversold_leaders = [s for s in self.symbols if self.rsi2[s].Current.Value < 20]
                
                if oversold_leaders:
                    self.SetHoldings(self.tqqq, 1.0)
                    self.Debug(f"OCTANE ENTRY: {oversold_leaders[0].Value} dip buy via TQQQ")
            else:
                # Fast Exit: RSI on QQQ recovers or Trend breaks
                if self.RSI(self.qqq, 2).Current.Value > 70 or qqq_price < sma200_val:
                    self.Liquidate()
        else:
            self.Liquidate()
