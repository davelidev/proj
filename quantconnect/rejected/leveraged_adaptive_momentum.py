from datetime import datetime, timedelta
from AlgorithmImports import *
import numpy as np

class LeveragedAdaptiveMomentum(QCAlgorithm):
    def Initialize(self):
        # 12 year backtest
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.tmf = self.AddEquity("TMF", Resolution.Daily).Symbol
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        
        self.sma_spy = self.SMA(self.spy, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.MonthStart(self.spy), 
                         self.TimeRules.AfterMarketOpen(self.spy, 35), 
                         self.Rebalance)
        
        self.SetWarmUp(200)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma_spy.IsReady:
            return

        spy_price = self.Securities[self.spy].Price
        is_bull = spy_price > self.sma_spy.Current.Value
        
        if is_bull:
            # Bull Market: Use adaptive allocation between TQQQ and TMF
            # based on realized volatility of TQQQ over last 10 days
            hist = self.History(self.tqqq, 11, Resolution.Daily)
            if hist.empty: return
            
            vol = hist['close'].pct_change().dropna().std() * np.sqrt(252)
            
            # If vol is low (< 40%), go heavy TQQQ. If high (> 40%), mix in TMF.
            if vol < 0.40:
                self.Log(f"Bull Market. Low Vol ({vol:.2%}). 100% TQQQ.")
                self.SetHoldings(self.tqqq, 1.0, liquidateExistingHoldings=True)
            else:
                self.Log(f"Bull Market. High Vol ({vol:.2%}). 60/40 TQQQ/TMF.")
                self.SetHoldings(self.tqqq, 0.6)
                self.SetHoldings(self.tmf, 0.4)
        else:
            # Bear Market: Stay Defensive in TMF
            self.Log("Bear Market. 100% TMF.")
            self.SetHoldings(self.tmf, 1.0, liquidateExistingHoldings=True)
