from datetime import datetime, timedelta
from AlgorithmImports import *
import numpy as np

class VolTargetingLeveraged(QCAlgorithm):
    def Initialize(self):
        # 12 year backtest
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100000)
        
        # Target 20% Annual Volatility
        self.target_vol = 0.20
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        self.ief = self.AddEquity("IEF", Resolution.Daily).Symbol
        
        # Lookback for realized volatility (21 trading days = ~1 month)
        self.vol_lookback = 21
        
        # Trend Filter
        self.sma_spy = self.SMA(self.spy, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.spy), 
                         self.TimeRules.AfterMarketOpen(self.spy, 35), 
                         self.Rebalance)
        
        self.SetWarmUp(200)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma_spy.IsReady:
            return

        # 1. Calculate Realized Volatility of TQQQ
        history = self.History(self.tqqq, self.vol_lookback + 1, Resolution.Daily)
        if history.empty or len(history) < self.vol_lookback:
            return
            
        returns = history['close'].pct_change().dropna()
        realized_vol = returns.std() * np.sqrt(252) # Annualized
        
        if realized_vol == 0: return

        # 2. Determine Position Size (Volatility Scaling)
        # Weight = Target Vol / Current Vol
        weight = self.target_vol / realized_vol
        
        # 3. Apply Trend Filter
        spy_price = self.Securities[self.spy].Price
        if spy_price < self.sma_spy.Current.Value:
            # Bear Market: Switch to Defensive
            self.Log(f"Bear Market: Scaling to 0% TQQQ, 100% IEF")
            self.SetHoldings(self.tqqq, 0.0)
            self.SetHoldings(self.ief, 1.0)
        else:
            # Bull Market: Vol Targeting (cap at 100% exposure for safety)
            final_weight = min(weight, 1.0)
            self.Log(f"Bull Market: Vol {realized_vol:.2%}. Target {self.target_vol:.2%}. Weight {final_weight:.2%}")
            self.SetHoldings(self.tqqq, final_weight)
            self.SetHoldings(self.ief, 1.0 - final_weight)
