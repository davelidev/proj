from datetime import datetime, timedelta
from AlgorithmImports import *

class LSMeanReversion(QCAlgorithm):
    def Initialize(self):
        # 12 year backtest
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.sqqq = self.AddEquity("SQQQ", Resolution.Daily).Symbol
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        
        # Indicators
        self.rsi_tqqq = self.RSI(self.tqqq, 2, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi_sqqq = self.RSI(self.sqqq, 2, MovingAverageType.Wilders, Resolution.Daily)
        self.sma_spy = self.SMA(self.spy, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.spy), 
                         self.TimeRules.AfterMarketOpen(self.spy, 35), 
                         self.Rebalance)
        
        self.SetWarmUp(200)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma_spy.IsReady or not self.rsi_tqqq.IsReady:
            return

        spy_price = self.Securities[self.spy].Price
        is_bull = spy_price > self.sma_spy.Current.Value
        
        rsi_t = self.rsi_tqqq.Current.Value
        rsi_s = self.rsi_sqqq.Current.Value
        
        # Logic:
        # In Bull Market: Buy TQQQ when RSI(2) < 25 (oversold)
        # In Bear Market: Buy SQQQ when RSI(2) < 25 (meaning TQQQ is extremely overbought in a crash rally)
        # OR: Buy SQQQ when TQQQ RSI(2) > 75
        
        if is_bull:
            if rsi_t < 25:
                self.Log(f"Bull Market Dip: TQQQ RSI {rsi_t:.2f}. Buying TQQQ.")
                self.SetHoldings(self.tqqq, 1.0, liquidateExistingHoldings=True)
            elif rsi_t > 80:
                self.Log(f"Bull Market Peak: TQQQ RSI {rsi_t:.2f}. Exiting to Cash.")
                self.Liquidate()
        else:
            # Bear Market
            if rsi_t > 75:
                self.Log(f"Bear Market Rally: TQQQ RSI {rsi_t:.2f}. Buying SQQQ.")
                self.SetHoldings(self.sqqq, 1.0, liquidateExistingHoldings=True)
            elif rsi_t < 30:
                self.Log(f"Bear Market Flush: TQQQ RSI {rsi_t:.2f}. Exiting to Cash.")
                self.Liquidate()
