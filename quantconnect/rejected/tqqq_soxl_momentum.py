from datetime import datetime, timedelta
from AlgorithmImports import *

class TQQQSOXLMomentum(QCAlgorithm):
    def Initialize(self):
        # 12 year backtest
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.soxl = self.AddEquity("SOXL", Resolution.Daily).Symbol
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        
        self.sma_spy = self.SMA(self.spy, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.spy), 
                         self.TimeRules.AfterMarketOpen(self.spy, 35), 
                         self.Rebalance)
        
        self.SetWarmUp(200)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma_spy.IsReady:
            return

        spy_price = self.Securities[self.spy].Price
        
        if spy_price > self.sma_spy.Current.Value:
            # Bull Market: Rotation between the two highest alpha engines
            # Using 20-day momentum
            hist_tqqq = self.History(self.tqqq, 21, Resolution.Daily)
            hist_soxl = self.History(self.soxl, 21, Resolution.Daily)
            
            if hist_tqqq.empty or hist_soxl.empty: return
            
            mom_t = (hist_tqqq['close'].iloc[-1] / hist_tqqq['close'].iloc[0]) - 1
            mom_s = (hist_soxl['close'].iloc[-1] / hist_soxl['close'].iloc[0]) - 1
            
            best = self.tqqq if mom_t > mom_s else self.soxl
            
            if not self.Portfolio[best].Invested:
                self.Log(f"Bull Market. Winner: {best.Value} ({max(mom_t, mom_s):.2%}). Allocating.")
                self.Liquidate()
                self.SetHoldings(best, 1.0)
        else:
            if self.Portfolio.Invested:
                self.Log("Bear Market. Liquidating to Cash.")
                self.Liquidate()
