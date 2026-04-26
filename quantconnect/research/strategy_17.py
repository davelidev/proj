from datetime import datetime, timedelta
from AlgorithmImports import *

class TQQQUltimateOscillator(QCAlgorithm):
    def Initialize(self):
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100_000)
        self.SetBenchmark("QQQ")
        
        self.sym = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        
        self.ult = self.ULTOSC(self.sym, 7, 14, 28, Resolution.Daily)
        self.sma200 = self.SMA(self.qqq, 200, Resolution.Daily)
        self.rsi2 = self.RSI(self.sym, 2, MovingAverageType.Wilders, Resolution.Daily)
        
        self.SetWarmUp(200, Resolution.Daily)

    def OnData(self, data):
        if self.IsWarmingUp or not self.ult.IsReady or not self.sma200.IsReady:
            return

        price = self.Securities[self.sym].Price
        qqq_price = self.Securities[self.qqq].Price
        s200 = self.sma200.Current.Value
        ult_val = self.ult.Current.Value
        r2 = self.rsi2.Current.Value

        if not self.Portfolio.Invested:
            # Ultimate Oscillator < 30 is extremely oversold, coupled with bull market
            if qqq_price > s200 and ult_val < 30:
                self.SetHoldings(self.sym, 1.0)
        else:
            # Fast exit on bounce (RSI2 > 70) or trend break
            if r2 > 70 or qqq_price < s200:
                self.Liquidate(self.sym)
