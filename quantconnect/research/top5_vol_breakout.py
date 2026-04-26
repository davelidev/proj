from datetime import datetime, timedelta
from AlgorithmImports import *

class Top5VolBreakout(QCAlgorithm):
    def Initialize(self):
        # Parameters for optimization
        self.lookback = 20
        self.vol_lookback = 10
        self.vol_threshold = 0.02 # 2% daily range
        
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100_000)
        
        # Top 5 Market Cap Universe (Updated annually in logic)
        self.tickers = ["AAPL", "MSFT", "AMZN", "GOOGL", "NVDA"]
        self.symbols = [self.AddEquity(t, Resolution.Daily).Symbol for t in self.tickers]
        
        # Indicators for each stock
        self.highs = {s: self.MAX(s, self.lookback, Resolution.Daily) for s in self.symbols}
        self.atrs = {s: self.ATR(s, self.vol_lookback, MovingAverageType.Wilders, Resolution.Daily) for s in self.symbols}
        
        self.SetWarmUp(self.lookback, Resolution.Daily)
        
        # Annual Rebalance Schedule
        self.Schedule.On(self.DateRules.MonthStart(), self.TimeRules.AfterMarketOpen("AAPL", 30), self.Rebalance)

    def Rebalance(self):
        # Even distribution of 20% each for any that are in a breakout state
        # Or simply rotate annually to the newest Top 5 (manual update for this research)
        if self.Time.month == 1:
            self.Debug(f"Annual Rebalance Check at {self.Time}")

    def OnData(self, data):
        if self.IsWarmingUp: return
        
        for s in self.symbols:
            if not data.ContainsKey(s) or data[s] is None: continue
            
            price = self.Securities[s].Price
            recent_high = self.highs[s].Current.Value
            atr = self.atrs[s].Current.Value
            
            # Volatility Breakout Logic:
            # 1. Price is at or above a 20-day high (Breakout)
            # 2. Volatility (ATR) is expanding relative to price (Momentum confirmed)
            if not self.Portfolio[s].Invested:
                if price >= recent_high and atr > (price * 0.02):
                    self.SetHoldings(s, 0.20) # 20% per stock
            else:
                # Exit if price drops below 20-day high - 2*ATR (Trailing Stop)
                if price < (recent_high - (2 * atr)):
                    self.Liquidate(s)
