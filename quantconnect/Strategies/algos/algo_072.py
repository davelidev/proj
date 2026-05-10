class Algo072(BaseSubAlgo):
    """
    Sector breadth rotation strategy.
    If 6 or more of the 10 major sector ETFs have positive 21-day returns,
    we go long an equal-weight basket of all sectors. Otherwise, we go long TQQQ.
    """

    def initialize(self) -> None:
        """Set up algorithm parameters, add securities."""

        # 10 major sector ETFs (covering traditional GICS sectors + telecom)
        sector_tickers = [
            "XLB",  # Materials
            "XLE",  # Energy
            "XLF",  # Financials
            "XLI",  # Industrials
            "XLK",  # Technology
            "XLP",  # Consumer Staples
            "XLU",  # Utilities
            "XLV",  # Health Care
            "XLY",  # Consumer Discretionary
            "IYZ",  # Telecommunications
        ]

        # Add sector ETFs and store their Symbols
        self.sector_symbols = []
        for ticker in sector_tickers:
            sym = self.AddEquity(ticker, Resolution.Daily).Symbol
            self.sector_symbols.append(sym)

        # Add TQQQ (3x leveraged Nasdaq-100 ETF)
        self.tqqq_symbol = self.AddEquity("TQQQ", Resolution.Daily).Symbol

    def update_targets(self) -> None:
        """
        Calculate sector breadth and set portfolio targets.
        The targets dictionary is consumed by the parent class to execute trades.
        """
        # Require at least 22 daily data points to compute reliable 21-day returns
        hist = self.History(self.sector_symbols, 22, Resolution.Daily)
        if hist.empty or len(hist) < 22 * len(self.sector_symbols):
            # Insufficient data – fall back to long the sector basket
            w = 1.0 / len(self.sector_symbols)
            self.targets = {sym: w for sym in self.sector_symbols}
            return

        # For each sector, compute return over the last 21 trading days
        # hist has multi‑index (Symbol, time), we group by Symbol
        closes = hist['close'].groupby(level=0).agg(['first', 'last'])
        # first = close 21 days ago, last = today's close
        returns = (closes['last'] - closes['first']) / closes['first']

        up_count = int((returns > 0).sum())

        if up_count >= 6:
            # Bullish breadth: go long the sector basket equally
            w = 1.0 / len(self.sector_symbols)
            self.targets = {sym: w for sym in self.sector_symbols}
        else:
            # Bearish breadth: go long TQQQ
            self.targets = {self.tqqq_symbol: 1.0}
