from AlgorithmImports import *
from datetime import timedelta

class Algo078(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.Resolution = Resolution.Daily

        # Define universe of ETFs (stocks, bonds, gold, emerging markets)
        self.symbols = [Symbol.Create("SPY", SecurityType.Equity, Market.USA),
                        Symbol.Create("AGG", SecurityType.Equity, Market.USA),
                        Symbol.Create("GLD", SecurityType.Equity, Market.USA),
                        Symbol.Create("EEM", SecurityType.Equity, Market.USA)]
        for symbol in self.symbols:
            self.AddEquity(symbol, Resolution.Daily)

        # Schedule monthly rebalance on the first trading day of each month
        self.Schedule.On(self.DateRules.MonthStart(self.symbols[0]),
                         self.TimeRules.AfterMarketOpen(self.symbols[0], 30),
                         self.Rebalance)

        self.correlation_window = 252  # one year of trading days
        self.low_corr_threshold = 0.5

    def Rebalance(self):
        # Need at least correlation_window + 1 days of data for returns and correlation
        history = self.History(self.symbols, self.correlation_window + 1, Resolution.Daily)
        if history.empty or len(history.index.levels[0]) < self.correlation_window + 1:
            self.Debug("Not enough history to rebalance")
            return

        # Compute daily returns for each symbol
        close = history['close'].unstack(level=0)
        returns = close.pct_change().dropna()

        # Compute correlation matrix
        corr_matrix = returns.corr()

        # Average pairwise correlation (upper triangle excluding diagonal)
        upper_tri = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        avg_corr = upper_tri.stack().mean()

        self.Debug(f"Average correlation: {avg_corr:.4f}")

        # Get current prices
        prices = {}
        for symbol in self.symbols:
            price = self.Securities[symbol].Price
            if price == 0:
                return  # security not ready
            prices[symbol] = price

        if avg_corr < self.low_corr_threshold:
            # Low correlation -> equal weight
            equal_weight = 1.0 / len(self.symbols)
            for symbol in self.symbols:
                self.SetHoldings(symbol, equal_weight)
            self.Debug("Low correlation: Equal weight")
        else:
            # High correlation -> concentrate into security with best momentum (12-month return)
            # Momentum = (current price / price 252 days ago) - 1
            start_prices = close.iloc[-self.correlation_window-1]  # oldest close in window (t-252)
            latest_prices = close.iloc[-1]                         # most recent close (t)
            momentum = {}
            for symbol in self.symbols:
                if symbol in start_prices.index and symbol in latest_prices.index:
                    mom = latest_prices[symbol] / start_prices[symbol] - 1
                    momentum[symbol] = mom
            best_symbol = max(momentum, key=momentum.get)
            self.Debug(f"High correlation: Concentrate into {best_symbol} with momentum {momentum[best_symbol]:.4f}")
            for symbol in self.symbols:
                weight = 1.0 if symbol == best_symbol else 0.0
                self.SetHoldings(symbol, weight)

        # Ensure no leverage (sum weights <= 1 already satisfied)
        # No SetBrokerageModel used -> default margin, but we enforce no leverage via weights
