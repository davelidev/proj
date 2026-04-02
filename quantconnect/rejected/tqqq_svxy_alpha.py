from datetime import datetime, timedelta
from AlgorithmImports import *

class TQQQSVXYAlpha(QCAlgorithm):
    def Initialize(self):
        # 12 year backtest
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100000)

        # Core Alpha Engines
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.svxy = self.AddEquity("SVXY", Resolution.Daily).Symbol
        
        # Risk Sensors
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        self.vix = self.AddData(CBOE, "VIX", Resolution.Daily).Symbol
        self.vix3m = self.AddData(CBOE, "VIX3M", Resolution.Daily).Symbol
        
        self.sma_spy = self.SMA(self.spy, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.spy), 
                         self.TimeRules.AfterMarketOpen(self.spy, 35), 
                         self.Rebalance)
        
        self.SetWarmUp(200)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma_spy.IsReady:
            return

        # 1. Broad Trend Filter
        spy_bull = self.Securities[self.spy].Price > self.sma_spy.Current.Value
        
        # 2. VIX Term Structure Filter (Contango check)
        if self.Securities.ContainsKey(self.vix) and self.Securities.ContainsKey(self.vix3m):
            vix_ratio = self.Securities[self.vix].Price / self.Securities[self.vix3m].Price
            # Ratio < 0.90 is strong contango
            is_safe = vix_ratio < 0.92
        else:
            is_safe = False
            
        if spy_bull and is_safe:
            if not self.Portfolio.Invested:
                self.Log(f"Risk-ON: Ratio {vix_ratio:.3f}. Bull Market. Allocating to Alpha Engines.")
                self.SetHoldings(self.tqqq, 0.5)
                self.SetHoldings(self.svxy, 0.5)
        else:
            if self.Portfolio.Invested:
                self.Log(f"Risk-OFF: Ratio {vix_ratio:.3f} or Bear Market. Liquidating.")
                self.Liquidate()
