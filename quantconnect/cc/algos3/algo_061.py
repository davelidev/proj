from AlgorithmImports import *

class Algo061(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        # Add TQQQ as required
        self.AddEquity("TQQQ", Resolution.Daily)
        
        # Universe selection for top 10 by market cap (all sectors)
        self.AddUniverse(self.CoarseSelectionFunction)
        
        # Dictionary to hold indicators for each symbol in the basket
        self.basket = {}
    
    def CoarseSelectionFunction(self, coarse):
        # Filter for fundamental data and market cap > 0
        filtered = [c for c in coarse if c.HasFundamentalData and c.MarketCap > 0]
        # Sort by market cap descending and take top 10
        sorted_by_mcap = sorted(filtered, key=lambda c: c.MarketCap, reverse=True)
        top10 = sorted_by_mcap[:10]
        return [c.Symbol for c in top10]
    
    def OnSecuritiesChanged(self, changes):
        # Add indicators for new symbols
        for added in changes.AddedSecurities:
            symbol = added.Symbol
            if symbol not in self.basket:
                max_ind = Maximum(10)
                roc_ind = RateOfChange(5)
                # Register with selector to use Close price
                self.RegisterIndicator(symbol, max_ind, Resolution.Daily, 
                                       Selector=lambda x: x.Close)
                self.RegisterIndicator(symbol, roc_ind, Resolution.Daily, 
                                       Selector=lambda x: x.Close)
                self.basket[symbol] = {'max': max_ind, 'roc': roc_ind}
                
                # Warm up indicators with historical data
                history = self.History(symbol, 10, Resolution.Daily)
                if not history.empty:
                    for index, row in history.iterrows():
                        max_ind.Update(index, row.close)
                        roc_ind.Update(index, row.close)
        
        # Remove indicators for symbols no longer in universe
        for removed in changes.RemovedSecurities:
            symbol = removed.Symbol
            if symbol in self.basket:
                del self.basket[symbol]
    
    def OnData(self, data):
        # Collect symbols meeting entry condition
        buys = []
        for symbol, inds in self.basket.items():
            if inds['max'].IsReady and inds['roc'].IsReady and symbol in data.Bars:
                close = data.Bars[symbol].Close
                if close == inds['max'].Current.Value and inds['roc'].Current.Value > 0:
                    buys.append(symbol)
        
        # Liquidate positions that no longer qualify
        for symbol, holding in self.Portfolio.items():
            if symbol not in buys and holding.Invested:
                self.SetHoldings(symbol, 0)
        
        # Enter positions for qualifying symbols with equal weight
        if buys:
            weight = 1.0 / len(buys)
            for symbol in buys:
                self.SetHoldings(symbol, weight)
