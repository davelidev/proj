from datetime import datetime, timedelta
from AlgorithmImports import *

class VolSpikeReversion(QCAlgorithm):
    def Initialize(self):
        # 12 year backtest
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.vix = self.AddData(CBOE, "VIX", Resolution.Daily).Symbol
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        
        # Indicators
        self.sma_vix = self.SMA(self.vix, 10, Resolution.Daily)
        self.sma_spy = self.SMA(self.spy, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq), 
                         self.TimeRules.AfterMarketOpen(self.tqqq, 35), 
                         self.Rebalance)
        
        self.SetWarmUp(200)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma_vix.IsReady or not self.sma_spy.IsReady:
            return

        vix_price = self.Securities[self.vix].Price
        spy_price = self.Securities[self.spy].Price
        
        # Logic: Buy the panic.
        # If VIX is 20% above its 10-day SMA, it's a spike.
        is_spike = vix_price > self.sma_vix.Current.Value * 1.20
        is_bull = spy_price > self.sma_spy.Current.Value
        
        if is_spike and is_bull:
            if not self.Portfolio[self.tqqq].Invested:
                self.Log(f"VIX Spike: {vix_price:.2f} > {self.sma_vix.Current.Value:.2f} * 1.2. Buying TQQQ.")
                self.SetHoldings(self.tqqq, 1.0)
        elif self.Portfolio[self.tqqq].Invested:
            # Exit when VIX calms down below its SMA
            if vix_price < self.sma_vix.Current.Value:
                self.Log(f"VIX Calmed: {vix_price:.2f} < {self.sma_vix.Current.Value:.2f}. Liquidating.")
                self.Liquidate()
