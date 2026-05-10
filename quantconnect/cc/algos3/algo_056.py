from AlgorithmImports import *

class Algo056(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelectionFunction)

        # Hardcoded TQQQ
        self.AddEquity("TQQQ", Resolution.Daily)

        # Basket to hold symbol data
        self.basket = {}
        # Initialize TQQQ in basket
        self.basket["TQQQ"] = {
            "bb": BollingerBands(20, 2),
            "consolidated": False,
            "entry_price": 0
        }

        # Benchmark
        self.SetBenchmark("SPY")

    def CoarseSelectionFunction(self, coarse):
        # Filter for stocks with fundamental data, non-failed, etc.
        sorted_by_market_cap = sorted(
            [x for x in coarse if x.HasFundamentalData and x.MarketCap > 0],
            key=lambda x: x.MarketCap,
            reverse=True
        )
        # Take top 10
        top10 = [x.Symbol for x in sorted_by_market_cap[:10]]

        # Ensure TQQQ is always included (if it's not already in top10)
        if "TQQQ" not in [str(s) for s in top10]:
            top10.append(self.Symbol("TQQQ"))

        # Return the universe symbols
        return top10

    def OnSecuritiesChanged(self, changes):
        for added in changes.AddedSecurities:
            symbol = added.Symbol
            if symbol not in self.basket:
                self.basket[symbol] = {
                    "bb": BollingerBands(20, 2),
                    "consolidated": False,
                    "entry_price": 0
                }

        for removed in changes.RemovedSecurities:
            symbol = removed.Symbol
            if symbol in self.basket and symbol != "TQQQ":
                self.Liquidate(symbol)
                del self.basket[symbol]

    def OnData(self, data):
        # First, update all indicators and check signals
        for symbol, info in self.basket.items():
            if symbol in data and data[symbol] is not None:
                bar = data[symbol]
                info["bb"].Update(bar.EndTime, bar.Close)

        # Evaluate entries and exits
        for symbol, info in self.basket.items():
            if symbol not in data or data[symbol] is None:
                continue

            bb = info["bb"]
            if not bb.IsReady:
                continue

            close = data[symbol].Close
            upper = bb.UpperBand.Current.Value
            middle = bb.MiddleBand.Current.Value
            lower = bb.LowerBand.Current.Value

            # Range contraction: bandwidth is low relative to average
            bandwidth = (upper - lower) / middle if middle != 0 else 0
            avg_bandwidth = bb.StandardDeviation.Current.Value * 2 / middle if middle != 0 else 0  # rough proxy
            # Condition: bandwidth < 20% of average bandwidth (or some threshold)
            # Use a 0.5 threshold for simplicity
            is_contracted = bandwidth < 0.5 * (bb.StandardDeviation.Current.Value * 2 / middle) if middle != 0 else False

            # Breakout: close above upper band
            breakout = close > upper

            # Entry logic
            if not self.Portfolio[symbol].Invested:
                if is_contracted and breakout and not info["consolidated"]:
                    info["consolidated"] = True  # mark that we saw contraction
                if info["consolidated"] and breakout:
                    # Enter with equal weight (assuming up to 10 positions)
                    weight = 1.0 / max(len(self.basket), 1)
                    self.SetHoldings(symbol, weight)
                    info["entry_price"] = close
                    info["consolidated"] = False  # reset
            else:
                # Exit: close below lower band or trailing stop (5%)
                if close < lower or close < info["entry_price"] * 0.95:
                    self.SetHoldings(symbol, 0)
                    info["consolidated"] = False

