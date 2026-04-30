from datetime import datetime, timedelta
from AlgorithmImports import *

class QuantumDipRotator(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        
        self.tickers = ["AAPL", "MSFT", "NVDA", "GOOGL"]
        self.symbols = [self.AddEquity(t, Resolution.Daily).Symbol for t in self.tickers]
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        
        self.sma10 = {s: self.SMA(s, 10, Resolution.Daily) for s in self.symbols}
        self.sma200 = self.SMA(self.qqq, 200, Resolution.Daily)
        
        self.SetWarmUp(200, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.AfterMarketOpen("AAPL", 30), self.Rebalance)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma200.IsReady: return
        
        qqq_price = self.Securities[self.qqq].Price
        sma200_val = self.sma200.Current.Value
        
        # Bull Regime Only
        if qqq_price > sma200_val:
            if not self.Portfolio.Invested:
                # Find the stock with the deepest stretch below its SMA10
                candidates = []
                for s in self.symbols:
                    price = self.Securities[s].Price
                    sma = self.sma10[s].Current.Value
                    if price < (sma * 0.95): # >5% stretch
                        candidates.append((s, price/sma))
                
                if candidates:
                    # Enter the one with lowest ratio (deepest dip)
                    target = min(candidates, key=lambda x: x[1])[0]
                    self.SetHoldings(target, 1.0)
            else:
                # EXIT logic for invested stock
                invested = [s for s in self.symbols if self.Portfolio[s].Invested][0]
                if self.Securities[invested].Price > self.sma10[invested].Current.Value:
                    self.Liquidate()
        else:
            self.Liquidate()
