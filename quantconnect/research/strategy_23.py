from datetime import datetime, timedelta
from AlgorithmImports import *

class MegaCapTrendShield(QCAlgorithm):
    def Initialize(self):
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100_000)
        
        # Mega-Cap Tech (More stable than mid-cap)
        self.tickers = ["AAPL", "MSFT", "GOOGL", "AMZN"]
        self.symbols = [self.AddEquity(t, Resolution.Daily).Symbol for t in self.tickers]
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        
        # Protective Indicators
        self.sma200 = self.SMA(self.qqq, 200, Resolution.Daily)
        self.sma20 = self.SMA(self.qqq, 20, Resolution.Daily)
        self.rsi2 = {s: self.RSI(s, 2, MovingAverageType.Wilders, Resolution.Daily) for s in self.symbols}
        
        self.SetWarmUp(200, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.AfterMarketOpen("TQQQ", 30), self.Rebalance)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma200.IsReady: return
        
        qqq_price = self.Securities[self.qqq].Price
        sma200_val = self.sma200.Current.Value
        sma20_val = self.sma20.Current.Value
        
        # THE SHIELD: structural bull market AND short-term trend is not broken
        is_shield_up = qqq_price > sma200_val and qqq_price > sma20_val
        
        if is_shield_up:
            if not self.Portfolio.Invested:
                # Buy on any Mega-Cap dip
                oversold = [s for s in self.symbols if self.rsi2[s].Current.Value < 25]
                if oversold:
                    self.SetHoldings(self.tqqq, 1.0)
                    self.Debug(f"SHIELD ENTRY at {qqq_price}")
            else:
                # Fast Profit Taking on QQQ recovery
                if self.RSI(self.qqq, 2).Current.Value > 75:
                    self.Liquidate()
        else:
            # Hard Exit if trend breaks
            self.Liquidate()
            self.Debug(f"SHIELD EXIT: Trend Break at {qqq_price}")
