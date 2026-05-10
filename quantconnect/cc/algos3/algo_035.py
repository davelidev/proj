from AlgorithmImports import *
from System.Collections.Generic import List
from System import Action
import math

class Algo035(QCAlgorithm):
    """
    Skew-based daily trading algorithm with dynamic mega-cap basket and TQQQ.
    """
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        # Add TQQQ (fixed ticker)
        self.AddEquity('TQQQ', Resolution.Daily)

        # Universe settings: daily resolution
        self.UniverseSettings.Resolution = Resolution.Daily

        # Add universe filter for top-10 mega-cap stocks
        self.AddUniverse(self.CoarseFilter, self.FineFilter)

        # Basket tracking (key: Symbol, value: placeholder)
        self.basket = {}

        # Equity tracking for drawdown
        self.highest_equity = self.Portfolio.TotalPortfolioValue

        # Schedule daily rebalance after market open
        self.Schedule.On(
            self.DateRules.EveryDay('TQQQ'),
            self.TimeRules.AfterMarketOpen('TQQQ', 30),
            self.Rebalance
        )

        # Set brokerage model to default (no leverage)
        # No SetBrokerageModel

    def CoarseFilter(self, coarse):
        # Filter stocks with price > $5 and fundamental data, sort by dollar volume
        filtered = [x for x in coarse if x.HasFundamentalData and x.Price > 5]
        sorted_by_volume = sorted(filtered, key=lambda x: x.DollarVolume, reverse=True)[:500]
        return [x.Symbol for x in sorted_by_volume]

    def FineFilter(self, fine):
        # Filter mega-cap (market cap > $200B) and take top 10 by market cap
        mega_cap = [x for x in fine if x.MarketCap > 200e9]
        sorted_by_cap = sorted(mega_cap, key=lambda x: x.MarketCap, reverse=True)[:10]
        selected = [x.Symbol for x in sorted_by_cap]

        # Update basket dictionary
        self.basket = {sym: None for sym in selected}
        return selected

    def OnData(self, data):
        # Data-driven rebalance (daily)
        if not self.IsWarmingUp:
            self.Rebalance()

    def Rebalance(self):
        # Current portfolio value and drawdown
        equity = self.Portfolio.TotalPortfolioValue
        self.highest_equity = max(self.highest_equity, equity)
        drawdown = 0.0
        if self.highest_equity > 0:
            drawdown = (self.highest_equity - equity) / self.highest_equity
        drawdown_factor = 1.0 - drawdown  # reduce exposure during drawdown

        # Gather all symbols: TQQQ + basket
        all_symbols = ['TQQQ'] + list(self.basket.keys())

        # Compute raw weights for each symbol (unscaled)
        raw_weights = {}
        for symbol in all_symbols:
            w = self.ComputeWeight(symbol)
            if w is not None:
                raw_weights[symbol] = w

        if not raw_weights:
            self.Liquidate()
            return

        # Breadth factor: fraction of basket symbols with positive 20-day return
        positive_count = 0
        total_basket = len(self.basket)
        for sym in self.basket:
            ret = self.Compute20dReturn(sym)
            if ret is not None and ret > 0:
                positive_count += 1
        breadth = positive_count / max(total_basket, 1)  # avoid division by zero
        breadth_factor = 0.5 + 0.5 * breadth  # range [0.5, 1] – low breadth reduces exposure

        # Combine all scaling factors
        total_scale = drawdown_factor * breadth_factor

        # Normalize raw weights so they sum to total_scale
        total_raw = sum(raw_weights.values())
        if total_raw == 0:
            self.Liquidate()
            return
        scale = total_scale / total_raw

        # Apply scaling and set holdings (no leverage, weights ≤ 1)
        for sym, w in raw_weights.items():
            final_w = w * scale
            if final_w > 0:
                self.SetHoldings(sym, final_w)
            else:
                self.SetHoldings(sym, 0.0)  # or liquidate individually

    def ComputeWeight(self, symbol):
        """
        Compute a raw weight for a given symbol based on skew and volatility regime.
        """
        # Need 21 daily closes for 20 returns
        history = self.History(symbol, 21, Resolution.Daily)
        if history.empty or len(history) < 21:
            return None

        closes = list(history['close'].values)
        returns = []
        for i in range(1, len(closes)):
            if closes[i-1] != 0:
                returns.append((closes[i] - closes[i-1]) / closes[i-1])
        if len(returns) < 3:
            return None

        # Compute skew manually (no external libraries)
        n = len(returns)
        mean = sum(returns) / n
        variance = sum((r - mean) ** 2 for r in returns) / (n - 1)  # sample variance
        std = math.sqrt(variance) if variance > 0 else 0.0
        if std == 0:
            skew = 0.0
        else:
            skew = (sum((r - mean) ** 3 for r in returns) / n) / (std ** 3)

        # Skew factor: reduce weight when |skew| is high
        skew_factor = 1.0 / (1.0 + abs(skew))

        # Volatility regime: compare 20-day vol to 60-day vol
        hist60 = self.History(symbol, 60, Resolution.Daily)
        if not hist60.empty and len(hist60) >= 60:
            closes60 = list(hist60['close'].values)
            ret60 = []
            for i in range(1, len(closes60)):
                if closes60[i-1] != 0:
                    ret60.append((closes60[i] - closes60[i-1]) / closes60[i-1])
            if len(ret60) >= 20:
                # 20-day vol (last 20 returns)
                ret20 = ret60[-20:]
                mean20 = sum(ret20) / len(ret20)
                var20 = sum((r - mean20)**2 for r in ret20) / (len(ret20) - 1)
                vol20 = math.sqrt(max(var20, 0))
                # 60-day vol (all 60 returns)
                mean60 = sum(ret60) / len(ret60)
                var60 = sum((r - mean60)**2 for r in ret60) / (len(ret60) - 1)
                vol60 = math.sqrt(max(var60, 0))
                if vol60 > 0:
                    vol_ratio = vol20 / vol60
                else:
                    vol_ratio = 1.0
                # Reduce weight if volatility is rising (ratio > 1.2)
                vol_factor = 1.0 / (1.0 + 0.5 * max(0, vol_ratio - 1.2))
            else:
                vol_factor = 1.0
        else:
            vol_factor = 1.0

        # Combine factors (multiplicative)
        raw_weight = skew_factor * vol_factor
        return raw_weight

    def Compute20dReturn(self, symbol):
        """
        Compute the 20-day simple return for a symbol.
        """
        history = self.History(symbol, 21, Resolution.Daily)
        if history.empty or len(history) < 21:
            return None
        closes = list(history['close'].values)
        if closes[0] == 0:
            return None
        return (closes[-1] - closes[0]) / closes[0]
