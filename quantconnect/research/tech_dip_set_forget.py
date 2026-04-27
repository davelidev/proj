from datetime import datetime, timedelta
from AlgorithmImports import *

class TechDipSetForget(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.Settings.AutomaticIndicatorWarmUp = True
        
        # Track entry prices for hard stops
        self.entry_prices = {}
        
        self.AddUniverse(self._select)
        # Daily precision for rebalancing
        self.Schedule.On(self.DateRules.EveryDay("SPY"), self.TimeRules.At(10, 5), self._rebalance)
    
    def _select(self, fundamental):
        # Top 5 Tech Giants
        filtered = [f for f in fundamental if f.HasFundamentalData and f.AssetClassification.MorningstarSectorCode == MorningstarSectorCode.Technology]
        return [f.Symbol for f in sorted(filtered, key=lambda f: f.MarketCap)[-5:]] 
    
    def OnSecuritiesChanged(self, changes):
        for security in changes.AddedSecurities:
            security.rsi = self.RSI(security.Symbol, 2)
            security.max = self.MAX(security.Symbol, 252) # 1-year high
            security.sma50 = self.SMA(security.Symbol, 50)
        for security in changes.RemovedSecurities:
            self.Liquidate(security.Symbol)
            if security.Symbol in self.entry_prices: del self.entry_prices[security.Symbol]
    
    def _rebalance(self):
        for symbol in self.UniverseManager.ActiveSecurities.Keys:
            security = self.Securities[symbol]
            if not (security.rsi.IsReady and security.sma50.IsReady and security.max.IsReady): 
                continue
            
            price = security.Price
            
            # Entry: RSI < 30 AND Price > SMA(50)
            if not security.Invested and security.rsi.Current.Value < 30 and price > security.sma50.Current.Value:
                self.SetHoldings(security.Symbol, 0.2)
                self.entry_prices[security.Symbol] = price
            
            elif security.Invested:
                # Exits
                is_ath = price >= security.max.Current.Value
                
                # Hard "Set and Forget" Stop Loss (15% below initial entry)
                entry_price = self.entry_prices.get(security.Symbol, price)
                is_hard_stop = price < entry_price * 0.85 
                
                if is_ath or is_hard_stop:
                    reason = "ATH" if is_ath else "15% Hard Stop"
                    self.Debug(f"Exiting {symbol.Value} due to {reason}")
                    self.Liquidate(security.Symbol)
                    if security.Symbol in self.entry_prices: del self.entry_prices[security.Symbol]
