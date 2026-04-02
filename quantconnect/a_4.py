# Wooden ARKK Machine 2.2
# Converted from Composer symphony to QuantConnect
#
# Logic:
#   If RSI(IEI, 7) > RSI(SPHB, 7):
#       Bull branch: select bottom 1 asset by 4-bar moving average return from
#           [TARK, TECL, UPRO, TMF, YINN, EDC, SOXX]
#   Else:
#       Bear branch: select bottom 1 asset by 4-bar moving average return from
#           [SARK, PSQ, TMV, DRV, TYO]
#   Hold selected asset at 100% weight, rebalance daily.

from AlgorithmImports import *


class WoodenARKKMachine22(QCAlgorithm):

    BULL_ASSETS = ["TARK", "TECL", "UPRO", "TMF", "YINN", "EDC", "SOXX"]
    BEAR_ASSETS = ["SARK", "PSQ", "TMV", "DRV", "TYO"]
    RSI_WINDOW = 7
    MAR_WINDOW = 4  # moving-average-return window (trading days)

    def Initialize(self):
        self.SetStartDate(2021, 1, 1)
        self.SetCash(100000)
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.Margin)

        # Add all symbols
        for ticker in self.BULL_ASSETS + self.BEAR_ASSETS + ["IEI", "SPHB"]:
            self.AddEquity(ticker, Resolution.Daily)

        # RSI indicators for the branching condition
        self.rsi_iei  = self.RSI("IEI",  self.RSI_WINDOW, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi_sphb = self.RSI("SPHB", self.RSI_WINDOW, MovingAverageType.Wilders, Resolution.Daily)

        self.SetWarmUp(max(self.RSI_WINDOW * 2, self.MAR_WINDOW + 1), Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay("IEI"),
            self.TimeRules.AfterMarketOpen("IEI", 1),
            self.Rebalance,
        )

    def Rebalance(self):
        if self.IsWarmingUp:
            return
        if not self.rsi_iei.IsReady or not self.rsi_sphb.IsReady:
            return

        candidates = (
            self.BULL_ASSETS
            if self.rsi_iei.Current.Value > self.rsi_sphb.Current.Value
            else self.BEAR_ASSETS
        )

        selected = self._select_bottom_1_by_mar(candidates)
        if selected is None:
            return

        # Liquidate anything not selected
        for holding in self.Portfolio.Values:
            if holding.Invested and holding.Symbol.Value != selected:
                self.Liquidate(holding.Symbol)

        self.SetHoldings(selected, 1.0)

    def _select_bottom_1_by_mar(self, tickers):
        """Return the ticker with the lowest moving-average return over MAR_WINDOW bars."""
        scores = {}
        for ticker in tickers:
            history = self.History(ticker, self.MAR_WINDOW + 1, Resolution.Daily)
            if history.empty or len(history) < self.MAR_WINDOW + 1:
                self.Debug(f"Insufficient history for {ticker}, skipping.")
                continue
            closes = history["close"]
            mar = closes.iloc[-1] / closes.iloc[0] - 1
            scores[ticker] = mar

        if not scores:
            self.Debug("No valid scores — skipping rebalance.")
            return None

        return min(scores, key=scores.get)

    def OnData(self, data):
        pass
