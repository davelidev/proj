from AlgorithmImports import *

class Algo070(QCAlgorithm):
    '''
    Volume-weighted momentum strategy on dynamic top-10 universe by market cap (all sectors).
    Uses the same entry pattern as Batch 2 (Algos 011-020) but applied to broader universe.
    '''

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        # Hardcoded TQQQ
        self.AddEquity("TQQQ", Resolution.Daily)

        # Universe: top 10 by market cap (all sectors)
        self.AddUniverse(self.CoarseSelectionFunction)

        self.basket = {}  # symbol -> tuple (roc_indicator, volume_sma_indicator)

        # Monthly rebalance on first trading day
        self.Schedule.On(self.DateRules.MonthStart("TQQQ"),
                         self.TimeRules.AfterMarketOpen("TQQQ", 0),
                         self.Rebalance)

        self.rebalance_day = True  # force first rebalance

    def CoarseSelectionFunction(self, coarse):
        # Filter stocks with price and volume data
        filtered = [x for x in coarse if x.HasFundamentalData and x.Price > 0 and x.Volume > 0]
        # Sort by market cap descending and take top 10
        sorted_by_cap = sorted(filtered, key=lambda x: x.MarketCap, reverse=True)
        top10 = [x.Symbol for x in sorted_by_cap[:10]]
        return top10

    def OnSecuritiesChanged(self, changes):
        # Add indicators for new symbols, remove for old
        for added in changes.AddedSecurities:
            symbol = added.Symbol
            if symbol not in self.basket:
                # 12-month momentum (252 trading days)
                roc = self.ROC(symbol, 252, Resolution.Daily)
                # 21-day average volume
                vol_sma = self.SMA(symbol, 21, Resolution.Daily, Field.Volume)
                self.basket[symbol] = (roc, vol_sma)

        for removed in changes.RemovedSecurities:
            symbol = removed.Symbol
            if symbol in self.basket:
                del self.basket[symbol]

    def OnData(self, data):
        # Indicators are automatically updated by QC; no manual update needed
        pass

    def Rebalance(self):
        if len(self.basket) == 0:
            return

        # Compute volume-weighted momentum score for each symbol
        scores = {}
        for symbol, (roc, vol_sma) in self.basket.items():
            if roc.IsReady and vol_sma.IsReady:
                momentum = roc.Current.Value
                avg_volume = vol_sma.Current.Value
                score = momentum * avg_volume
                scores[symbol] = score

        if len(scores) == 0:
            return

        # Select top 5 symbols by score (or all if less than 5)
        sorted_symbols = sorted(scores.keys(), key=lambda s: scores[s], reverse=True)
        select_count = min(5, len(sorted_symbols))
        selected = sorted_symbols[:select_count]

        # Equal weight among selected (no leverage)
        weight = 1.0 / select_count
        for symbol in self.basket:
            if symbol in selected:
                self.SetHoldings(symbol, weight)
            else:
                self.SetHoldings(symbol, 0)  # liquidate

