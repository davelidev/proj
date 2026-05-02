from AlgorithmImports import *
import numpy as np

class KalmanTrendFollowing(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.ticker = "TQQQ"
        self.symbol = self.AddEquity(self.ticker, Resolution.Daily).Symbol
        
        # Kalman Filter Parameters
        self.Q = 1e-5 # Process Noise
        self.R = 0.01 # Measurement Noise
        self.x = 0    # Initial state (price)
        self.P = 1    # Initial covariance
        self.velocity = 0 # Estimated momentum
        
        self.SetWarmUp(30)

    def OnData(self, data):
        if not data.Bars.ContainsKey(self.symbol): return
        
        price = float(data.Bars[self.symbol].Close)
        
        # Kalman Filter Update
        # 1. Prediction
        # x_pred = x
        # P_pred = P + Q
        self.P += self.Q
        
        # 2. Update
        # K = P_pred / (P_pred + R)
        K = self.P / (self.P + self.R)
        
        # x_new = x_pred + K * (price - x_pred)
        new_x = self.x + K * (price - self.x)
        
        # Velocity estimate (change in state)
        self.velocity = new_x - self.x
        
        # Update state and covariance
        self.x = new_x
        self.P = (1 - K) * self.P
        
        if self.IsWarmingUp: return

        # Trading Logic: Long if velocity is positive (uptrend)
        if self.velocity > 0:
            if not self.Portfolio[self.symbol].Invested:
                self.SetHoldings(self.symbol, 1.0)
        else:
            if self.Portfolio[self.symbol].Invested:
                self.Liquidate(self.symbol)
