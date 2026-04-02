from datetime import datetime, timedelta
from AlgorithmImports import *

class TQQQSQQQMacro(QCAlgorithm):
    def Initialize(self):
        # 12 year backtest
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.sqqq = self.AddEquity("SQQQ", Resolution.Daily).Symbol
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        
        self.sma_spy = self.SMA(self.spy, 200, Resolution.Daily)
        self.rsi_tqqq = self.RSI(self.tqqq, 2, MovingAverageType.Wilders, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.spy), 
                         self.TimeRules.AfterMarketOpen(self.spy, 35), 
                         self.Rebalance)
        
        self.SetWarmUp(200)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma_spy.IsReady:
            return

        spy_price = self.Securities[self.spy].Price
        is_bull = spy_price > self.sma_spy.Current.Value
        
        if is_bull:
            # Bull Market: Buy TQQQ on dips
            if self.rsi_tqqq.Current.Value < 40:
                if not self.Portfolio[self.tqqq].Invested:
                    self.Log(f"Bull Market Dip. Buying TQQQ.")
                    self.Liquidate()
                    self.SetHoldings(self.tqqq, 1.0)
            elif self.rsi_tqqq.Current.Value > 80:
                # Overbought in bull market: move to cash to lock in gains
                if self.Portfolio[self.tqqq].Invested:
                    self.Log("Bull Market Overbought. Exiting to cash.")
                    self.Liquidate()
        else:
            # Bear Market: Opportunistic SQQQ (shorts)
            if self.rsi_tqqq.Current.Value > 70:
                # Rally in bear market: enter SQQQ
                if not self.Portfolio[self.sqqq].Invested:
                    self.Log("Bear Market Rally. Buying SQQQ.")
                    self.Liquidate()
                    self.SetHoldings(self.sqqq, 1.0)
            elif self.rsi_tqqq.Current.Value < 30:
                # Flush in bear market: exit SQQQ
                if self.Portfolio[self.sqqq].Invested:
                    self.Log("Bear Market Flush. Exiting to cash.")
                    self.Liquidate()
