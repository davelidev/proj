from datetime import datetime, timedelta
from AlgorithmImports import *
import pandas as pd

class VAALeveraged(QCAlgorithm):

    def Initialize(self):
        # 12 year backtest
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100000)

        # VAA-G Offensive Assets (Including TQQQ for CAGR > 30%)
        self.offensive = ["TQQQ", "EFA", "EEM", "AGG"]
        # VAA-G Defensive Assets
        self.defensive = ["LQD", "IEF", "SHY"]
        
        self.symbols = {}
        for ticker in self.offensive + self.defensive:
            symbol = self.AddEquity(ticker, Resolution.Daily).Symbol
            self.symbols[ticker] = symbol

        # Rebalance on the first trading day of each month
        self.Schedule.On(self.DateRules.MonthStart("TQQQ"), 
                         self.TimeRules.AfterMarketOpen("TQQQ", 35), 
                         self.Rebalance)
        
        self.SetWarmUp(253)

    def Rebalance(self):
        if self.IsWarmingUp:
            return

        scores = {}
        
        # Calculate Momentum Scores (13612W) for all assets
        # Score = (12 * r1) + (4 * r3) + (2 * r6) + (1 * r12)
        for ticker, symbol in self.symbols.items():
            history = self.History(symbol, 253, Resolution.Daily)
            if history.empty or len(history) < 253:
                continue
            
            prices = history['close']
            p0 = prices.iloc[-1]
            p1 = prices.iloc[-22]
            p3 = prices.iloc[-64]
            p6 = prices.iloc[-127]
            p12 = prices.iloc[-253]
            
            r1 = (p0 / p1) - 1
            r3 = (p0 / p3) - 1
            r6 = (p0 / p6) - 1
            r12 = (p0 / p12) - 1
            
            scores[ticker] = (12 * r1) + (4 * r3) + (2 * r6) + (1 * r12)

        if not scores: return

        # VAA-G Logic: Risk-on only if ALL offensive assets have positive momentum
        all_offensive_positive = all(scores.get(t, -1) > 0 for t in self.offensive)

        if all_offensive_positive:
            # Risk-On: Pick the offensive asset with the highest score
            best_ticker = max(self.offensive, key=lambda t: scores.get(t, -1000))
            self.Log(f"RISK-ON: {best_ticker} (Score: {scores[best_ticker]:.2f})")
        else:
            # Risk-Off: Pick the defensive asset with the highest score
            best_ticker = max(self.defensive, key=lambda t: scores.get(t, -1000))
            self.Log(f"RISK-OFF: {best_ticker} (Score: {scores[best_ticker]:.2f})")

        target_symbol = self.symbols[best_ticker]
        
        # Liquidate and switch to the new best asset
        if not self.Portfolio[target_symbol].Invested:
            self.Liquidate()
            self.SetHoldings(target_symbol, 1.0)
