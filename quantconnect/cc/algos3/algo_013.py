from AlgorithmImports import *

class Algo013(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        
        self.tqqq = self.AddEquity('TQQQ', Resolution.Daily).Symbol
        self.macd = self.MACD(self.tqqq, 12, 26, 9, MovingAverageType.Exponential, Resolution.Daily)
        
        self.AddUniverse(self.CoarseSelectionFunction)
        self.basket = {}
        self._previous_diff = None
        self._signal = 0  # 0: cash, 1: long basket
        
    def CoarseSelectionFunction(self, coarse):
        sorted_by_market_cap = sorted(
            [c for c in coarse if c.HasFundamentalData and c.MarketCap > 0],
            key=lambda c: c.MarketCap,
            reverse=True
        )
        top10 = [c.Symbol for c in sorted_by_market_cap[:10]]
        
        self.basket.clear()
        for symbol in top10:
            self.basket[symbol] = 0  # weight placeholder
        
        return top10
    
    def OnData(self, data):
        if not self.macd.IsReady:
            return
        
        # Compute MACD cross signal
        current_diff = self.macd.Current.Value - self.macd.Signal.Current.Value
        if self._previous_diff is not None:
            if current_diff > 0 and self._previous_diff <= 0:
                self._signal = 1  # go long
            elif current_diff < 0 and self._previous_diff >= 0:
                self._signal = 0  # go to cash
        self._previous_diff = current_diff
        
        # Liquidate symbols not in current basket and not TQQQ
        for symbol in list(self.Portfolio.Keys):
            if symbol not in self.basket and symbol != self.tqqq:
                self.Liquidate(symbol)
        
        # Set holdings for basket symbols based on signal
        if len(self.basket) > 0:
            target_weight = 1.0 / len(self.basket) if self._signal == 1 else 0
            for symbol in self.basket:
                self.SetHoldings(symbol, target_weight)
