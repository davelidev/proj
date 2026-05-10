class Algo108(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.AddEquity("TQQQ", Resolution.Daily)
        self.symbol = self.Symbol("TQQQ")
        
        # Rolling windows to store recent candles
        self.window_length = 3  # enough for morning star (3 bars)
        self.candle_window = RollingWindow[TradeBar](self.window_length)
        
        # Warm up with history to fill the window
        history = self.History(self.symbol, self.window_length, Resolution.Daily)
        for bar in history:
            self.candle_window.Add(bar)
        
        self.SetWarmUp(self.window_length)

    def OnData(self, data):
        if self.IsWarmingUp:
            return
        
        # Add current bar to window
        if data.Bars.ContainsKey(self.symbol):
            bar = data.Bars[self.symbol]
            self.candle_window.Add(bar)
        
        # Need at least 3 bars to check patterns
        if not self.candle_window.IsReady:
            return
        
        bar0 = self.candle_window[0]  # current (most recent)
        bar1 = self.candle_window[1]  # previous day
        bar2 = self.candle_window[2]  # two days ago
        
        # Check for entry patterns (long only)
        if not self.Portfolio[self.symbol].Invested:
            if self.IsBullishEngulfing(bar1, bar0) or self.IsMorningStar(bar2, bar1, bar0):
                self.SetHoldings(self.symbol, 1.0)  # weight <= 1.0
        else:
            # Exit on opposite patterns
            if self.IsBearishEngulfing(bar1, bar0) or self.IsEveningStar(bar2, bar1, bar0):
                self.Liquidate(self.symbol)
    
    def IsBullishEngulfing(self, previous, current):
        # previous candle must be bearish
        if previous.Close >= previous.Open:
            return False
        # current candle must be bullish
        if current.Close <= current.Open:
            return False
        # current must engulf previous: open < previous close and close > previous open
        if current.Open < previous.Close and current.Close > previous.Open:
            return True
        return False
    
    def IsBearishEngulfing(self, previous, current):
        # previous candle must be bullish
        if previous.Close <= previous.Open:
            return False
        # current candle must be bearish
        if current.Close >= current.Open:
            return False
        # current must engulf previous: open > previous close and close < previous open
        if current.Open > previous.Close and current.Close < previous.Open:
            return True
        return False
    
    def IsMorningStar(self, first, second, third):
        # first: bearish (long)
        if first.Close >= first.Open:
            return False
        # second: small body (doji), preferably gapping down but we simplify
        body_first = abs(first.Close - first.Open)
        body_second = abs(second.Close - second.Open)
        if body_second > 0.3 * body_first:  # second body smaller than 30% of first (tunable)
            return False
        # third: bullish, closes above midpoint of first candle
        if third.Close <= third.Open:
            return False
        midpoint_first = (first.High + first.Low) / 2.0
        if third.Close > midpoint_first:
            return True
        return False
    
    def IsEveningStar(self, first, second, third):
        # first: bullish (long)
        if first.Close <= first.Open:
            return False
        # second: small body
        body_first = abs(first.Close - first.Open)
        body_second = abs(second.Close - second.Open)
        if body_second > 0.3 * body_first:
            return False
        # third: bearish, closes below midpoint of first candle
        if third.Close >= third.Open:
            return False
        midpoint_first = (first.High + first.Low) / 2.0
        if third.Close < midpoint_first:
            return True
        return False