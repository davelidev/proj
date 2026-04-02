from datetime import datetime, timedelta
from AlgorithmImports import *

class TQQQTECLTrend(QCAlgorithm):
    def Initialize(self):
        # 12 year backtest
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.tecl = self.AddEquity("TECL", Resolution.Daily).Symbol
        
        # Individual Trend Filters
        self.sma_t = self.SMA(self.tqqq, 50, Resolution.Daily)
        self.sma_l = self.SMA(self.tecl, 50, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq), 
                         self.TimeRules.AfterMarketOpen(self.tqqq, 35), 
                         self.Rebalance)
        
        self.SetWarmUp(50)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma_t.IsReady or not self.sma_l.IsReady:
            return

        # Check Trend
        t_bull = self.Securities[self.tqqq].Price > self.sma_t.Current.Value
        l_bull = self.Securities[self.tecl].Price > self.sma_l.Current.Value
        
        if t_bull or l_bull:
            # At least one is in a bull trend. Pick the best 10-day momentum.
            hist_t = self.History(self.tqqq, 10, Resolution.Daily)
            hist_l = self.History(self.tecl, 10, Resolution.Daily)
            
            if hist_t.empty or hist_l.empty: return
            
            mom_t = (hist_t['close'].iloc[-1] / hist_t['close'].iloc[0]) - 1 if t_bull else -1
            mom_l = (hist_l['close'].iloc[-1] / hist_l['close'].iloc[0]) - 1 if l_bull else -1
            
            best = self.tqqq if mom_t > mom_l else self.tecl
            
            if not self.Portfolio[best].Invested:
                self.Log(f"Trend Buy: {best.Value}. Allocating.")
                self.Liquidate()
                self.SetHoldings(best, 1.0)
        else:
            if self.Portfolio.Invested:
                self.Log("Both below 50-day SMA. Liquidating.")
                self.Liquidate()
