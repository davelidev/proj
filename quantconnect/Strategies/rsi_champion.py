from datetime import datetime, timedelta
from AlgorithmImports import *                                                                                        
 
class RSIDipChampion(QCAlgorithm):                                                                               
                                                                
    def Initialize(self):
        
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.SetBenchmark("QQQ")
        
        self.aggressive = ["TQQQ", "SOXL", "TECL"]
        
        for ticker in set(self.aggressive + ['QQQ']):
            self.AddEquity(ticker, Resolution.Daily)
            
        # RSI(2) on QQQ for regime signal
        self.qqq_rsi2 = self.RSI("QQQ", 2, MovingAverageType.Wilders, Resolution.Daily)
        
        self.Schedule.On(
            self.DateRules.EveryDay("QQQ"),
            self.TimeRules.AfterMarketOpen("QQQ", 35),
            self.Rebalance,
        )
        self.is_long = None

    def Rebalance(self):
        if not self.qqq_rsi2.IsReady:
            return
        
        prev_is_long = self.is_long
        # Trigger: QQQ is extremely oversold
        self.is_long = self.qqq_rsi2.Current.Value < 25
        
        if prev_is_long != self.is_long:
            self.Liquidate()
            if self.is_long:
                # Enter aggressive growth basket
                for ticker in self.aggressive:
                    self.SetHoldings(ticker, 1 / len(self.aggressive))
            # If not long, we stay in Cash (Liquidated)
