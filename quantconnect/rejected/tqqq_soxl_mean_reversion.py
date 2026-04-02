from datetime import datetime, timedelta
from AlgorithmImports import *

class TQQQSOXLMeanReversion(QCAlgorithm):
    def Initialize(self):
        # 12 year backtest
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.soxl = self.AddEquity("SOXL", Resolution.Daily).Symbol
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        
        self.rsi_tqqq = self.RSI(self.tqqq, 2, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi_soxl = self.RSI(self.soxl, 2, MovingAverageType.Wilders, Resolution.Daily)
        self.sma_spy = self.SMA(self.spy, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.spy), 
                         self.TimeRules.AfterMarketOpen(self.spy, 35), 
                         self.Rebalance)
        
        self.SetWarmUp(200)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma_spy.IsReady:
            return

        spy_price = self.Securities[self.spy].Price
        if spy_price < self.sma_spy.Current.Value:
            if self.Portfolio.Invested:
                self.Liquidate()
            return

        # Bull Market: Selective Mean Reversion
        if self.rsi_tqqq.Current.Value < 15:
            self.SetHoldings(self.tqqq, 0.5)
        elif self.rsi_tqqq.Current.Value > 85:
            self.Liquidate(self.tqqq)
            
        if self.rsi_soxl.Current.Value < 15:
            self.SetHoldings(self.soxl, 0.5)
        elif self.rsi_soxl.Current.Value > 85:
            self.Liquidate(self.soxl)
