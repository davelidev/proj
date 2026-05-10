import numpy as np
from QuantConnect import *
from QuantConnect.Algorithm import *
from QuantConnect.Data.Market import TradeBar
from QuantConnect.Orders import MarketOrder

class Algo083(QCAlgorithm):
    
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        # Add the five symbols with daily resolution
        self.symbols = ["SPY", "QQQ", "IWM", "EEM", "TLT"]
        for symbol in self.symbols:
            self.AddEquity(symbol, Resolution.Daily)
        
        # Warmup period to calculate relative strength on first rebalance
        self.SetWarmup(252)
        
        # Rebalance monthly on the first trading day after market open
        self.Schedule.On(
            self.DateRules.MonthStart("SPY"),
            self.TimeRules.AfterMarketOpen("SPY", 30)
        )
        
        # Number of top performers to hold
        self.top_n = 2
        
        # Keep track of current month to avoid multiple rebalances per month
        self.last_month = -1
        
    def OnData(self, data):
        # We handle rebalancing via scheduled events, not on each data point
        pass
    
    def OnEndOfDay(self):
        # Use end of day to trigger scheduled rebalance logic
        if self.IsWarmingUp:
            return
        
        # Get current UTC time, convert to Eastern
        current_time = self.Time
        if current_time.month == self.last_month:
            return
        self.last_month = current_time.month
        
        # Run rebalance only on the first trading day of the month
        calendar = self.TradingCalendar
        trading_days = calendar.GetDaysByType(TradingDayType.BusinessDay, current_time, current_time)
        if len(trading_days) == 0 or trading_days[0].Date != current_time.date():
            return
        
        self.Rebalance()
    
    def Rebalance(self):
        # Get 252-day historical close prices for all symbols
        lookback = 252
        history = self.History(self.symbols, lookback + 1, Resolution.Daily)
        if history.empty:
            return
        
        # Get the latest close for each symbol
        current_prices = {}
        for symbol_str in self.symbols:
            symbol = self.Symbol(symbol_str)
            if symbol in history.index.levels[0]:
                data = history.loc[symbol]
                if len(data) >= lookback + 1:
                    current_price = data['close'].iloc[-1]
                    past_price = data['close'].iloc[0]
                    if past_price != 0:
                        roc = (current_price / past_price) - 1
                    else:
                        roc = 0
                    current_prices[symbol] = roc
        
        if not current_prices:
            return
        
        # Filter symbols with positive relative strength (ROC > 0)
        positive_roc = {sym: roc for sym, roc in current_prices.items() if roc > 0}
        
        # Sort by ROC descending
        sorted_symbols = sorted(positive_roc.items(), key=lambda x: x[1], reverse=True)
        
        # Select top N symbols (or all if fewer)
        selected = [sym for sym, _ in sorted_symbols[:self.top_n]]
        
        # Determine target weights
        if not selected:
            # No positive performers -> go to cash
            invested = [x.Key for x in self.Portfolio if x.Value.Invested]
            for sym in invested:
                self.Liquidate(sym)
            return
        
        # Equal weight among selected symbols
        weight = 1.0 / len(selected)
        
        # Ensure weights don't exceed 1.0 (already satisfied)
        total_weight = weight * len(selected)
        if total_weight > 1.0:
            # Scale down proportionally (shouldn't happen with equal weight if no leverage)
            weight = 1.0 / len(selected)
        
        # Liquidate any holdings not in selected
        for symbol in self.symbols:
            sym = self.Symbol(symbol)
            if sym in self.Portfolio.Keys:
                holding = self.Portfolio[sym]
                if holding.Invested and sym not in selected:
                    self.Liquidate(sym)
        
        # Set holdings for selected symbols
        for symbol in selected:
            self.SetHoldings(symbol, weight)