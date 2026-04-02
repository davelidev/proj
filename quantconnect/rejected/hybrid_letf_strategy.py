from datetime import datetime, timedelta
from AlgorithmImports import *

class HybridLETFStrategy(QCAlgorithm):
    def Initialize(self):
        # 12 year backtest
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100000)

        # Core offensive LETFs
        self.offensive = ["TQQQ", "SOXL", "TECL"]
        self.defensive = ["IEF"]
        self.spy = "SPY"
        self.qqq = "QQQ"
        
        self.symbols = {}
        for ticker in self.offensive + self.defensive + [self.spy, self.qqq]:
            self.symbols[ticker] = self.AddEquity(ticker, Resolution.Daily).Symbol

        # Indicators
        self.sma_spy = self.SMA(self.symbols[self.spy], 200, Resolution.Daily)
        self.rsi_qqq = self.RSI(self.symbols[self.qqq], 2, MovingAverageType.Wilders, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.spy), 
                         self.TimeRules.AfterMarketOpen(self.spy, 35), 
                         self.Rebalance)
        
        self.SetWarmUp(200)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma_spy.IsReady or not self.rsi_qqq.IsReady:
            return

        spy_price = self.Securities[self.symbols[self.spy]].Price
        rsi_value = self.rsi_qqq.Current.Value
        
        # Hybrid Logic:
        # 1. Broad Trend: SPY > 200 SMA (Avoid major bear markets)
        # 2. Local Dip: RSI(2) < 30 (Buy the fear)
        
        is_bull_market = spy_price > self.sma_spy.Current.Value
        is_oversold = rsi_value < 30
        
        if is_bull_market:
            if is_oversold:
                # Buy aggressively during dips in a bull market
                self.Log(f"Bull Market Dip: RSI {rsi_value:.2f}. Going 100% Offensive.")
                for ticker in self.offensive:
                    self.SetHoldings(self.symbols[ticker], 1.0 / len(self.offensive))
            else:
                # In a bull market but not oversold - hold moderate position
                # or stay in defensive to avoid volatility decay? 
                # Let's try staying in offensive but maybe 50/50 with defensive to reduce DD
                self.Log(f"Bull Market Trend: RSI {rsi_value:.2f}. 50% Offensive, 50% Defensive.")
                for ticker in self.offensive:
                    self.SetHoldings(self.symbols[ticker], 0.5 / len(self.offensive))
                self.SetHoldings(self.symbols["IEF"], 0.5)
        else:
            # Bear Market: Stay Defensive
            if not self.Portfolio[self.symbols["IEF"]].Invested:
                self.Log(f"Bear Market: RSI {rsi_value:.2f}. Switching to Defensive.")
                self.Liquidate()
                self.SetHoldings(self.symbols["IEF"], 1.0)
