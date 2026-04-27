from datetime import datetime, timedelta
from AlgorithmImports import *

class TechDipAggressive(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.Settings.AutomaticIndicatorWarmUp = True
        
        # Track high water marks for trailing stops
        self.high_water_marks = {}
        
        self.AddUniverse(self._select)
        # Check DAILY for high-precision entries and exits
        self.Schedule.On(self.DateRules.EveryDay("SPY"), self.TimeRules.At(10, 5), self._rebalance)
    
    def _select(self, fundamental):
        # Top 5 Tech Giants
        filtered = [f for f in fundamental if f.HasFundamentalData and f.AssetClassification.MorningstarSectorCode == MorningstarSectorCode.Technology]
        return [f.Symbol for f in sorted(filtered, key=lambda f: f.MarketCap)[-5:]] 
    
    def OnSecuritiesChanged(self, changes):
        for security in changes.AddedSecurities:
            security.rsi = self.RSI(security.Symbol, 2)
            security.max = self.MAX(security.Symbol, 252) # 1-year high
            security.sma20 = self.SMA(security.Symbol, 20)
        for security in changes.RemovedSecurities:
            self.Liquidate(security.Symbol)
            if security.Symbol in self.high_water_marks: del self.high_water_marks[security.Symbol]
    
    def _rebalance(self):
        for symbol in self.UniverseManager.ActiveSecurities.Keys:
            security = self.Securities[symbol]
            if not (security.rsi.IsReady and security.sma20.IsReady and security.max.IsReady): 
                continue
            
            price = security.Price
            
            # Entry: RSI < 30 AND Price > SMA(20)
            if not security.Invested and security.rsi.Current.Value < 30 and price > security.sma20.Current.Value:
                self.SetHoldings(security.Symbol, 0.2)
                self.high_water_marks[security.Symbol] = price
            
            elif security.Invested:
                # Update Trailing Stop High Water Mark
                if price > self.high_water_marks.get(security.Symbol, 0):
                    self.high_water_marks[security.Symbol] = price
                
                # Exits
                is_ath = price >= security.max.Current.Value
                is_stop = price < self.high_water_marks[security.Symbol] * 0.85 # 15% Trailing Stop
                
                if is_ath or is_stop:
                    reason = "ATH" if is_ath else "15% Trailing Stop"
                    self.Debug(f"Exiting {symbol.Value} due to {reason}")
                    self.Liquidate(security.Symbol)
                    if security.Symbol in self.high_water_marks: del self.high_water_marks[security.Symbol]
