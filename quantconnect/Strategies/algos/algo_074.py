class Algo074(BaseSubAlgo):
    """
    Daily sector rotation between tech (XLK) and healthcare (XLV) based on 12-month relative strength.
    """

    def initialize(self):
        """Initialize algorithm: set dates, cash, add symbols, and schedule daily updates."""

        # Add sector ETFs
        self.symbol_xlk = self.AddEquity("XLK", Resolution.Daily).Symbol
        self.symbol_xlv = self.AddEquity("XLV", Resolution.Daily).Symbol

        # Schedule the update_targets method to run once per day after market open

    def update_targets(self):
        """
        Compare 12-month returns of XLK and XLV.
        Set self.targets to allocate 100% to the outperforming sector.
        """
        lookback = 252  # ~12 months of trading days

        # Request historical close prices for both symbols
        hist = self.History([self.symbol_xlk, self.symbol_xlv], lookback, Resolution.Daily)
        if hist.empty:
            return

        # Get the closing price data for each symbol
        try:
            closes = hist['close'].unstack(level=0)
        except Exception:
            # If data format is unexpected, skip this update
            return

        # Ensure we have at least lookback+1 rows (current + lookback days ago)
        if closes.shape[0] < lookback + 1:
            return

        latest_close = closes.iloc[-1]
        past_close = closes.iloc[-lookback - 1]

        # Compute 12-month returns
        return_xlk = (latest_close[self.symbol_xlk] - past_close[self.symbol_xlk]) / past_close[self.symbol_xlk]
        return_xlv = (latest_close[self.symbol_xlv] - past_close[self.symbol_xlv]) / past_close[self.symbol_xlv]

        # Allocate 100% to the stronger sector
        if return_xlk > return_xlv:
            self.targets = {self.symbol_xlk: 1.0}
        else:
            self.targets = {self.symbol_xlv: 1.0}
