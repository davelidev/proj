from datetime import datetime, timedelta
from AlgorithmImports import *

class AlphaLeaderRotation(QCAlgorithm):
    """
    Top 5 Alpha Giant Champion (High-Concentration Edition)
    
    Logic:
    - Universe: Top 5 by Market Cap.
    - Ranking: 1-month Momentum (Relative Strength).
    - Position: 100% in the #1 Strength stock.
    - Entry: #1 stock must be at a 20-day High.
    - Shield: QQQ > 200 SMA.
    """
    def Initialize(self):
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100_000)
        
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.sma200 = self.SMA(self.qqq, 200, Resolution.Daily)
        
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.SelectFundamental)
        
        self.data = {}
        self.top5_symbols = []
        
        self.SetWarmUp(200, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.AfterMarketOpen(self.qqq, 30), self.CheckSignals)

    def SelectFundamental(self, fundamental):
        sorted_by_mcap = sorted([f for f in fundamental if f.MarketCap > 0], 
                                key=lambda x: x.MarketCap, reverse=True)
        self.top5_symbols = [f.Symbol for f in sorted_by_mcap[:5]]
        return self.top5_symbols

    def OnSecuritiesChanged(self, changes):
        for security in changes.AddedSecurities:
            if security.Symbol == self.qqq: continue
            if security.Symbol not in self.data:
                self.data[security.Symbol] = SymbolData(self, security.Symbol)

    def CheckSignals(self):
        if self.IsWarmingUp or not self.sma200.IsReady: return
        
        qqq_price = self.Securities[self.qqq].Price
        is_bull = qqq_price > self.sma200.Current.Value
        
        if is_bull:
            # Rank Top 5 by 1-month momentum
            candidates = []
            for s in self.top5_symbols:
                if s in self.data and self.data[s].IsReady:
                    candidates.append((s, self.data[s].mom.Current.Value))
            
            if candidates:
                # Target the SINGLE strongest leader
                leader = sorted(candidates, key=lambda x: x[1], reverse=True)[0][0]
                price = self.Securities[leader].Price
                
                # ENTRY: Leader breaks 20-day High
                if price >= self.data[leader].high.Current.Value:
                    if not self.Portfolio[leader].Invested:
                        self.Liquidate() # Exit others
                        self.SetHoldings(leader, 1.0)
                        self.Debug(f"ALPHA ROTATION: 100% {leader.Value} at {self.Time}")
                
                # EXIT holdings if they break 10-day low or lose #1 spot
                for s in [sec.Symbol for sec in self.Portfolio.Values if sec.Invested]:
                    if s == self.qqq: continue
                    if s != leader or self.Securities[s].Price < self.data[s].low.Current.Value:
                        self.Liquidate(s)
        else:
            if self.Portfolio.Invested:
                self.Liquidate()

class SymbolData:
    def __init__(self, algo, symbol):
        self.mom = algo.ROC(symbol, 21, Resolution.Daily)
        self.high = algo.MAX(symbol, 20, Resolution.Daily)
        self.low = algo.MIN(symbol, 10, Resolution.Daily)
    
    @property
    def IsReady(self):
        return self.mom.IsReady and self.high.IsReady and self.low.IsReady
