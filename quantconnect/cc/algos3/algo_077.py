from QuantConnect import *
from QuantConnect.Algorithm import QCAlgorithm
from QuantConnect.Data.Market import TradeBar
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

class Algo077(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        # Sector SPDR ETFs representing U.S. equity sectors
        self.sector_etfs = [
            "XLK",  # Technology
            "XLY",  # Consumer Discretionary
            "XLP",  # Consumer Staples
            "XLE",  # Energy
            "XLF",  # Financials
            "XLV",  # Health Care
            "XLI",  # Industrials
            "XLB",  # Materials
            "XLU",  # Utilities
            "XLRE", # Real Estate
            "XLC"   # Communication Services
        ]
        
        self.symbols = []
        for etf in self.sector_etfs:
            symbol = self.AddEquity(etf, Resolution.Daily).Symbol
            self.symbols.append(symbol)
        
        # Schedule monthly rebalance on first trading day after market open
        self.Schedule.On(
            self.DateRules.MonthStart(),
            self.TimeRules.AfterMarketOpen(),
            self.Rebalance
        )
        
        # Warmup period to collect enough history
        self.warmup_period = 378  # 252 days for momentum + 126 days for vol buffer
        
    def Rebalance(self):
        # Ensure we have enough data
        if self.Time < self.StartDate + timedelta(days=self.warmup_period):
            return
        
        # Get price history for all symbols (daily close)
        history = self.History(self.symbols, self.warmup_period, Resolution.Daily)
        if history.empty:
            return
        
        # Unstack to get a DataFrame with columns = symbols, index = time, values = close
        close_prices = history['close'].unstack(level=0)
        # Remove symbols with missing data
        close_prices = close_prices.dropna(axis=1)
        
        if close_prices.empty:
            return
        
        # Current prices (latest row)
        current_prices = close_prices.iloc[-1]
        # Prices 252 trading days ago
        if len(close_prices) < 252:
            return
        past_prices = close_prices.iloc[-252]
        
        # Momentum = (current / past) - 1
        momentum = (current_prices / past_prices) - 1
        
        # Compute annualized volatility (60-day rolling, annualized)
        # We'll use the most recent 60 days of daily returns
        recent_prices = close_prices.iloc[-61:]  # 60 returns
        daily_returns = recent_prices.pct_change().dropna()
        if len(daily_returns) < 60:
            return
        
        # Annualized volatility = std(daily_returns) * sqrt(252)
        vol_series = daily_returns.std() * np.sqrt(252)
        
        # Filter: volatility < 30%
        valid_sectors = vol_series[vol_series < 0.30].index
        
        # Among valid sectors, keep only those with momentum data
        valid_momentum = momentum[valid_sectors].dropna()
        
        if valid_momentum.empty:
            # No sectors qualify, liquidate everything
            self.Liquidate()
            return
        
        # Rank by momentum descending, take top 3
        top_sectors = valid_momentum.sort_values(ascending=False).head(3).index
        
        # Equal weight among selected sectors
        weight = 1.0 / len(top_sectors)
        
        # Set holdings: ensure total weight <= 1.0 (no leverage)
        self.SetHoldings(list(zip(top_sectors, [weight]*len(top_sectors))))
        
        # Optionally, liquidate any positions not in top_sectors
        for symbol in self.symbols:
            if symbol not in top_sectors:
                self.Liquidate(symbol)
