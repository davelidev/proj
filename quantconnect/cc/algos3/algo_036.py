from AlgorithmImports import *
from datetime import timedelta

class Algo036(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        # Add TQQQ (hardcoded allowed)
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        
        # Universe settings
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelectionFunction)
        
        # Basket tracking
        self.basket = {}  # symbol -> dict of computed values (cached)
        self.current_basket_symbols = set()
        
        # Equity tracking for drawdown
        self.portfolio_peak = 100000
        self.last_rebalance = datetime.min
        
    def CoarseSelectionFunction(self, coarse):
        # Filter for US equities with fundamental data and market cap
        eligible = [x for x in coarse if x.HasFundamentalData and x.Market == "usa" and x.AdjustedPrice > 5]
        
        # Sort by market cap descending, take top 10, exclude TQQQ
        sorted_by_cap = sorted(eligible, key=lambda x: x.MarketCap, reverse=True)
        top10 = [x.Symbol for x in sorted_by_cap[:10] if x.Symbol != self.tqqq]
        
        return top10
    
    def OnSecuritiesChanged(self, changes):
        # Update basket tracking
        for added in changes.AddedSecurities:
            sym = added.Symbol
            if sym not in self.basket:
                self.basket[sym] = {}  # will hold indicators or cached data
            self.current_basket_symbols.add(sym)
        
        for removed in changes.RemovedSecurities:
            sym = removed.Symbol
            if sym in self.current_basket_symbols:
                self.current_basket_symbols.discard(sym)
            if sym in self.basket:
                del self.basket[sym]
    
    def OnData(self, data):
        # Only rebalance once per day
        if self.Time.date() == self.last_rebalance.date():
            return
        self.last_rebalance = self.Time
        
        self.Rebalance()
    
    def Rebalance(self):
        # ------------------- Vol Regime Detection -------------------
        tqqq_vol_current, tqqq_vol_median = self.ComputeVolRegime()
        low_vol_regime = tqqq_vol_current < 1.2 * tqqq_vol_median
        
        # ------------------- Target Weights -------------------
        target_weights = {}
        
        if low_vol_regime:
            # Compute signals for each basket symbol
            scores = {}
            for sym in self.current_basket_symbols:
                if sym not in self.basket:
                    continue
                # Fetch historical data for momentum, vol, correlation
                momentum = self.ComputeMomentum(sym, 252)
                vol = self.ComputeVolatility(sym, 20)
                corr = self.ComputeCorrelationWithTQQQ(sym, 63)
                
                if momentum is None or vol is None or corr is None:
                    continue
                
                # Simple factor score: positive momentum * low vol
                # Use inverse vol and scale momentum (0/1)
                score = (1.0 / vol) * (1.0 if momentum > 0 else 0.0)
                scores[sym] = score
            
            if scores:
                total_score = sum(scores.values())
                if total_score > 0:
                    for sym, score in scores.items():
                        target_weights[sym] = score / total_score
                else:
                    # Equal weight fallback
                    n = len(scores)
                    for sym in scores:
                        target_weights[sym] = 1.0 / n
        else:
            # High vol regime: only TQQQ
            target_weights[self.tqqq] = 1.0
        
        # ------------------- Drawdown Gate -------------------
        # Track equity peak
        current_equity = self.Portfolio.TotalPortfolioValue
        if current_equity > self.portfolio_peak:
            self.portfolio_peak = current_equity
        drawdown = (self.portfolio_peak - current_equity) / self.portfolio_peak
        
        # If drawdown > 20%, scale all target weights by 0.5
        scale_factor = 1.0
        if drawdown > 0.2:
            scale_factor = 0.5
        
        for sym in target_weights:
            target_weights[sym] *= scale_factor
        
        # ------------------- Set Holdings -------------------
        # Collect all symbols currently in portfolio and targets
        all_syms = set(self.Portfolio.Keys) | set(target_weights.keys())
        
        for sym in all_syms:
            weight = target_weights.get(sym, 0.0)
            if weight > 0:
                self.SetHoldings(sym, weight)
            else:
                self.SetHoldings(sym, 0)
    
    def ComputeVolRegime(self):
        # Get TQQQ daily close prices for last 252+20 days
        history = self.History([self.tqqq], 252 + 20, Resolution.Daily)
        if history.empty or len(history) < 252:
            return 0, 1  # fallback: current vol < median => low vol
        
        closes = history.loc[self.tqqq]['close'].values
        returns = (closes[1:] / closes[:-1]) - 1
        if len(returns) < 20:
            return 0, 1
        
        # Compute rolling 20-day vol (annualized, using 252 trading days)
        rolling_vol = []
        for i in range(20, len(returns)+1):
            vol_20 = np.std(returns[i-20:i]) * np.sqrt(252)
            rolling_vol.append(vol_20)
        
        # Current vol is the most recent
        current_vol = rolling_vol[-1]
        # Median of the last 252 days (if available)
        if len(rolling_vol) >= 252:
            median_vol = np.median(rolling_vol[-252:])
        else:
            median_vol = np.median(rolling_vol)
        
        return current_vol, median_vol
    
    def ComputeMomentum(self, symbol, period):
        # 12-month momentum (simple return over last 252 trading days)
        history = self.History([symbol], period, Resolution.Daily)
        if history.empty or len(history) < period:
            return None
        closes = history.loc[symbol]['close'].values
        if len(closes) < 2:
            return None
        return (closes[-1] / closes[0]) - 1
    
    def ComputeVolatility(self, symbol, period):
        # Daily return volatility over period (annualized)
        history = self.History([symbol], period + 1, Resolution.Daily)
        if history.empty or len(history) < period + 1:
            return None
        closes = history.loc[symbol]['close'].values
        returns = (closes[1:] / closes[:-1]) - 1
        if len(returns) < period:
            return None
        return np.std(returns) * np.sqrt(252)
    
    def ComputeCorrelationWithTQQQ(self, symbol, period):
        # Pearson correlation of daily returns with TQQQ over period
        # Need both series
        tqqq_history = self.History([self.tqqq], period + 1, Resolution.Daily)
        sym_history = self.History([symbol], period + 1, Resolution.Daily)
        if tqqq_history.empty or sym_history.empty:
            return None
        tqqq_closes = tqqq_history.loc[self.tqqq]['close'].values
        sym_closes = sym_history.loc[symbol]['close'].values
        if len(tqqq_closes) < period + 1 or len(sym_closes) < period + 1:
            return None
        # Align lengths (should be same)
        min_len = min(len(tqqq_closes), len(sym_closes))
        tqqq_ret = (tqqq_closes[1:min_len] / tqqq_closes[:min_len-1]) - 1
        sym_ret = (sym_closes[1:min_len] / sym_closes[:min_len-1]) - 1
        if len(tqqq_ret) < 2:
            return None
        corr = np.corrcoef(tqqq_ret, sym_ret)[0, 1]
        return corr
