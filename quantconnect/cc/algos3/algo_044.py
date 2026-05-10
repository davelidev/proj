from System import *
from QuantConnect import *
from QuantConnect.Algorithm import *
from QuantConnect.Indicators import *
from QuantConnect.Data.Market import TradeBar
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

class Algo044(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.AddEquity('TQQQ', Resolution.Daily)
        self.tqqq_symbol = self.Symbol('TQQQ')
        
        self.AddUniverse(self.CoarseSelectionFunction)
        self.basket = {}  # symbol -> dict of indicators
        self.rebalance_day = None
        self.SetWarmUp(60)
        
        # Indicators for TQQQ
        self.tqqq_atr = self.ATR(self.tqqq_symbol, 20, MovingAverageType.Simple, Resolution.Daily)
        self.tqqq_sma200 = self.SMA(self.tqqq_symbol, 200, Resolution.Daily)
        
    def CoarseSelectionFunction(self, coarse):
        # Filter for US stocks with fundamentals
        filtered = [c for c in coarse if c.HasFundamentalData and c.Market == 'usa']
        # Sort by market cap descending, take top 10
        sorted_coarse = sorted(filtered, key=lambda c: c.MarketCap, reverse=True)
        top10 = [c.Symbol for c in sorted_coarse[:10]]
        
        # Remove symbols no longer in universe
        for symbol in list(self.basket.keys()):
            if symbol not in top10:
                self.basket.pop(symbol)
        
        # Add new symbols
        for symbol in top10:
            if symbol not in self.basket:
                # Create indicators for this symbol
                atr = self.ATR(symbol, 20, MovingAverageType.Simple, Resolution.Daily)
                corr = self.RollingCorrelation(self.tqqq_symbol, symbol, 60, Resolution.Daily)
                sma200 = self.SMA(symbol, 200, Resolution.Daily)
                self.basket[symbol] = {
                    'ATR': atr,
                    'Correlation': corr,
                    'SMA200': sma200,
                    'LastPrice': 0
                }
        
        return top10

    def OnData(self, data):
        if self.IsWarmingUp:
            return
        
        if not data.ContainsKey(self.tqqq_symbol):
            return
        
        # Rebalance only once per day
        if self.rebalance_day == self.Time.date():
            return
        self.rebalance_day = self.Time.date()
        
        # --- Regime detection (based on TQQQ vs 200 SMA) ---
        tqqq_price = data[self.tqqq_symbol].Close
        tqqq_sma200_val = self.tqqq_sma200.Current.Value if self.tqqq_sma200.IsReady else None
        regime_factor = 1.0 if (tqqq_sma200_val is not None and tqqq_price > tqqq_sma200_val) else 0.5
        
        # --- Seasonality (monthly mean return of TQQQ over last 5 years) ---
        seasonality_factor = 1.0
        tqqq_hist = self.History(self.tqqq_symbol, 252*5, Resolution.Daily)
        if not tqqq_hist.empty:
            try:
                tqqq_hist = tqqq_hist.copy()
                tqqq_hist['Month'] = tqqq_hist.index.get_level_values('time').month
                monthly_ret = tqqq_hist['close'].pct_change().groupby(tqqq_hist['Month']).mean()
                current_month = self.Time.month
                if current_month in monthly_ret.index:
                    seasonality_factor = 1 + float(monthly_ret.loc[current_month])
            except:
                pass
        
        # --- Dispersion (cross-sectional std of daily returns of basket members over last 20 days) ---
        dispersion_factor = 1.0
        basket_symbols = list(self.basket.keys())
        if len(basket_symbols) >= 2:
            all_symbols = basket_symbols + [self.tqqq_symbol]
            try:
                hist = self.History(all_symbols, 60, Resolution.Daily)
                if not hist.empty:
                    # Pivot to get time as index, symbols as columns
                    close = hist['close'].unstack(level=0)
                    returns = close.pct_change().dropna()
                    daily_dispersion = returns.std(axis=1)
                    avg_dispersion = daily_dispersion.tail(20).mean()
                    dispersion_factor = 1.0 / (1.0 + avg_dispersion)
            except:
                pass
        
        # --- Compute scores for each basket symbol ---
        scores = {}
        for symbol, info in self.basket.items():
            if not data.ContainsKey(symbol):
                continue
            price = data[symbol].Close
            info['LastPrice'] = price
            
            # Volatility signal: ATR / price as implied volatility proxy
            atr_val = info['ATR'].Current.Value if info['ATR'].IsReady else 0.0
            if price > 0 and atr_val > 0:
                iv_estimate = atr_val / price * 100
                vol_score = 1.0 / (1.0 + iv_estimate)
            else:
                vol_score = 0.5
            
            # Correlation signal: absolute correlation with TQQQ
            corr_val = info['Correlation'].Current.Value if info['Correlation'].IsReady else 0.0
            corr_weight = 1.0 - abs(corr_val)   # lower weight when strongly correlated
            
            # Combine all factors
            score = vol_score * corr_weight * dispersion_factor * seasonality_factor * regime_factor
            if score > 0:
                scores[symbol] = score
        
        # --- Compute score for TQQQ (no correlation used) ---
        tqqq_atr_val = self.tqqq_atr.Current.Value if self.tqqq_atr.IsReady else 0.0
        if tqqq_price > 0 and tqqq_atr_val > 0:
            tqqq_iv = tqqq_atr_val / tqqq_price * 100
            tqqq_vol_score = 1.0 / (1.0 + tqqq_iv)
        else:
            tqqq_vol_score = 0.5
        tqqq_score = tqqq_vol_score * regime_factor * seasonality_factor * dispersion_factor
        if tqqq_score > 0:
            scores[self.tqqq_symbol] = tqqq_score
        
        if not scores:
            return
        
        # --- Normalize scores into weights (total <= 1, no leverage) ---
        total_score = sum(scores.values())
        if total_score <= 0:
            return
        
        # Allocate 95% of capital to avoid rounding issues and keep cash buffer
        for symbol, score in scores.items():
            weight = (score / total_score) * 0.95
            weight = min(weight, 1.0)  # enforce no leverage
            self.SetHoldings(symbol, weight)
        
        # Liquidate any positions not in scores
        for holding in self.Portfolio.Values:
            if holding.Invested and holding.Symbol not in scores:
                self.Liquidate(holding.Symbol)
