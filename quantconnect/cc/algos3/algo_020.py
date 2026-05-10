from AlgorithmImports import *

class Algo020(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        # Add TQQQ as a fixed holding
        self.AddEquity("TQQQ", Resolution.Daily)
        self.basket = {self.Symbol("TQQQ"): {}}

        # Universe selection for top-10 by market cap
        self.AddUniverse(self.CoarseSelectionFunction)

    def CoarseSelectionFunction(self, coarse):
        # Filter and sort by market cap, take top 10
        filtered = [c for c in coarse if c.HasFundamentalData and c.MarketCap > 0]
        sorted_by_mcap = sorted(filtered, key=lambda c: c.MarketCap, reverse=True)
        top10 = sorted_by_mcap[:10]

        # Build new basket: always include TQQQ
        new_basket = {self.Symbol("TQQQ"): self.basket.get(self.Symbol("TQQQ"), {})}
        for c in top10:
            sym = c.Symbol
            new_basket[sym] = self.basket.get(sym, {})

        self.basket = new_basket

        # Return ticker strings for the universe to subscribe
        return [str(c.Symbol) for c in top10]

    def OnData(self, data):
        # Create and warm up indicators for any new symbols
        for symbol in list(self.basket.keys()):
            if symbol not in self.Securities:
                continue
            ind_dict = self.basket[symbol]
            if "medianVol" not in ind_dict:
                vol_median = Median(20, Resolution.Daily)
                self.RegisterIndicator(symbol, vol_median, Resolution.Daily, Field.Volume)
                # Warm up with history
                history = self.History[TradeBar](symbol, 20, Resolution.Daily)
                for bar in history:
                    vol_median.Update(bar)
                ind_dict["medianVol"] = vol_median
            if "roc5" not in ind_dict:
                roc = RateOfChange(5, Resolution.Daily)
                self.RegisterIndicator(symbol, roc, Resolution.Daily)
                history = self.History[TradeBar](symbol, 5, Resolution.Daily)
                for bar in history:
                    roc.Update(bar)
                ind_dict["roc5"] = roc

        # Compute signals
        long_symbols = []
        for symbol, ind_dict in self.basket.items():
            if symbol not in data or not data.ContainsKey(symbol):
                continue
            bar = data[symbol]
            vol_med = ind_dict.get("medianVol")
            roc = ind_dict.get("roc5")
            if vol_med is None or roc is None:
                continue
            if not vol_med.IsReady or not roc.IsReady:
                continue
            # Check volume > 1.2 * 20-day median AND 5-day return > 0
            if bar.Volume > 1.2 * vol_med.Current.Value and roc.Current.Value > 0:
                long_symbols.append(symbol)

        # Build target weights for all currently held symbols and basket symbols
        target_weights = {}
        # Zero out anything not in basket (positions from previous day)
        for sym in self.Securities.Keys:
            if sym not in self.basket:
                target_weights[sym] = 0.0
        # Assign equal weight to long signals, zero to others in basket
        weight = 1.0 / len(long_symbols) if long_symbols else 0.0
        for sym in self.basket:
            target_weights[sym] = weight if sym in long_symbols else 0.0

        # Execute rebalance
        for sym, w in target_weights.items():
            self.SetHoldings(sym, w)
