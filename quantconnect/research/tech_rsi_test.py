from AlgorithmImports import *
from datetime import timedelta

class TechRSI10AM(QCAlgorithm):
    """
    Strategy 10: Tech RSI Giant (10:00 AM Execution)
    - Universe: Top 30 Market Cap Tech Stocks
    - Entry: RSI(2) < 30
    - Execution: Every day at 10:00 AM
    - Hold: Fixed 5 Trading Days
    - Sizing: Fixed 20% per position (Max 5 slots)
    """
    def Initialize(self):
        self.SetStartDate(2020, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        # Using Minute resolution for the underlying to allow 10:00 AM execution
        self.UniverseSettings.Resolution = Resolution.Minute
        self.AddUniverse(self.CoarseSelectionFunction, self.FineSelectionFunction)
        
        self.rsi_period = 2
        self.rsi_threshold = 30
        self.hold_days = 5
        self.max_slots = 5
        
        self.entry_times = {} 
        self.indicators = {}

        # Schedule the logic to run at 10:00 AM every day
        self.Schedule.On(
            self.DateRules.EveryDay("AAPL"),
            self.TimeRules.At(10, 0),
            self.ExecuteStrategy
        )

    def CoarseSelectionFunction(self, coarse):
        sorted_by_volume = sorted([x for x in coarse if x.HasFundamentalData], 
                                  key=lambda x: x.DollarVolume, reverse=True)
        return [x.Symbol for x in sorted_by_volume[:200]]

    def FineSelectionFunction(self, fine):
        tech_stocks = [x for x in fine if x.AssetClassification.MorningstarSectorCode == MorningstarSectorCode.Technology]
        sorted_by_mkt_cap = sorted(tech_stocks, key=lambda x: x.MarketCap, reverse=True)
        return [x.Symbol for x in sorted_by_mkt_cap[:30]]

    def ExecuteStrategy(self):
        if self.IsWarmingUp: return

        # 1. Update Indicators (using Daily bars for the calculation)
        for symbol in self.ActiveSecurities.Keys:
            if symbol not in self.indicators:
                # We still want the RSI(2) to be based on Daily bars
                self.indicators[symbol] = self.RSI(symbol, self.rsi_period, MovingAverageType.Wilders, Resolution.Daily)
            
        # 2. Check for Exits (5-Day Hold)
        to_liquidate = []
        for symbol in list(self.entry_times.keys()):
            if self.Time >= self.entry_times[symbol] + timedelta(days=self.hold_days):
                to_liquidate.append(symbol)
        
        for symbol in to_liquidate:
            self.Liquidate(symbol)
            self.Debug(f"10:00 AM EXIT: {symbol.Value} (Time limit reached)")
            del self.entry_times[symbol]

        # 3. Check for Entry slots
        invested_symbols = [s for s in self.Portfolio.Keys if self.Portfolio[s].Invested]
        slots_available = self.max_slots - len(invested_symbols)

        if slots_available > 0:
            qualified = []
            for symbol in self.indicators:
                if not self.ActiveSecurities.ContainsKey(symbol): continue
                if symbol in invested_symbols: continue
                
                rsi = self.indicators[symbol]
                if rsi.IsReady and rsi.Current.Value < self.rsi_threshold:
                    qualified.append(symbol)
            
            if qualified:
                qualified.sort(key=lambda s: self.indicators[s].Current.Value)
                for target in qualified[:slots_available]:
                    self.SetHoldings(target, 0.20)
                    self.entry_times[target] = self.Time
                    self.Debug(f"10:00 AM ENTRY: {target.Value} at RSI {self.indicators[target].Current.Value:.2f}")

    def OnData(self, data):
        # Logic handled by Schedule.On
        pass
