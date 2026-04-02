from datetime import datetime, timedelta
from AlgorithmImports import *

class TQQQTECLAlpha(QCAlgorithm):
    def Initialize(self):
        # 12 year backtest
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.tecl = self.AddEquity("TECL", Resolution.Daily).Symbol
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        
        self.sma_spy = self.SMA(self.spy, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.MonthStart(self.spy), 
                         self.TimeRules.AfterMarketOpen(self.spy, 35), 
                         self.Rebalance)
        
        self.SetWarmUp(252)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma_spy.IsReady:
            return

        spy_price = self.Securities[self.spy].Price
        
        if spy_price > self.sma_spy.Current.Value:
            # Bull Market: Rotation between Tech Leaders
            # Using 12-month momentum for stability
            hist_t = self.History(self.tqqq, 252, Resolution.Daily)
            hist_l = self.History(self.tecl, 252, Resolution.Daily)
            
            if hist_t.empty or hist_l.empty: return
            
            mom_t = (hist_t['close'].iloc[-1] / hist_t['close'].iloc[0]) - 1
            mom_l = (hist_l['close'].iloc[-1] / hist_l['close'].iloc[0]) - 1
            
            best = self.tqqq if mom_t > mom_l else self.tecl
            
            if not self.Portfolio[best].Invested:
                self.Log(f"Bull Market. Winner: {best.Value} ({max(mom_t, mom_l):.2%}). Allocating.")
                self.Liquidate()
                self.SetHoldings(best, 1.0)
        else:
            if self.Portfolio.Invested:
                self.Log("Bear Market. Liquidating to Cash.")
                self.Liquidate()
