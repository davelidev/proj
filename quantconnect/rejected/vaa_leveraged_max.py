from datetime import datetime, timedelta
from AlgorithmImports import *

class VAALeveragedMax(QCAlgorithm):
    def Initialize(self):
        # 12 year backtest
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100000)

        # High-Beta Offensive Universe for >30% CAGR
        # FNGU/BULZ have higher returns than TQQQ during bull runs
        self.offensive = ["TQQQ", "SOXL", "TECL", "FNGU"]
        self.defensive = ["TLT", "IEF", "SHY"]
        
        self.symbols = {}
        for ticker in self.offensive + self.defensive:
            # Note: FNGU launched in Jan 2018. Before that, it will be skipped.
            # We'll handle missing data gracefully.
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
            if not self.Securities[symbol].HasData:
                continue
                
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

        # Unanimous positive rule for low drawdown
        available_offensive = [t for t in self.offensive if t in scores]
        all_offensive_positive = all(scores.get(t, -1) > 0 for t in available_offensive)

        if all_offensive_positive and len(available_offensive) > 0:
            # Risk-On: Pick the top asset
            best_ticker = max(available_offensive, key=lambda t: scores.get(t, -1000))
            self.Log(f"RISK-ON: {best_ticker}")
            target_symbol = self.symbols[best_ticker]
        else:
            # Risk-Off: Pick the best defensive asset
            best_ticker = max(self.defensive, key=lambda t: scores.get(t, -1000))
            self.Log(f"RISK-OFF: {best_ticker}")
            target_symbol = self.symbols[best_ticker]

        if not self.Portfolio[target_symbol].Invested:
            self.Liquidate()
            self.SetHoldings(target_symbol, 1.0)
