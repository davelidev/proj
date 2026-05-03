from datetime import datetime, timedelta
from AlgorithmImports import *


class LargeCapTechStrategy(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.Settings.AutomaticIndicatorWarmUp = True
        self.Settings.SeedInitialPrices = True
        
        self._universe = self.AddUniverse(self._select)
        self.Schedule.On(
            self.DateRules.WeekStart("SPY"),
            self.TimeRules.AfterMarketOpen("SPY", 5),
            self._rebalance,
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
            security.rsi = self.RSI(security.Symbol, 2)
            security.max = self.MAX(security.Symbol, 252)
            security.sma50 = self.SMA(security.Symbol, 50)
        for security in changes.RemovedSecurities:
            self.Liquidate(security.Symbol)
    
    def _rebalance(self):
        if not self._universe.Selected: return

        for symbol in self._universe.Selected:   
            security = self.Securities[symbol]
            if not (security.max.IsReady and security.sma50.IsReady):
                continue                        
            
            # Buy signal: RSI(2) < 30 AND Price > SMA(50)
            if not security.Invested:
                if security.rsi.Current.Value < 30 and security.Price > security.sma50.Current.Value:
                    self.SetHoldings(security.Symbol, 1 / 5.0)
            
            # Sell signal: 15% hard stop OR at 1yr-high (ATH proxy)
            else:
                # 15% Hard Stop
                if security.Price <= security.Holdings.AveragePrice * 0.85:
                    self.Liquidate(security.Symbol)
                # Exit at ATH (1-year high)
                elif security.Price >= security.max.Current.Value:
                    self.Liquidate(security.Symbol)
