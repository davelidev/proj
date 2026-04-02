from datetime import datetime, timedelta
from AlgorithmImports import *

class VIXTermStructureLeveraged(QCAlgorithm):
    def Initialize(self):
        # 12 year backtest
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100000)

        # Assets
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.svxy = self.AddEquity("SVXY", Resolution.Daily).Symbol
        
        # VIX Index and VXV (3-month VIX proxy)
        # On QuantConnect, VXV is often available as "VIX3M"
        self.vix = self.AddData(CBOE, "VIX", Resolution.Daily).Symbol
        self.vix3m = self.AddData(CBOE, "VIX3M", Resolution.Daily).Symbol
        
        # Strategy Parameters
        self.ratio_threshold = 0.95 # VIX/VIX3M ratio < 0.95 indicates contango
        self.exit_ratio = 1.00      # VIX/VIX3M ratio > 1.00 indicates backwardation
        
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq), 
                         self.TimeRules.AfterMarketOpen(self.tqqq, 35), 
                         self.Rebalance)
        
        self.SetWarmUp(30)

    def Rebalance(self):
        if not (self.Securities.ContainsKey(self.vix) and self.Securities.ContainsKey(self.vix3m)):
            return
            
        vix_price = self.Securities[self.vix].Price
        vix3m_price = self.Securities[self.vix3m].Price
        
        if vix_price == 0 or vix3m_price == 0:
            return
            
        # VIX / VIX3M Ratio
        # Lower ratio = More Contango = Risk On
        # Higher ratio = Backwardation = Risk Off
        ratio = vix_price / vix3m_price
        self.Plot("VIX Ratio", "Ratio", ratio)

        if ratio < self.ratio_threshold:
            if not self.Portfolio.Invested:
                self.Log(f"Risk-On: VIX Ratio {ratio:.3f}. Buying TQQQ and SVXY.")
                self.SetHoldings(self.tqqq, 0.5)
                self.SetHoldings(self.svxy, 0.5)
        elif ratio > self.exit_ratio:
            if self.Portfolio.Invested:
                self.Log(f"Risk-Off: VIX Ratio {ratio:.3f}. Liquidating to Cash.")
                self.Liquidate()
