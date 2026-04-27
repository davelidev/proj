from datetime import datetime, timedelta
from AlgorithmImports import *

class TechDipHybridExit(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.Settings.AutomaticIndicatorWarmUp = True
        
        self.entry_times = {}
        self.AddUniverse(self._select)
        self.Schedule.On(self.DateRules.EveryDay("SPY"), self.TimeRules.At(10, 5), self._rebalance)
    
    def _select(self, fundamental):
        filtered = [f for f in fundamental if f.HasFundamentalData and f.AssetClassification.MorningstarSectorCode == MorningstarSectorCode.Technology]
        return [f.Symbol for f in sorted(filtered, key=lambda f: f.MarketCap)[-5:]] 
    
    def OnSecuritiesChanged(self, changes):
        for security in changes.AddedSecurities:
            security.rsi = self.RSI(security.Symbol, 2)
            security.max = self.MAX(security.Symbol, 252)
            security.sma20 = self.SMA(security.Symbol, 20)
        for security in changes.RemovedSecurities:
            self.Liquidate(security.Symbol)
            if security.Symbol in self.entry_times: del self.entry_times[security.Symbol]
    
    def _rebalance(self):
        for symbol in self.UniverseManager.ActiveSecurities.Keys:
            security = self.Securities[symbol]
            if not (security.rsi.IsReady and security.sma20.IsReady and security.max.IsReady): continue
            
            # Entry: RSI < 25 AND Price > SMA(20)
            if not security.Invested and security.rsi.Current.Value < 25 and security.Price > security.sma20.Current.Value:
                self.SetHoldings(security.Symbol, 0.2)
                self.entry_times[security.Symbol] = self.Time
            
            # Exit: Either 1-Year High (ATH proxy) OR 6 Months (182 days)
            elif security.Invested:
                is_ath = security.Price >= security.max.Current.Value
                is_six_months = self.Time >= self.entry_times.get(security.Symbol, self.Time) + timedelta(days=182)
                
                if is_ath or is_six_months:
                    reason = "ATH" if is_ath else "6-Month Limit"
                    self.Debug(f"Exiting {symbol.Value} due to {reason}")
                    self.Liquidate(security.Symbol)
                    if security.Symbol in self.entry_times: del self.entry_times[security.Symbol]
