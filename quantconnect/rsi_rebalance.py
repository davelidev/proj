from AlgorithmImports import *                                                                                        
 
class DualRegimeRSIRotation(QCAlgorithm):                                                                               
                                                                
    def Initialize(self):
        self.SetStartDate(2015, 1, 1)
        self.SetCash(100000)
        self.SetBenchmark("QQQ")
        self.aggressive = ["TQQQ", "SOXL", "TECL"]
        self.defensive = ["TLT", "GLD", "IEF", "AGG", "BND", "SGOV", "BSV"]
        for ticker in set(self.aggressive + self.defensive + ['QQQ']):
            self.AddEquity(ticker, Resolution.Daily)
        # RSI(2) on TQQQ for regime signal
        self.qqq_rsi2 = self.RSI("QQQ", 2, MovingAverageType.Wilders, Resolution.Daily)
        # RSI(10) on each defensive asset for ranking
        self.defensive_rsi10 = {
            ticker: self.RSI(ticker, 10, MovingAverageType.Wilders, Resolution.Daily)
            for ticker in self.defensive
        }
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
        self.is_long = self.qqq_rsi2.Current.Value < 25
        
        if prev_is_long != self.is_long:
            self.Liquidate()
            if self.is_long:
                for ticker in self.aggressive:
                    self.SetHoldings(ticker, 1 / len(self.aggressive))
            else:
                return
                ready = {t: rsi for t, rsi in self.defensive_rsi10.items() if rsi.IsReady}
                if selected := min(ready, key=lambda t: ready[t].Current.Value, default=None):
                    self.SetHoldings(selected, 1)
