from AlgorithmImports import *

class VigilantAssetAllocation(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        # Define Universes
        self.offensive = ["SPY", "EFA", "EEM", "AGG"]
        self.defensive = ["LQD", "IEF", "SHY"]
        self.symbols = [self.AddEquity(ticker, Resolution.Daily).Symbol for ticker in self.offensive + self.defensive]

        # Rebalance monthly on the last trading day
        self.Schedule.On(self.DateRules.MonthEnd("SPY"), 
                         self.TimeRules.BeforeMarketClose("SPY", 30), 
                         self.Rebalance)

    def Rebalance(self):
        scores = {}
        
        # 1. Calculate Momentum Scores for all assets
        for symbol in self.symbols:
            history = self.History(symbol, 260, Resolution.Daily)
            if history.empty: continue
            
            # Get prices for 1, 3, 6, and 12 months ago (approx 21 trading days/month)
            prices = history['close']
            if len(prices) < 253: continue
            
            p0 = prices.iloc[-1]
            r1 = (p0 / prices.iloc[-22]) - 1
            r3 = (p0 / prices.iloc[-64]) - 1
            r6 = (p0 / prices.iloc[-127]) - 1
            r12 = (p0 / prices.iloc[-253]) - 1
            
            scores[symbol] = (12 * r1) + (4 * r3) + (2 * r6) + (1 * r12)

        if not scores: return

        # 2. Check Breadth (Are all offensive assets positive?)
        offensive_symbols = [s for s in self.symbols if s.Value in self.offensive]
        offensive_scores = {s: scores[s] for s in offensive_symbols if s in scores}
        
        if len(offensive_scores) < len(self.offensive): return
        
        all_positive = all(score > 0 for score in offensive_scores.values())

        # 3. Select Target Asset
        if all_positive:
            # Risk-On: Pick best offensive
            target_symbol = max(offensive_scores, key=offensive_scores.get)
        else:
            # Risk-Off: Pick best defensive
            defensive_symbols = [s for s in self.symbols if s.Value in self.defensive]
            defensive_scores = {s: scores[s] for s in defensive_symbols if s in scores}
            if not defensive_scores: return
            target_symbol = max(defensive_scores, key=defensive_scores.get)

        # 4. Execute Trades
        for symbol in self.symbols:
            if symbol != target_symbol and self.Portfolio[symbol].Invested:
                self.Liquidate(symbol)
        
        self.SetHoldings(target_symbol, 1.0)
