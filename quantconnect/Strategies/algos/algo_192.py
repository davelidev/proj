class Algo192(BaseSubAlgo):
    def initialize(self):
        self.AddEquity("SPY")
        self.AddEquity("QQQ")
        self.AddEquity("IWM")
        self.period = 20
        self.price_history = {"SPY": [], "QQQ": [], "IWM": []}

    def update_targets(self):
        self.targets = {}
        for symbol, history in self.price_history.items():
            price = self.Securities[symbol].Price
            history.append(price)
            if len(history) > self.period:
                history.pop(0)
            if len(history) == self.period:
                sma = sum(history) / self.period
                # Short when price drops significantly below the SMA (crash scenario)
                if price < sma * 0.98:
                    self.targets[symbol] = -0.33  # equal short weight across symbols
                else:
                    self.targets[symbol] = 0
            else:
                self.targets[symbol] = 0
