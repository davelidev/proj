from System.Collections.Generic import List
from AlgorithmImports import *
import numpy as np
import pandas as pd

class Algo043(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        
        # Resolution for all added securities
        self.UniverseSettings.Resolution = Resolution.Daily
        
        # Add TQQQ (hardcoded exception)
        self.tqqq = self.AddEquity('TQQQ', Resolution.Daily).Symbol
        
        # Dynamic mega-cap universe (top 10 by market cap)
        self.AddUniverse(self.CoarseSelectionFunction)
        
        # Basket to hold all symbols including TQQQ
        self.basket = {}  # Symbol -> dict with additional data if needed
        
        # Initialize basket with TQQQ
        self.basket[self.tqqq] = {}
        
        # Minimum days of history required for signals
        self.min_history = 252  # enough for 3-month momentum + correlation
        
        # Schedule daily rebalance at market open (optional, OnData works too)
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq), 
                         self.TimeRules.AfterMarketOpen(self.tqqq, 10),
                         self.Rebalance)
        
        # For debugging
        self.rebalance_days = 0
    
    def CoarseSelectionFunction(self, coarse):
        # Filter for US equities with fundamental data and positive price
        filtered = [c for c in coarse if c.HasFundamentalData and c.Price > 0]
        # Sort by market cap descending, take top 10
        sorted_by_mc = sorted(filtered, key=lambda c: c.MarketCap, reverse=True)
        top10 = [c.Symbol for c in sorted_by_mc[:10]]
        return top10
    
    def OnSecuritiesChanged(self, changes):
        # Update basket: add new symbols, remove old ones
        for added in changes.AddedSecurities:
            sym = added.Symbol
            if sym not in self.basket:
                self.basket[sym] = {}
                self.Debug(f"Added {sym} to basket")
        for removed in changes.RemovedSecurities:
            sym = removed.Symbol
            if sym in self.basket:
                del self.basket[sym]
                self.Debug(f"Removed {sym} from basket")
    
    def Rebalance(self):
        """Main rebalance logic, called daily after market open."""
        symbols = list(self.basket.keys())
        if len(symbols) < 2:
            return
        
        # Request history for all symbols (long enough for all signals)
        history = self.History(symbols, self.min_history, Resolution.Daily)
        if history.empty:
            return
        
        # Unstack to get close prices (Symbol x Date)
        close = history['close'].unstack(level=0).dropna(how='any', axis=0)
        if close.empty:
            return
        
        # Need at least 63 days for momentum
        if len(close) < 63:
            return
        
        # Current date slice
        today = self.Time.date()
        if today not in close.index:
            return
        
        # Align to today
        prices = close.loc[:today]
        
        # 1. Momentum (3-month returns = 63 trading days)
        momentum = (prices.iloc[-1] / prices.iloc[-63] - 1).dropna()
        if momentum.empty:
            return
        
        # 2. Correlation with TQQQ (63-day rolling correlation of daily returns)
        returns = prices.pct_change().dropna()
        # Ensure TQQQ is in returns
        if self.tqqq not in returns.columns:
            return
        tqqq_ret = returns[self.tqqq].iloc[-63:]
        correlation = {}
        for sym in returns.columns:
            if sym == self.tqqq:
                correlation[sym] = 1.0
            else:
                sym_ret = returns[sym].iloc[-63:]
                if len(sym_ret) >= 63:
                    corr = np.corrcoef(tqqq_ret, sym_ret)[0,1]
                    correlation[sym] = corr if not np.isnan(corr) else 0.0
                else:
                    correlation[sym] = 0.0
        
        # 3. Dispersion: cross-sectional standard deviation of momentum values
        momentum_series = momentum.drop(self.tqqq, errors='ignore')  # exclude TQQQ? or include
        # We'll compute dispersion over all basket symbols
        dispersion = momentum.std()  # standard deviation across symbols
        
        # 4. Seasonality: average monthly return over past 12 months
        monthly_returns = prices.resample('M').apply(lambda x: x.iloc[-1] / x.iloc[0] - 1)
        monthly_returns = monthly_returns.iloc[-12:]  # last 12 months
        avg_monthly_return = monthly_returns.mean()
        
        # 5. Regime detection: TQQQ above 200-day SMA
        sma200 = prices[self.tqqq].rolling(200).mean().iloc[-1]
        regime_bullish = prices[self.tqqq].iloc[-1] > sma200
        
        # --- Combine signals to adjust sizing ---
        # Base weights: momentum-ranked, top 3, proportional to momentum
        sorted_mom = momentum.sort_values(ascending=False)
        top3 = sorted_mom.head(3)
        if len(top3) == 0:
            return
        # Weight proportional to momentum magnitude (positive only)
        pos_mom = top3[top3 > 0]
        if pos_mom.empty:
            # If all momentum negative, still pick smallest negative? Use absolute momentum? 
            # Strategy says "weight by 3mo momentum", assume positive only. If not, skip.
            self.Liquidate()
            return
        raw_weights = pos_mom / pos_mom.sum()
        
        # Dynamic sizing factor based on regime, correlation, dispersion
        factor = 1.0
        
        # Regime: reduce if bearish
        if not regime_bullish:
            factor *= 0.5
        
        # Dispersion: high dispersion (≥0.2) reduces factor
        if dispersion >= 0.2:
            factor *= 0.7
        
        # Correlation: if average correlation with TQQQ is very negative (market panic), reduce
        avg_corr = np.mean([correlation[sym] for sym in pos_mom.index])
        if avg_corr < -0.3:
            factor *= 0.8
        
        # Apply factor to weights
        scaled_weights = raw_weights * factor
        # Ensure sum <= 1 (no leverage)
        total_weight = scaled_weights.sum()
        if total_weight > 1.0:
            scaled_weights = scaled_weights / total_weight  # scale down to 1
        elif total_weight <= 0:
            self.Liquidate()
            return
        
        # Liquidate positions not in top3
        current_holdings = [s.Key for s in self.Portfolio if s.Value.Invested]
        for sym in current_holdings:
            if sym not in pos_mom.index:
                self.Liquidate(sym)
        
        # Set holdings
        for sym, weight in scaled_weights.items():
            if weight > 0:
                self.SetHoldings(sym, weight)
        
        self.rebalance_days += 1
        self.Debug(f"{today} Rebalanced. Top3: {[str(s) for s in pos_mom.index]}, weights: {scaled_weights.values}")
    
    def OnData(self, data):
        """OnData is not used for rebalance (scheduled event handles it)."""
        pass
