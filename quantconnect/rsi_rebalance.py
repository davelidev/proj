from AlgorithmImports import *                                                                                        
 
class RSI2LeveragedETFsV3(QCAlgorithm):                                                                               
                                                                
    def Initialize(self):
        self.SetStartDate(2012, 1, 1)
        self.SetCash(100000)
        self.SetBenchmark("QQQ")
        self.aggressive = ["TQQQ", "SOXL", "TECL"]
        self.defensive = ["BSV", "TLT", "LQD", "VBF", "XLP", "UGE", "XLU", "XLV", "SPAB", "ANGL"]
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

    def Rebalance(self):
        if not self.qqq_rsi2.IsReady:
            return
        if self.qqq_rsi2.Current.Value < 20:
            # Aggressive regime: equal-weight leveraged ETFs
            targets = {t: 1.0 / len(self.aggressive) for t in self.aggressive}
        else:
            # Defensive regime: pick the single most oversold asset (lowest RSI-10)
            ready = {t: rsi for t, rsi in self.defensive_rsi10.items() if rsi.IsReady}
            if not ready:
                return
            selected = min(ready, key=lambda t: ready[t].Current.Value)
            targets = {selected: 1.0}
        # Liquidate anything not in targets, then set targets
        for ticker in set(self.aggressive + self.defensive):
            if ticker not in targets:
                self.Liquidate(ticker)
        for ticker, weight in targets.items():
            self.SetHoldings(ticker, weight)
