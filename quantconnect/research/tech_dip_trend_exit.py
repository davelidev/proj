from datetime import datetime, timedelta
from AlgorithmImports import *

class TechDipTrendExit(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.Settings.AutomaticIndicatorWarmUp = True
        
        self.AddUniverse(self._select)
        # Check daily at 10:05 AM
        self.Schedule.On(self.DateRules.EveryDay("SPY"), self.TimeRules.At(10, 5), self._rebalance)
    
    def _select(self, fundamental):
        # Top 5 Tech Giants by Market Cap
        filtered = [f for f in fundamental if f.HasFundamentalData and f.AssetClassification.MorningstarSectorCode == MorningstarSectorCode.Technology]
        return [f.Symbol for f in sorted(filtered, key=lambda f: f.MarketCap)[-5:]] 
    
    def OnSecuritiesChanged(self, changes):
        for security in changes.AddedSecurities:
            security.rsi = self.RSI(security.Symbol, 2)
            security.max = self.MAX(security.Symbol, 252) # 1-year high
            security.sma20 = self.SMA(security.Symbol, 20)
            security.sma200 = self.SMA(security.Symbol, 200) # Trend filter
        for security in changes.RemovedSecurities:
            self.Liquidate(security.Symbol)
    
    def _rebalance(self):
        # We trade the current universe selection
        for symbol in self.UniverseManager.ActiveSecurities.Keys:
            security = self.Securities[symbol]
            if not (security.rsi.IsReady and security.sma20.IsReady and security.max.IsReady and security.sma200.IsReady): 
                continue
            
            # Entry: RSI < 25 AND Price > SMA(20) (Bullish pullback)
            if not security.Invested and security.rsi.Current.Value < 25 and security.Price > security.sma20.Current.Value:
                self.SetHoldings(security.Symbol, 0.2)
            
            # Exit: Price >= 1-Year High OR Price < SMA(200) (Trend Failure)
            elif security.Invested:
                is_ath = security.Price >= security.max.Current.Value
                is_trend_failure = security.Price < security.sma200.Current.Value
                
                if is_ath or is_trend_failure:
                    reason = "ATH" if is_ath else "Trend Failure (SMA200)"
                    self.Debug(f"Exiting {symbol.Value} due to {reason}")
                    self.Liquidate(security.Symbol)
