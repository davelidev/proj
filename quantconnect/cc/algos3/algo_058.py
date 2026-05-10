from QuantConnect import *
from QuantConnect.Algorithm import *
from QuantConnect.Indicators import *
from QuantConnect.Data.UniverseSelection import *

class Algo058(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        # Add fixed TQQQ equity (not traded)
        self.AddEquity("TQQQ", Resolution.Daily)

        # Universe settings
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelectionFunction, self.FineSelectionFunction)

        # Basket to hold CCI indicators for each universe symbol
        self.basket = {}

        # Warm up for CCI(14)
        self.SetWarmup(14, Resolution.Daily)

    def CoarseSelectionFunction(self, coarse):
        # Select stocks with fundamental data and non-zero price
        filtered = [x for x in coarse if x.HasFundamentalData and x.Price > 0]
        # Return all symbols for fine selection
        return [x.Symbol for x in filtered]

    def FineSelectionFunction(self, fine):
        # Sort by market cap descending, take top 10
        sorted_by_mcap = sorted(fine, key=lambda x: x.MarketCap, reverse=True)
        top10 = [x.Symbol for x in sorted_by_mcap[:10]]
        return top10

    def OnSecuritiesChanged(self, changes):
        # Remove indicators for symbols that left the universe
        for removed in changes.RemovedSecurities:
            if removed.Symbol in self.basket:
                del self.basket[removed.Symbol]
                self.Liquidate(removed.Symbol)

        # Add new symbols and create CCI indicators
        for added in changes.AddedSecurities:
            symbol = added.Symbol
            if symbol not in self.basket:
                self.basket[symbol] = self.CCI(symbol, 14, Resolution.Daily)

    def OnData(self, data):
        if self.IsWarmingUp:
            return

        # Update indicators and evaluate signals
        for symbol, cci in self.basket.items():
            # Ensure we have data for this symbol
            if not data.ContainsKey(symbol):
                continue

            # Update indicator
            cci.Update(data[symbol].EndTime, data[symbol].Close)

            if not cci.IsReady:
                continue

            current_cci = cci.Current.Value

            # Entry: CCI oversold (< -100) and not currently invested
            if current_cci < -100 and not self.Portfolio[symbol].Invested:
                # Allocate 10% per position (max 10 symbols => 100%)
                self.SetHoldings(symbol, 0.10)

            # Exit: CCI overbought (> 100) and currently invested
            elif current_cci > 100 and self.Portfolio[symbol].Invested:
                self.SetHoldings(symbol, 0)
