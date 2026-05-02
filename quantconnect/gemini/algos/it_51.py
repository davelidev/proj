from AlgorithmImports import *
from statsmodels.tsa.stattools import coint
import numpy as np

class StatArbPairsTrading(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        # Assets
        self.ticker1 = "PEP"
        self.ticker2 = "KO"
        self.pair = [self.AddEquity(self.ticker1, Resolution.Daily).Symbol, 
                     self.AddEquity(self.ticker2, Resolution.Daily).Symbol]

        # Parameters
        self.lookback = 252 
        self.entry_threshold = 2.0
        self.exit_threshold = 0.5
        
        self.SetWarmUp(self.lookback)

    def OnData(self, data):
        if self.IsWarmingUp: return

        # Get historical data
        history = self.History(self.pair, self.lookback, Resolution.Daily)
        if history.empty or len(history) < self.lookback: return

        # Extract prices
        prices = history['close'].unstack(level=0)
        if self.pair[0] not in prices or self.pair[1] not in prices: return
        
        asset1 = prices[self.pair[0]]
        asset2 = prices[self.pair[1]]

        # 1. Test for Cointegration
        try:
            _, pvalue, _ = coint(asset1, asset2)
        except:
            return
        
        if pvalue < 0.05:
            # 2. Calculate Z-Score of the ratio
            ratio = asset1 / asset2
            mean = ratio.mean()
            std = ratio.std()
            current_ratio = asset1.iloc[-1] / asset2.iloc[-1]
            
            zscore = (current_ratio - mean) / std

            # 3. Trading Logic
            if zscore > self.entry_threshold:
                # Spread high: Short A1, Long A2
                self.SetHoldings(self.pair[0], -0.5)
                self.SetHoldings(self.pair[1], 0.5)
            elif zscore < -self.entry_threshold:
                # Spread low: Long A1, Short A2
                self.SetHoldings(self.pair[0], 0.5)
                self.SetHoldings(self.pair[1], -0.5)
            elif abs(zscore) < self.exit_threshold:
                self.Liquidate()
