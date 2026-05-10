from clr import AddReference
AddReference("QuantConnect.Algorithm")
AddReference("QuantConnect.Indicators")

from QuantConnect import *
from QuantConnect.Algorithm import *
from QuantConnect.Indicators import *
from QuantConnect.Data.Fundamental import Fundamental

class Algo028(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        # Core equity – always present
        self.AddEquity("TQQQ", Resolution.Daily)

        # Dynamic universe of top-10 mega‑cap stocks
        self.AddUniverse(self.FundamentalFilter)

        # Holdings tracking (NOT self.universe)
        self.basket = {}          # symbol -> remaining hold days (2 -> 1 -> 0 -> exit)
        self._maxIndicators = {}  # symbol -> Maximum(10) indicator
        self._prevMax = {}        # symbol -> previous value of the maximum indicator
        self._targetWeight = -0.1 # fixed short weight per trade

        self.SetWarmUp(10, Resolution.Daily)

        # Indicator for TQQQ
        tqqq = self.Symbol("TQQQ")
        self._maxIndicators[tqqq] = self.MAX(tqqq, 10, Resolution.Daily, Field.High)


    def FundamentalFilter(self, fundamentals: List[Fundamental]) -> List[Symbol]:
        """Select the top 10 stocks by market capitalisation."""
        filtered = [f for f in fundamentals if f.HasFundamentalData and f.MarketCap > 0]
        sortedFunds = sorted(filtered, key=lambda f: f.MarketCap, reverse=True)
        top10 = sortedFunds[:10]
        chosen = [f.Symbol for f in top10]

        # Add new symbols and their indicators
        for symbol in chosen:
            if symbol not in self._maxIndicators:
                self._symbols.add(symbol)
                self.AddEquity(symbol, Resolution.Daily)
                self._maxIndicators[symbol] = self.MAX(symbol, 10, Resolution.Daily, Field.High)

        # Remove symbols that fell out of the top 10
        toRemove = [s for s in self._symbols if s not in chosen]
        for symbol in toRemove:
            self._symbols.remove(symbol)
            self.RemoveSecurity(symbol)
            # Clean up all related dictionaries
            if symbol in self._maxIndicators:
                del self._maxIndicators[symbol]
            if symbol in self._prevMax:
                del self._prevMax[symbol]
            if symbol in self.basket:
                del self.basket[symbol]

        return chosen


    def OnData(self, data: Slice) -> None:
        if self.IsWarmingUp:
            return

        targetWeights = {}

        # Process universe symbols (dynamic top-10)
        for symbol in list(self._symbols):
            if not data.ContainsKey(symbol) or data[symbol] is None:
                continue
            bar = data[symbol]
            if bar is None:
                continue
            high = bar.High

            if symbol not in self._maxIndicators:
                continue
            maxInd = self._maxIndicators[symbol]
            if not maxInd.IsReady:
                continue

            currentMax = maxInd.Current.Value
            prevMax = self._prevMax.get(symbol, None)

            # New 10‑day high occurs when today's high > yesterday's 10‑day maximum
            newHigh = (prevMax is not None and high > prevMax)

            # Update stored previous maximum
            self._prevMax[symbol] = currentMax

            # Position management
            if symbol in self.basket:
                # Already short – decrement remaining days
                self.basket[symbol] -= 1
                if self.basket[symbol] <= 0:
                    targetWeights[symbol] = 0
                    del self.basket[symbol]
                else:
                    targetWeights[symbol] = self._targetWeight
            elif newHigh:
                # Enter a new short position
                self.basket[symbol] = 2
                targetWeights[symbol] = self._targetWeight

        # Process TQQQ separately (always in the algorithm)
        tqqq = self.Symbol("TQQQ")
        if data.ContainsKey(tqqq) and data[tqqq] is not None:
            bar = data[tqqq]
            high = bar.High
            if tqqq in self._maxIndicators:
                maxInd = self._maxIndicators[tqqq]
                if maxInd.IsReady:
                    currentMax = maxInd.Current.Value
                    prevMax = self._prevMax.get(tqqq, None)

                    newHigh = (prevMax is not None and high > prevMax)
                    self._prevMax[tqqq] = currentMax

                    if tqqq in self.basket:
                        self.basket[tqqq] -= 1
                        if self.basket[tqqq] <= 0:
                            targetWeights[tqqq] = 0
                            del self.basket[tqqq]
                        else:
                            targetWeights[tqqq] = self._targetWeight
                    elif newHigh:
                        self.basket[tqqq] = 2
                        targetWeights[tqqq] = self._targetWeight

        # Enforce no leverage: sum of absolute weights <= 1
        totalAbs = sum(abs(w) for w in targetWeights.values())
        if totalAbs > 1.0:
            scale = 1.0 / totalAbs
            for k in targetWeights:
                targetWeights[k] *= scale

        # Rebalance portfolio once per day
        self.SetHoldings(targetWeights)