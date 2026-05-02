from AlgorithmImports import *
import numpy as np

class KalmanRSIMeanReversion(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.ticker = "TQQQ"
        self.symbol = self.AddEquity(self.ticker, Resolution.Daily).Symbol
        
        # Indicators
        self.rsi = self.RSI(self.symbol, 2, MovingAverageType.Wilders, Resolution.Daily)
        
        # Kalman Filter Parameters for RSI smoothing
        self.Q = 1e-4 
        self.R = 0.1 
        self.x = 50    
        self.P = 1    
        self.smoothed_rsi = 50
        
        self.SetWarmUp(30)

    def OnData(self, data):
        if not self.rsi.IsReady: return
        
        # Kalman Update for RSI
        rsi_val = float(self.rsi.Current.Value)
        self.P += self.Q
        K = self.P / (self.P + self.R)
        self.smoothed_rsi = self.x + K * (rsi_val - self.x)
        self.x = self.smoothed_rsi
        self.P = (1 - K) * self.P
        
        if self.IsWarmingUp: return

        # Trading Logic: Long if smoothed RSI is oversold
        if self.smoothed_rsi < 25:
            if not self.Portfolio[self.symbol].Invested:
                self.SetHoldings(self.symbol, 1.0)
        elif self.smoothed_rsi > 75:
            if self.Portfolio[self.symbol].Invested:
                self.Liquidate(self.symbol)
