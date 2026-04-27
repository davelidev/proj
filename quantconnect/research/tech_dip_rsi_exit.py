from datetime import datetime, timedelta
from AlgorithmImports import *

class TechDipRSIExit(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.Settings.AutomaticIndicatorWarmUp = True
        
        self.AddUniverse(self._select)
        self.Schedule.On(self.DateRules.EveryDay("SPY"), self.TimeRules.At(10, 5), self._rebalance)
    
    def _select(self, fundamental):
        filtered = [f for f in fundamental if f.HasFundamentalData and f.AssetClassification.MorningstarSectorCode == MorningstarSectorCode.Technology]
        return [f.Symbol for f in sorted(filtered, key=lambda f: f.MarketCap)[-5:]] 
    
    def OnSecuritiesChanged(self, changes):
        for security in changes.AddedSecurities:
            security.rsi = self.RSI(security.Symbol, 2)
            security.sma20 = self.SMA(security.Symbol, 20)
        for security in changes.RemovedSecurities:
            self.Liquidate(security.Symbol)
    
    def _rebalance(self):
        for symbol in self.UniverseManager.ActiveSecurities.Keys:
            security = self.Securities[symbol]
            if not (security.rsi.IsReady and security.sma20.IsReady): continue
            
            # Entry: RSI < 25 AND Price > SMA(20)
            if not security.Invested and security.rsi.Current.Value < 25 and security.Price > security.sma20.Current.Value:
                self.SetHoldings(security.Symbol, 0.2)
            # Exit: RSI > 70
            elif security.Invested and security.rsi.Current.Value > 70:
                self.Liquidate(security.Symbol)
