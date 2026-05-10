from System import *
from QuantConnect import *
from QuantConnect.Algorithm import *
from QuantConnect.Data import *
from QuantConnect.Indicators import *
from QuantConnect.Securities import *

class Algo071(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        # Define the set of sector ETFs (9 SPDR sector funds)
        self.sectorTickers = ["XLY", "XLP", "XLE", "XLF", "XLV", "XLI", "XLB", "XLK", "XLU"]
        self.symbols = []
        self.momentum = {}
        
        for ticker in self.sectorTickers:
            symbol = self.AddEquity(ticker, Resolution.Daily).Symbol
            self.symbols.append(symbol)
            # 63-day rate of change (momentum)
            self.momentum[symbol] = self.ROC(symbol, 63, Resolution.Daily)
        
        # Warm up the algorithm with 63 trading days to initialise indicators
        self.SetWarmUp(63)

    def OnData(self, data):
        # Skip trading during warmup period
        if self.IsWarmingUp:
            return
        
        # Gather current momentum values for all symbols that have data
        momentumValues = {}
        for symbol in self.symbols:
            if data.Bars.ContainsKey(symbol) and self.momentum[symbol].IsReady:
                momentumValues[symbol] = self.momentum[symbol].Current.Value
        
        # Need at least 3 symbols with valid momentum
        if len(momentumValues) < 3:
            return
        
        # Rank symbols by momentum descending, take top 3
        ranked = sorted(momentumValues.keys(), key=lambda s: momentumValues[s], reverse=True)
        top3 = ranked[:3]
        
        # Equal weight for each selected sector
        weight = 1.0 / 3.0
        
        # Liquidate all positions that are not in the top 3
        for symbol in self.symbols:
            if symbol not in top3:
                self.Liquidate(symbol)
        
        # Set holdings for the top 3 sectors simultaneously
        self.SetHoldings(top3[0], weight, top3[1], weight, top3[2], weight)
