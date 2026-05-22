from datetime import datetime, timedelta
from AlgorithmImports import *

class GiantSniper(QCAlgorithm):
    """
    Giant Sniper (Mean-Reversion) - ARCHIVED
    
    Core Concept:
    - High-conviction mean reversion in global leaders. 
    - Dynamically selects the Top 5 largest companies by Market Cap every month.
    - Entry: Deep daily dips (RSI2 < 20) in any of the Top 5 giants.
    - Exit: Short-term strength (RSI2 > 70) or Broader Trend Break.
    - Shield: QQQ > 200 SMA filter for structural safety.
    """
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        
        # TREND SHIELD
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.sma200 = self.SMA(self.qqq, 200, Resolution.Daily)
        
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.SelectFundamental)
        
        self.data = {}
        self.top5_symbols = []
        
        self.SetWarmUp(200, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.AfterMarketOpen(self.qqq, 30), self.Rebalance)

    def SelectFundamental(self, fundamental):
        # Dynamically track Top 5 Market Cap
        sorted_by_mcap = sorted([f for f in fundamental if f.MarketCap > 0], 
                                key=lambda x: x.MarketCap, reverse=True)
        self.top5_symbols = [f.Symbol for f in sorted_by_mcap[:5]]
        return self.top5_symbols

    def OnSecuritiesChanged(self, changes):
        for security in changes.AddedSecurities:
            symbol = security.Symbol
            if symbol == self.qqq: continue
            if symbol not in self.data:
                self.data[symbol] = SymbolData(self, symbol)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma200.IsReady: return
        
        qqq_price = self.Securities[self.qqq].Price
        is_bull = qqq_price > self.sma200.Current.Value
        
        if is_bull:
            # Check for deep dips in any of the Top 5 giants
            triggered = []
            for s in self.top5_symbols:
                if s in self.data and self.data[s].IsReady:
                    if self.data[s].rsi.Current.Value < 20: # Aggressive dip buy
                        triggered.append(s)
            
            if triggered:
                # Enter top 5 equally
                weight = 1.0 / len(triggered)
                for s in triggered:
                    if not self.Portfolio[s].Invested:
                        self.SetHoldings(s, weight)
            
            # Dynamic Exit: RSI exhaustion OR QQQ Trend break
            for s in self.top5_symbols:
                if self.Portfolio[s].Invested:
                    if self.data[s].rsi.Current.Value > 70:
                        self.Liquidate(s)
        else:
            # Bear Shield
            if self.Portfolio.Invested:
                self.Liquidate()

class SymbolData:
    def __init__(self, algo, symbol):
        self.rsi = algo.RSI(symbol, 2, MovingAverageType.Wilders, Resolution.Daily)
    
    @property
    def IsReady(self):
        return self.rsi.IsReady
