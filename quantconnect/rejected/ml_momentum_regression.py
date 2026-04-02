from datetime import datetime, timedelta
from AlgorithmImports import *
from sklearn.linear_model import LinearRegression
import numpy as np

class MLMomentumRegression(QCAlgorithm):
    def Initialize(self):
        # 12 year backtest
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100000)

        # High-alpha candidates
        self.tickers = ["TQQQ", "SOXL", "FNGU"]
        self.symbols = [self.AddEquity(t, Resolution.Daily).Symbol for t in self.tickers]
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        
        # Trend Filter
        self.sma_spy = self.SMA(self.spy, 200, Resolution.Daily)
        
        self.lookback = 60  # Days to train
        self.features = 5   # Previous 5 days returns as features
        
        self.Schedule.On(self.DateRules.EveryDay(self.spy), 
                         self.TimeRules.AfterMarketOpen(self.spy, 35), 
                         self.Rebalance)
        
        self.SetWarmUp(self.lookback + self.features)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma_spy.IsReady:
            return

        # Regime Filter: Only trade in Bull Markets
        if self.Securities[self.spy].Price < self.sma_spy.Current.Value:
            if self.Portfolio.Invested:
                self.Liquidate()
            return

        predictions = {}
        for symbol in self.symbols:
            # Note: FNGU might not have enough history in early years
            if not self.Securities[symbol].HasData:
                continue
                
            history = self.History(symbol, self.lookback + self.features + 1, Resolution.Daily)
            if history.empty or len(history) < (self.lookback + self.features + 1):
                continue

            returns = history['close'].pct_change().dropna().values
            
            # X: Previous 'features' days returns
            # Y: Next day return
            X = []
            Y = []
            for i in range(len(returns) - self.features):
                X.append(returns[i:i+self.features])
                Y.append(returns[i+self.features])
            
            model = LinearRegression()
            model.fit(X, Y)
            
            # Predict next day using the most recent returns
            latest_features = np.array(returns[-self.features:]).reshape(1, -1)
            prediction = model.predict(latest_features)[0]
            predictions[symbol] = prediction

        # Pick the asset with the highest predicted return, if positive
        if predictions:
            best_symbol = max(predictions, key=predictions.get)
            if predictions[best_symbol] > 0:
                if not self.Portfolio[best_symbol].Invested:
                    self.Log(f"ML Predict {best_symbol.Value}: {predictions[best_symbol]:.4f}")
                    self.SetHoldings(best_symbol, 1.0, liquidateExistingHoldings=True)
            else:
                if self.Portfolio.Invested:
                    self.Log("No positive predictions. Liquidating.")
                    self.Liquidate()
