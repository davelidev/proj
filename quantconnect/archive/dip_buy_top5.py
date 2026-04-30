from datetime import datetime, timedelta
from AlgorithmImports import *

class Top5TechDynamicCompounding(QCAlgorithm):
    """
    Strategy 10: Top 5 Tech Dynamic Compounding
    
    Core Concept:
    - Applies Strategy 7 logic to the top 5 tech stocks by market cap.
    - Bull Regime (Price > 200 SMA): 
        - 100% leverage (split) on RSI(2) < 30 (Dip Buy).
        - 20% leverage (split) on RSI(10) > 80 (Profit Protection).
        - 50% leverage (split) as base bull exposure.
    - Bear Regime (Price < 200 SMA): 
        - 0% exposure (Cash).
    """
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        
        self.UniverseSettings.Resolution = Resolution.Daily
        self.Settings.AutomaticIndicatorWarmUp = True
        
        self._universe = self.AddUniverse(self._select)
        
        # rebalance daily
        self.Schedule.On(
            self.DateRules.EveryDay("SPY"),
            self.TimeRules.AfterMarketOpen("SPY", 30),
            self.Rebalance,
        )

    def _select(self, fundamental):
        filtered = [
            f for f in fundamental
            if (f.HasFundamentalData and 
                f.AssetClassification.MorningstarSectorCode == MorningstarSectorCode.Technology)
        ]
        return [f.Symbol for f in sorted(filtered, key=lambda f: f.MarketCap)[-5:]] 

    def OnSecuritiesChanged(self, changes):
        for security in changes.AddedSecurities:
            security.rsi2 = self.RSI(security.Symbol, 2, MovingAverageType.Wilders, Resolution.Daily)
            security.rsi10 = self.RSI(security.Symbol, 10, MovingAverageType.Wilders, Resolution.Daily)
            security.sma200 = self.SMA(security.Symbol, 200, Resolution.Daily)
            
        for security in changes.RemovedSecurities:
            self.Liquidate(security.Symbol)

    def Rebalance(self):
        # Equal weight allocation (0.2 per stock)
        target_weight_per_stock = 1.0 / 5.0
        
        for symbol in self._universe.Selected:
            if symbol not in self.Securities:
                continue
                
            security = self.Securities[symbol]
            if not (security.rsi2.IsReady and security.rsi10.IsReady and security.sma200.IsReady):
                continue

            price = security.Price
            sma_val = security.sma200.Current.Value
            r2 = security.rsi2.Current.Value
            r10 = security.rsi10.Current.Value

            # BULL MARKET MODE
            if price > sma_val:
                if r10 > 80:
                    # De-leverage on extreme overbought
                    self.SetHoldings(symbol, target_weight_per_stock * 0.2)
                elif r2 < 30:
                    # Full leverage on dips
                    self.SetHoldings(symbol, target_weight_per_stock * 1.0)
                elif not security.Invested:
                    # Default bull entry (50% target)
                    self.SetHoldings(symbol, target_weight_per_stock * 0.5)
            
            # BEAR MARKET MODE
            else:
                if security.Invested:
                    self.Liquidate(symbol)
