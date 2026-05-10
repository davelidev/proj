from AlgorithmImports import *

class Algo073(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.normal_tickers = ["SPY"]                     # Normal mode
        self.defensive_tickers = ["XLU", "XLP"]          # Defensive mode (utilities & staples)

        # Add equity symbols with daily resolution
        for symbol in self.normal_tickers + self.defensive_tickers:
            self.AddEquity(symbol, Resolution.Daily)

        # Add VIX index data (daily)
        self.AddData(VIXIndex, "VIX", Resolution.Daily)

        # State variables
        self._current_mode = "normal"                     # Default
        self._last_vix = None

        # Schedule rebalance at market close (daily)
        self.Schedule.On(self.DateRules.EveryDay("SPY"), self.TimeRules.BeforeMarketClose("SPY", 1),
                         self.Rebalance)

    def Rebalance(self):
        """Main rebalancing logic executed daily before market close."""
        # Check if we have a valid VIX reading
        if self._last_vix is None:
            # No VIX data yet – stay in normal mode
            target_mode = "normal"
        else:
            target_mode = "defensive" if self._last_vix > 25 else "normal"

        # Determine target portfolio (weights sum to 1.0, no leverage)
        if target_mode == "defensive":
            # Hold equal weight in XLU and XLP
            target_holdings = {
                "XLU": 0.5,
                "XLP": 0.5
            }
        else:
            target_holdings = {
                "SPY": 1.0
            }

        # Rebalance only if mode changed or first run
        if target_mode != self._current_mode:
            self.Debug(f"Mode switch: {self._current_mode} -> {target_mode} (VIX = {self._last_vix})")
            self._current_mode = target_mode

        # Execute trades to achieve target weights
        self.SetHoldingsWithBasket(target_holdings)

    def OnData(self, data):
        """Capture VIX index value on each daily data event."""
        vix_symbol = "VIX"
        if data.ContainsKey(vix_symbol) and data[vix_symbol] is not None:
            self._last_vix = data[vix_symbol].Close

    def SetHoldingsWithBasket(self, target_holdings):
        """
        Adjust portfolio to match target weight dictionary.
        Each ticker must be between 0 and 1, sum = 1.
        """
        # Sell all current positions not in target_holdings
        for symbol in self.Portfolio.Keys:
            ticker = symbol.Value
            if ticker not in target_holdings:
                self.SetHoldings(symbol, 0)

        # Set target weights for each desired holding
        total_weight = sum(target_holdings.values())
        if abs(total_weight - 1.0) > 0.0001:
            self.Error(f"Target weights must sum to 1.0, got {total_weight}")
            return

        for ticker, weight in target_holdings.items():
            if weight < 0 or weight > 1:
                self.Error(f"Weight for {ticker} out of range: {weight}")
                continue
            symbol = Symbol(ticker)
            self.SetHoldings(symbol, weight)


# Index data type for VIX (custom implementation for QuantConnect)
class VIXIndex(PythonData):
    def GetSource(self, config, date, isLive):
        # VIX index data is available via QuantConnect's data provider
        return SubscriptionDataSource(f"{config.Symbol.Value}.csv",
                                      SubscriptionTransportMedium.RemoteFile,
                                      FileFormat.Csv)

    def Reader(self, config, line, date, isLive):
        # Simple CSV parser for VIX daily data (OHLCV)
        index = VIXIndex()
        try:
            data = line.split(',')
            if len(data) != 6:
                return None
            index.Time = datetime.strptime(data[0], "%Y-%m-%d")
            index.Open = float(data[1])
            index.High = float(data[2])
            index.Low = float(data[3])
            index.Close = float(data[4])
            index.Value = index.Close
            return index
        except:
            return None