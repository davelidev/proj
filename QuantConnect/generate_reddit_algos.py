import os

TEMPLATE_SMA = """
from AlgorithmImports import *

class RedditSMAStrategy(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.asset = self.AddEquity("{asset}", Resolution.Daily).Symbol
        self.signal = self.AddEquity("{signal_asset}", Resolution.Daily).Symbol
        self.sma = self.SMA(self.signal, {sma_period}, Resolution.Daily)
        self.SetWarmUp({sma_period}, Resolution.Daily)

    def OnData(self, data):
        if self.IsWarmingUp or not self.sma.IsReady:
            return
        
        price = self.Securities[self.signal].Price
        if price > self.sma.Current.Value:
            if not self.Portfolio.Invested:
                self.SetHoldings(self.asset, 1.0)
        else:
            if self.Portfolio.Invested:
                self.Liquidate()
"""

TEMPLATE_RSI = """
from AlgorithmImports import *

class RedditRSIStrategy(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.asset = self.AddEquity("{asset}", Resolution.Daily).Symbol
        self.rsi = self.RSI(self.asset, {rsi_period}, Resolution.Daily)
        self.SetWarmUp({rsi_period}, Resolution.Daily)

    def OnData(self, data):
        if self.IsWarmingUp or not self.rsi.IsReady:
            return
        
        rsi_val = self.rsi.Current.Value
        if rsi_val < {rsi_lower}:
            if not self.Portfolio.Invested:
                self.SetHoldings(self.asset, 1.0)
        elif rsi_val > {rsi_upper}:
            if self.Portfolio.Invested:
                self.Liquidate()
"""

TEMPLATE_ROTATION = """
from AlgorithmImports import *

class RedditRotationStrategy(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.assets = [self.AddEquity(ticker, Resolution.Daily).Symbol for ticker in {assets}]
        self.lookback = {lookback}
        self.last_rebalance = -1

    def OnData(self, data):
        if self.Time.month == self.last_rebalance:
            return
        self.last_rebalance = self.Time.month

        # Calculate momentum
        scores = {{}}
        for asset in self.assets:
            hist = self.History(asset, self.lookback, Resolution.Daily)
            if not hist.empty:
                start_price = hist.iloc[0].close
                current_price = self.Securities[asset].Price
                scores[asset] = (current_price - start_price) / start_price
        
        if not scores: return
        
        best_asset = max(scores, key=scores.get)
        if scores[best_asset] > 0:
            if not self.Portfolio[best_asset].Invested:
                self.Liquidate()
                self.SetHoldings(best_asset, 1.0)
        else:
            self.Liquidate()
"""

TEMPLATE_TOP_CAP = """
from AlgorithmImports import *

class RedditTopCapStrategy(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelectionFunction)
        self.sma_period = {sma_period}
        self.top_n = {top_n}
        self.symbols = []
        self.smas = {{}}

    def CoarseSelectionFunction(self, coarse):
        # Sort by dollar volume as a proxy for market cap if fundamental data is limited, 
        # or use actual market cap if using Fundamental selection.
        # Here we use DollarVolume for coarse.
        sorted_by_volume = sorted(coarse, key=lambda x: x.DollarVolume, reverse=True)
        self.symbols = [x.Symbol for x in sorted_by_volume[:self.top_n]]
        return self.symbols

    def OnData(self, data):
        for symbol in self.symbols:
            if symbol not in self.smas:
                self.smas[symbol] = self.SMA(symbol, self.sma_period, Resolution.Daily)
            
            if not self.smas[symbol].IsReady: continue
            
            price = self.Securities[symbol].Price
            sma = self.smas[symbol].Current.Value
            
            if price > sma:
                if not self.Portfolio[symbol].Invested:
                    self.SetHoldings(symbol, 1.0 / self.top_n)
            else:
                if self.Portfolio[symbol].Invested:
                    self.Liquidate(symbol)
"""

def generate():
    os.makedirs("gemini/algos", exist_ok=True)
    idx = 111
    
    # SMA Batch (111-120)
    for sma in [50, 100, 150, 200, 250]:
        for asset in ["TQQQ", "SOXL"]:
            with open(f"gemini/algos/it_{idx}.py", "w") as f:
                f.write(TEMPLATE_SMA.format(asset=asset, signal_asset="QQQ", sma_period=sma))
            idx += 1

    # RSI Batch (121-135)
    for period in [2, 14]:
        for lower in [10, 20, 30]:
            for asset in ["TQQQ", "SOXL", "UPRO"]:
                with open(f"gemini/algos/it_{idx}.py", "w") as f:
                    f.write(TEMPLATE_RSI.format(asset=asset, rsi_period=period, rsi_lower=lower, rsi_upper=70))
                idx += 1

    # Rotation Batch (136-145)
    for lookback in [21, 63, 126]:
        for assets in [['TQQQ', 'TLT'], ['TQQQ', 'BIL'], ['SOXL', 'TQQQ', 'TLT']]:
            with open(f"gemini/algos/it_{idx}.py", "w") as f:
                f.write(TEMPLATE_ROTATION.format(assets=assets, lookback=lookback))
            idx += 1
            
    # Top Cap Batch (146-160)
    for n in [5, 10]:
        for sma in [100, 200]:
            with open(f"gemini/algos/it_{idx}.py", "w") as f:
                f.write(TEMPLATE_TOP_CAP.format(top_n=n, sma_period=sma))
            idx += 1

if __name__ == "__main__":
    generate()
