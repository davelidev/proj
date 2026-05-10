from AlgorithmImports import *

class Algo018(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        
        # Hardcoded TQQQ
        self.AddEquity("TQQQ", Resolution.Daily)
        tqqq_symbol = self.Symbol("TQQQ")
        self.basket = {
            tqqq_symbol: {
                'adx': self.ADX(tqqq_symbol, 14, Resolution.Daily),
                'max': self.MAX(tqqq_symbol, 21, Resolution.Daily)
            }
        }
        
        # Dynamic universe – top 10 by market cap
        self.AddUniverse(self.CoarseSelectionFunction)
        self.UniverseSettings.Resolution = Resolution.Daily
    
    def CoarseSelectionFunction(self, coarse):
        sorted_coarse = sorted(
            [c for c in coarse if c.HasFundamentalData and c.MarketCap != 0],
            key=lambda c: c.MarketCap,
            reverse=True
        )
        return [c.Symbol for c in sorted_coarse[:10]]
    
    def OnSecuritiesChanged(self, changes):
        # Add indicators for new universe symbols
        for added in changes.AddedSecurities:
            symbol = added.Symbol
            if symbol not in self.basket:
                self.basket[symbol] = {
                    'adx': self.ADX(symbol, 14, Resolution.Daily),
                    'max': self.MAX(symbol, 21, Resolution.Daily)
                }
        # Remove indicators and liquidate positions for removed symbols
        for removed in changes.RemovedSecurities:
            symbol = removed.Symbol
            if symbol in self.basket:
                self.SetHoldings(symbol, 0)  # liquidate
                del self.basket[symbol]
    
    def OnData(self, data):
        # Update indicators and find qualifying symbols
        qualifying = []
        for symbol, ind in self.basket.items():
            adx = ind['adx']
            max_21 = ind['max']
            if not (adx.IsReady and max_21.IsReady):
                continue
            if not data.ContainsKey(symbol):
                continue
            current_price = data[symbol].Close
            if current_price > max_21.Current.Value and adx.Current.Value > 30:
                qualifying.append(symbol)
        
        # Rebalance – equal weight among qualifiers, liquidate others
        if len(qualifying) > 0:
            weight = 1.0 / len(qualifying)
            for symbol in self.basket:
                if symbol in qualifying:
                    self.SetHoldings(symbol, weight)
                else:
                    self.SetHoldings(symbol, 0)
        else:
            # No signals – go to cash
            for symbol in self.basket:
                self.SetHoldings(symbol, 0)
