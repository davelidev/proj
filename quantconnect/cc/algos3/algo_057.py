class Algo057(QCAlgorithm):
    """Daily trading algorithm using day-of-week + 21-day momentum on all-sector top-10 universe."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        # Hardcode TQQQ as per instruction
        self.AddEquity("TQQQ", Resolution.Daily)

        # Universe selection: top-10 by market cap (all sectors)
        self.AddUniverse(self.CoarseSelectionFunction)

        # Basket of symbols (dynamic universe only, NOT including TQQQ)
        self.basket = {}

        # Indicators dictionary (symbol -> ROC(21))
        self.indicators = {}

        # Rebalance every Monday (DayOfWeek.Monday = 0 in .NET)
        self.rebalance_day = 1   # Monday

    def CoarseSelectionFunction(self, coarse):
        """Select top-10 by market cap from all stocks with fundamental data."""
        filtered = [c for c in coarse if c.HasFundamentalData and c.Price > 0]
        sorted_by_cap = sorted(filtered, key=lambda c: c.MarketCap, reverse=True)
        top10 = sorted_by_cap[:10]

        # Exclude TQQQ if it appears (already added manually)
        symbols = [c.Symbol for c in top10 if str(c.Symbol) != "TQQQ"]
        return symbols

    def OnSecuritiesChanged(self, changes):
        """Maintain indicators for added/removed universe symbols."""
        for added in changes.AddedSecurities:
            sym = added.Symbol
            if sym not in self.indicators:
                # Create and warm up ROC(21) indicator
                roc = self.ROC(sym, 21, Resolution.Daily)
                history = self.History(sym, 22, Resolution.Daily)  # need at least 21 bars
                if not history.empty:
                    for index, row in history.loc[sym].iterrows():
                        roc.Update(index, row["close"])
                self.indicators[sym] = roc

        for removed in changes.RemovedSecurities:
            sym = removed.Symbol
            if sym in self.indicators:
                del self.indicators[sym]
            # Liquidate any position in removed symbol
            if self.Portfolio[sym].Invested:
                self.Liquidate(sym)

    def OnData(self, data):
        """Entry pattern: Monday + positive 21-day momentum."""
        # Only rebalance on Mondays
        if self.Time.dayofweek != self.rebalance_day:
            return

        # Collect all actively traded symbols (TQQQ + current basket)
        all_symbols = [Symbol.Create("TQQQ", SecurityType.Equity, Market.USA)]
        all_symbols.extend(list(self.basket.keys()))  # basket keys are symbols from universe

        # Build list of symbols with positive 21-day momentum
        positive = []

        # Check TQQQ
        tqqq = Symbol.Create("TQQQ", SecurityType.Equity, Market.USA)
        if tqqq not in self.indicators:
            # Build indicator if not already present (should exist from Initialize)
            self.indicators[tqqq] = self.ROC(tqqq, 21, Resolution.Daily)
            history = self.History(tqqq, 22, Resolution.Daily)
            if not history.empty:
                for index, row in history.loc[tqqq].iterrows():
                    self.indicators[tqqq].Update(index, row["close"])
        if self.indicators[tqqq].IsReady and self.indicators[tqqq].Current.Value > 0:
            positive.append(tqqq)

        # Check universe symbols
        for sym in all_symbols:
            if sym == tqqq:
                continue
            if sym in self.indicators and self.indicators[sym].IsReady:
                if self.indicators[sym].Current.Value > 0:
                    positive.append(sym)

        # Equal-weight among positive momentum assets, else liquidate
        if positive:
            weight = 1.0 / len(positive)
            for sym in positive:
                self.SetHoldings(sym, weight)
        else:
            # Liquidate all positions
            for sym in all_symbols:
                self.Liquidate(sym)

        # Liquidate any held symbols not in positive list
        for sym in all_symbols:
            if sym not in positive and self.Portfolio[sym].Invested:
                self.Liquidate(sym)
