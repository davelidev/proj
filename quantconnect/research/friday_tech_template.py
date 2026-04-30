from datetime import datetime, timedelta
from AlgorithmImports import *

class FridayTechBreakout(QCAlgorithm):
    def Initialize(self):
        # Parameters (provided via API)
        self.bbars = int(self.GetParameter("bbars", 25))
        self.vix_shield = float(self.GetParameter("vix_shield", 28))
        self.exit_days = int(self.GetParameter("exit_days", 4))
        self.holdings_pct = 1.0
        
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        
        # Big Cap Tech Basket
        self.tickers = ["AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA", "NVDA", "AVGO", "ADBE", "CRM"]
        self.symbols = []
        for ticker in self.tickers:
            self.symbols.append(self.AddEquity(ticker, Resolution.Daily).Symbol)
            
        self.vix = self.AddData(CBOE, "VIX").Symbol
        
        # Indicators for each stock
        self.highs = {}
        for symbol in self.symbols:
            self.highs[symbol] = self.MAX(symbol, self.bbars, Resolution.Daily)
            
        self.SetWarmUp(self.bbars, Resolution.Daily)
        
        # State tracking
        self.trigger_on_friday = {symbol: False for symbol in self.symbols}
        self.entry_dates = {symbol: datetime.min for symbol in self.symbols}

        # Schedule rebalance checks
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.AfterMarketOpen("AAPL", 10), self.CheckSignals)

    def CheckSignals(self):
        if self.IsWarmingUp: return
        
        vix_val = self.Securities[self.vix].Price
        day = self.Time.weekday() # 0=Mon, 4=Fri
        
        # 1. Friday: Check for Breakouts
        if day == 4:
            for symbol in self.symbols:
                price = self.Securities[symbol].Price
                if price >= self.highs[symbol].Current.Value and vix_val < self.vix_shield:
                    self.trigger_on_friday[symbol] = True
                else:
                    self.trigger_on_friday[symbol] = False
        
        # 2. Monday: Enter if triggered
        if day == 0:
            invested_count = len([s for s in self.symbols if self.Portfolio[s].Invested])
            if invested_count == 0: # Only enter if not already rotating
                triggered = [s for s, t in self.trigger_on_friday.items() if t]
                if triggered:
                    # Allocate equally among triggered stocks
                    weight = self.holdings_pct / len(triggered)
                    for symbol in triggered:
                        self.SetHoldings(symbol, weight)
                        self.entry_dates[symbol] = self.Time
                        self.trigger_on_friday[symbol] = False

        # 3. Exit Check (Timed Exit)
        for symbol in self.symbols:
            if self.Portfolio[symbol].Invested:
                days_held = (self.Time - self.entry_dates[symbol]).days
                if days_held >= self.exit_days:
                    self.Liquidate(symbol)
