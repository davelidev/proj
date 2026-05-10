from AlgorithmImports import *

class Algo074(QCAlgorithm):
    """
    Algorithm: Tech (XLK) vs Healthcare (XLV) relative strength.
    Each month, invest all capital in the security with the best 12-month return.
    No leverage, no margin, no shorting.
    """

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.xlk = self.AddEquity("XLK", Resolution.Daily).Symbol
        self.xlv = self.AddEquity("XLV", Resolution.Daily).Symbol

        # Rebalance on the first trading day of each month
        self.Schedule.On(self.DateRules.MonthStart(), self.TimeRules.AfterMarketOpen(),
                         self.Rebalance)

        self.last_month = -1  # track to avoid multiple rebalances in same month

    def Rebalance(self):
        # Prevent multiple rebalances if scheduled event fires multiple times
        if self.Time.month == self.last_month:
            return
        self.last_month = self.Time.month

        # Request 12 months of daily close data (approx 252 trading days)
        history = self.History([self.xlk, self.xlv], 252, Resolution.Daily)
        if history.empty:
            return

        # Get the latest close and the close from the start of the period
        xlk_close = history.loc[self.xlk]["close"]
        xlv_close = history.loc[self.xlv]["close"]

        if len(xlk_close) < 2 or len(xlv_close) < 2:
            return

        # 12-month return: (current close - close 252 days ago) / close 252 days ago
        xlk_return = (xlk_close.iloc[-1] - xlk_close.iloc[0]) / xlk_close.iloc[0]
        xlv_return = (xlv_close.iloc[-1] - xlv_close.iloc[0]) / xlv_close.iloc[0]

        # Determine which is stronger
        if xlk_return > xlv_return:
            # All in XLK
            self.SetHoldings(self.xlk, 1.0)
            self.SetHoldings(self.xlv, 0.0)
        elif xlv_return > xlk_return:
            # All in XLV
            self.SetHoldings(self.xlv, 1.0)
            self.SetHoldings(self.xlk, 0.0)
        # else: equal returns → do nothing (keep current allocation or cash)
