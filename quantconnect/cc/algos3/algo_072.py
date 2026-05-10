class Algo072(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        # Define symbols
        self.sectorTickers = ["XLB", "XLE", "XLF", "XLI", "XLK", 
                              "XLP", "XLU", "XLV", "XLY", "XLC"]
        self.tqqqTicker = "TQQQ"

        # Create Symbol objects
        self.sectorSymbols = [Symbol.Create(t, SecurityType.Equity, Market.USA) 
                              for t in self.sectorTickers]
        self.tqqqSymbol = Symbol.Create(self.tqqqTicker, SecurityType.Equity, Market.USA)

        allSymbols = self.sectorSymbols + [self.tqqqSymbol]

        # Add securities with no leverage
        for sym in allSymbols:
            equity = self.AddEquity(sym, Resolution.Daily)
            equity.SetLeverage(1.0)

        # Rolling windows to hold 22 daily closes (today + 21 prior)
        self.windows = {}
        for sym in allSymbols:
            self.windows[sym] = RollingWindow[decimal](22)

        # Preload windows with history
        history = self.History(allSymbols, 22, Resolution.Daily)
        if not history.empty:
            for sym in allSymbols:
                if sym in history.index.levels[1]:
                    closes = history.loc[sym]["close"].values
                    for c in closes:
                        self.windows[sym].Add(c)

        # Warm up for 22 days so the windows are fully populated
        self.SetWarmUp(22)
        self.previousSignal = None

    def OnData(self, data):
        if self.IsWarmingUp:
            return

        # Update rolling windows with today's close
        for sym in self.windows:
            if data.ContainsKey(sym) and data[sym] is not None:
                self.windows[sym].Add(data[sym].Close)

        # Count sector ETFs with positive 21-day return
        positiveCount = 0
        for sym in self.sectorSymbols:
            window = self.windows.get(sym)
            if window is not None and window.IsReady:
                closeToday = window[0]
                close21Ago = window[21]
                if close21Ago != 0:
                    ret = (closeToday - close21Ago) / close21Ago
                    if ret > 0:
                        positiveCount += 1

        # Determine signal
        if positiveCount >= 6:
            signal = "basket"
        else:
            signal = "TQQQ"

        # Rebalance only if signal changes
        if signal != self.previousSignal:
            self.previousSignal = signal

            if signal == "basket":
                # Liquidate TQQQ and go into equal‑weighted sector basket
                self.Liquidate(self.tqqqSymbol)
                weight = 1.0 / len(self.sectorSymbols)  # 0.1
                for sym in self.sectorSymbols:
                    self.SetHoldings(sym, weight)
            else:
                # Liquidate sectors and go all‑in TQQQ
                for sym in self.sectorSymbols:
                    self.Liquidate(sym)
                self.SetHoldings(self.tqqqSymbol, 1.0)
