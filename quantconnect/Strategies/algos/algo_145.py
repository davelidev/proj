class Algo145(BaseSubAlgo):
    """
    Cross-asset confirmation strategy: TQQQ, QQQ, AAPL momentum aligned.
    Only enters positions when all three exhibit the same directional momentum.
    """

    def initialize(self):
        # Define the symbols used in the strategy
        self.symbols = ['TQQQ', 'QQQ', 'AAPL']

        # Storage for price history per symbol
        self.price_history = {sym: [] for sym in self.symbols}

        # Number of periods used to calculate momentum
        self.momentum_period = 20

        # Assume base class provides self.data with latest prices
        # Initialize any other state variables if needed

    def update_targets(self):
        """
        Called each time step (e.g., bar close) to update portfolio weights.
        Checks whether momentum of all three assets agrees.
        """
        # Update price histories from incoming data
        for sym in self.symbols:
            if sym in self.data:
                # Access the latest closing price (assuming self.data[sym].close exists)
                self.price_history[sym].append(self.data[sym].close)
                # Keep only the most recent 'momentum_period' prices
                if len(self.price_history[sym]) > self.momentum_period:
                    self.price_history[sym].pop(0)

        # Ensure sufficient data for all symbols
        if not all(len(self.price_history[sym]) >= self.momentum_period for sym in self.symbols):
            # Not enough history – remain neutral (cash)
            self.set_weights({sym: 0.0 for sym in self.symbols})
            return

        # Calculate momentum as the rate of change over the lookback period
        momentum = {}
        for sym in self.symbols:
            prices = self.price_history[sym]
            change = (prices[-1] - prices[0]) / prices[0] if prices[0] != 0 else 0
            momentum[sym] = change

        # Determine if all three are moving in the same direction
        all_positive = all(m > 0 for m in momentum.values())
        all_negative = all(m < 0 for m in momentum.values())

        # Set target weights based on alignment
        if all_positive:
            # Bullish alignment: equal long allocation
            weight = 1.0 / len(self.symbols)
            self.set_weights({sym: weight for sym in self.symbols})
        elif all_negative:
            # Bearish alignment: go to cash (or could short, but here we avoid shorting)
            self.set_weights({sym: 0.0 for sym in self.symbols})
        else:
            # No clear alignment – stay in cash
            self.set_weights({sym: 0.0 for sym in self.symbols})
