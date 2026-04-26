from datetime import datetime, timedelta
from AlgorithmImports import *


class TQQQDynamicCompounding(QCAlgorithm):
    """
    Strategy 8: TQQQ Dynamic Compounding
    
    Core Concept:
    - Varies leverage based on market regime and volatility.
    - Bull Regime (Price > 200 SMA): 
        - 100% leverage on RSI(2) < 30 (Dip Buy).
        - 20% leverage on RSI(10) > 80 (Profit Protection).
    - Bear Regime (Price < 200 SMA): 
        - 0% exposure (Cash).
    """
    def Initialize(self):
        
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        
        self.sym = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        
        # Growth and Safety Indicators
        self.rsi2 = self.RSI(self.sym, 2, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi10 = self.RSI(self.sym, 10, MovingAverageType.Wilders, Resolution.Daily)
        self.sma200 = self.SMA(self.sym, 200, Resolution.Daily)
        
        self.SetWarmUp(200, Resolution.Daily)
        
        # Dynamic adjustment: check daily
        self.Schedule.On(
            self.DateRules.EveryDay(self.sym),
            self.TimeRules.AfterMarketOpen(self.sym, 30),
            self.Rebalance,
        )

    def Rebalance(self):
        if self.IsWarmingUp or not self.rsi2.IsReady or not self.sma200.IsReady:
            return

        price = self.Securities[self.sym].Price
        sma_val = self.sma200.Current.Value
        r2 = self.rsi2.Current.Value
        r10 = self.rsi10.Current.Value

        # BULL MARKET MODE (Growth Focus)
        if price > sma_val:
            if r10 > 80:
                # De-leverage on extreme overbought to protect capital
                self.SetHoldings(self.sym, 0.2)
                self.Debug(f"BULL: De-leveraging at {price}")
            elif r2 < 30:
                # Full leverage on dips to drive compounding
                self.SetHoldings(self.sym, 1.0)
                self.Debug(f"BULL: Re-leveraging at {price}")
            elif not self.Portfolio.Invested:
                # Default bull entry if we missed the dip
                self.SetHoldings(self.sym, 0.5)
        
        # BEAR MARKET MODE (Survival Focus)
        else:
            if self.Portfolio.Invested:
                self.Liquidate(self.sym)
                self.Debug(f"BEAR: Exiting to Cash at {price}")
