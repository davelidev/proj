# region imports
from AlgorithmImports import *
import numpy as np
from scipy.stats import linregress
# endregion

class ClenowStocksOnTheMove(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2023, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        # Strategy Parameters
        self.lookback = 90
        self.atr_period = 20
        self.sma_period = 100
        self.market_sma_period = 200
        self.risk_factor = 0.001 # 10 basis points (0.1%)
        self.max_gap = 0.15      # 15% max gap filter
        self.top_percent = 0.20  # Buy from top 20% of ranked stocks
        
        self.SetWarmUp(self.market_sma_period)
        
        # Market Regime Indicator (S&P 500)
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        self.market_sma = self.SMA(self.spy, self.market_sma_period, Resolution.Daily)
        
        # Universe Selection: S&P 500-like universe
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelectionFunction)
        
        self.universe_symbols = []
        
        # Schedule rebalancing for every Wednesday
        self.Schedule.On(self.DateRules.Every(DayOfWeek.Wednesday), 
                         self.TimeRules.AfterMarketOpen(self.spy, 30), 
                         self.Rebalance)

    def CoarseSelectionFunction(self, coarse):
        # Filter for stocks with fundamental data and high dollar volume
        sorted_by_volume = sorted([x for x in coarse if x.HasFundamentalData], 
                                  key=lambda x: x.DollarVolume, reverse=True)
        self.universe_symbols = [x.Symbol for x in sorted_by_volume[:500]]
        return self.universe_symbols

    def Rebalance(self):
        self.Debug(f"Rebalance triggered at {self.Time}")
        if self.IsWarmingUp:
            self.Debug("Still warming up...")
            return
            
        if not self.market_sma.IsReady:
            self.Debug("Market SMA not ready.")
            return

        # 1. Market Regime Filter
        is_bull_market = self.Securities[self.spy].Price > self.market_sma.Current.Value
        self.Debug(f"Bull Market: {is_bull_market} (Price: {self.Securities[self.spy].Price}, SMA: {self.market_sma.Current.Value})")
        
        symbols_to_process = self.universe_symbols
        self.Debug(f"Symbols in universe: {len(symbols_to_process)}")
        
        if not symbols_to_process:
            self.Debug("Universe symbols list is empty. Checking ActiveSecurities...")
            symbols_to_process = [s for s in self.ActiveSecurities.Keys if s != self.spy]
            self.Debug(f"ActiveSecurities count: {len(symbols_to_process)}")

        if not symbols_to_process:
            return

        # 2. Calculate Momentum and Apply Filters
        rankings = []
        for symbol in symbols_to_process:
            try:
                history = self.History(symbol, self.lookback + 1, Resolution.Daily)
                if history.empty or 'close' not in history.columns or len(history) < self.lookback:
                    continue
                
                prices = history['close'].values
                
                # Gap Filter
                returns = np.diff(prices) / prices[:-1]
                if len(returns) > 0 and np.max(np.abs(returns)) > self.max_gap:
                    continue
                    
                # Trend Filter
                sma_100 = np.mean(prices[-self.sma_period:])
                if prices[-1] < sma_100:
                    continue
                
                # Momentum Calculation
                log_prices = np.log(prices)
                x = np.arange(len(log_prices))
                slope, intercept, r_value, p_value, std_err = linregress(x, log_prices)
                
                annualized_slope = (np.exp(slope) ** 252) - 1
                adjusted_slope = annualized_slope * (r_value ** 2)
                
                rankings.append({
                    'symbol': symbol,
                    'slope': adjusted_slope,
                    'price': prices[-1]
                })
            except Exception as e:
                self.Debug(f"Error processing {symbol}: {str(e)}")
                continue

        self.Debug(f"Eligible stocks: {len(rankings)}")

        # 3. Rank stocks by Adjusted Slope
        rankings = sorted(rankings, key=lambda x: x['slope'], reverse=True)
        num_to_rank = int(len(rankings) * self.top_percent)
        top_symbols = [x['symbol'] for x in rankings[:num_to_rank]]

        # 4. Sell Logic: Liquidate if stock falls out of top 20% or market turns bearish
        for symbol in list(self.Portfolio.Keys):
            if symbol == self.spy: continue
            
            # Sell if not in top 20% or if market turns bearish
            if symbol not in top_symbols or not is_bull_market:
                self.Liquidate(symbol)

        # 5. Buy Logic: Only if market is bullish
        if is_bull_market:
            for stock in rankings[:num_to_rank]:
                symbol = stock['symbol']
                
                # Skip if already in portfolio
                if self.Portfolio[symbol].Invested:
                    continue
                
                # Calculate ATR for position sizing
                history_atr = self.History(symbol, self.atr_period + 1, Resolution.Daily)
                if history_atr.empty or len(history_atr) < self.atr_period:
                    continue
                
                if not all(col in history_atr.columns for col in ['high', 'low', 'close']): continue
                
                high = history_atr['high'].values
                low = history_atr['low'].values
                close = history_atr['close'].values
                
                # True Range calculation
                tr = np.maximum(high[1:] - low[1:], 
                                np.maximum(np.abs(high[1:] - close[:-1]), 
                                           np.abs(low[1:] - close[:-1])))
                atr = np.mean(tr)
                
                if atr == 0: continue
                
                # Position Sizing: (Portfolio Value * 0.1%) / ATR
                target_shares = (self.Portfolio.TotalPortfolioValue * self.risk_factor) / atr
                
                # Safety check: Max 10% allocation per stock
                max_shares = (self.Portfolio.TotalPortfolioValue * 0.1) / stock['price']
                target_shares = min(target_shares, max_shares)
                
                if target_shares > 0:
                    self.MarketOrder(symbol, int(target_shares))

    def OnData(self, data):
        pass
