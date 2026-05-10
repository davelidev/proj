# QuantConnect Algorithm Algo0082
# Strategy: Monthly factor rotation between momentum, value, and quality.
# Uses only SetStartDate, SetEndDate, SetCash, AddEquity, SetHoldings.
# No SetBrokerageModel.

class Algo0082(QCAlgorithm):

    def Initialize(self):
        # Set date range and initial cash
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 1, 1)
        self.SetCash(100000)

        # Add factor ETFs: momentum, value, quality
        self.factors = ["MTUM", "VLUE", "QUAL"]
        for ticker in self.factors:
            self.AddEquity(ticker, Resolution.Daily)

        # Keep track of the last month we rebalanced
        self.last_rebalance_month = -1

    def OnData(self, data):
        # Rebalance only on the first trading day of each month
        current_month = self.Time.month
        if current_month == self.last_rebalance_month:
            return
        self.last_rebalance_month = current_month

        best_factor = None
        best_return = -float('inf')

        # Evaluate 12-month return for each factor
        for factor in self.factors:
            if not data.ContainsKey(factor) or not self.Securities[factor].HasData:
                continue

            # Request the last 252 daily bars (approx 1 year)
            history = self.History(factor, 252, Resolution.Daily)
            if history.empty or len(history) < 252:
                continue  # Not enough history yet

            # Current price from today's bar
            current_price = data[factor].Close
            # Price 252 trading days ago (approximately 12 months)
            price_12m_ago = history.iloc[0].Close  # Oldest bar in the window

            # Simple return over the period
            ret = (current_price - price_12m_ago) / price_12m_ago
            if ret > best_return:
                best_return = ret
                best_factor = factor

        # Allocate 100% of the portfolio to the best factor, liquidating others
        if best_factor is not None:
            self.SetHoldings(best_factor, 1.0)
