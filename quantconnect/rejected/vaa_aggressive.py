from datetime import datetime, timedelta
from AlgorithmImports import *
import pandas as pd

class VAAAggressive(QCAlgorithm):

    def Initialize(self):
        # 12 year backtest
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100000)

        # More aggressive offensive universe
        self.offensive = ["TQQQ", "SOXL", "TECL", "UPRO"]
        self.defensive = ["IEF", "SHY"]
        
        self.symbols = {}
        for ticker in self.offensive + self.defensive:
            symbol = self.AddEquity(ticker, Resolution.Daily).Symbol
            self.symbols[ticker] = symbol

        self.Schedule.On(self.DateRules.MonthStart("TQQQ"), 
                         self.TimeRules.AfterMarketOpen("TQQQ", 35), 
                         self.Rebalance)
        
        self.SetWarmUp(253)

    def Rebalance(self):
        if self.IsWarmingUp:
            return

        scores = {}
        for ticker, symbol in self.symbols.items():
            history = self.History(symbol, 253, Resolution.Daily)
            if history.empty or len(history) < 253:
                continue
            
            prices = history['close']
            p0 = prices.iloc[-1]
            r1 = (p0 / prices.iloc[-22]) - 1
            r3 = (p0 / prices.iloc[-64]) - 1
            r6 = (p0 / prices.iloc[-127]) - 1
            r12 = (p0 / prices.iloc[-253]) - 1
            scores[ticker] = (12 * r1) + (4 * r3) + (2 * r6) + (1 * r12)

        if not scores: return

        # Relaxed VAA: Risk-on if at least 2 offensive assets are positive
        # This allows for more aggressive entries than the "unanimous" rule
        positive_offensive = [t for t in self.offensive if scores.get(t, -1) > 0]

        if len(positive_offensive) >= 2:
            # Risk-On: Pick the top 2 offensive assets
            best_assets = sorted(positive_offensive, key=lambda t: scores.get(t, -1000), reverse=True)[:2]
            self.Log(f"RISK-ON: {best_assets}")
            
            self.Liquidate()
            for t in best_assets:
                self.SetHoldings(self.symbols[t], 0.5)
        else:
            # Risk-Off: Pick the best defensive asset
            best_ticker = max(self.defensive, key=lambda t: scores.get(t, -1000))
            self.Log(f"RISK-OFF: {best_ticker}")
            self.Liquidate()
            self.SetHoldings(self.symbols[best_ticker], 1.0)
