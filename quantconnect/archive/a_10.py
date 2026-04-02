# RSI Frankenfest v1.5(©K) 123 | 28 | 2020
# Converted from Composer symphony to QuantConnect
#
# Top gate: QQQ > EMA(200)?
#   No  → defensive: select-bottom 1 by RSI(10) from bond/defensive list
#   Yes → bull block:
#     RSI(TQQQ,2) < 20  → top 2 by 20-day price stdev from leveraged bull list (50/50)
#     Else:
#       RSI(XLK,10) > RSI(KMLM,10)?
#         Yes → weight-specified 80/20:
#                 80%: RSI(CORP,15) > RSI(XLK,10)  → QLD
#                      Else RSI(IYT,21) > RSI(SPY,21) → QLD
#                      Else → defensive bottom-1
#                 20%: QLD always
#               (if 80% also → QLD, total = QLD 100%)
#         No  → defensive: select-bottom 1 by RSI(10)
#
# Defensive list: BSV, TLT, LQD, VBF, XLP, UGE, XLU, XLV, SPAB, ANGL
# Leveraged bull list: TQQQ, TECL, SOXL, UPRO, QLD, LTL, ROM
#
# Rebalances daily.

from AlgorithmImports import *


class RSIFrankenfestV15(QCAlgorithm):

    DEFENSIVE = ["BSV", "TLT", "LQD", "VBF", "XLP", "UGE", "XLU", "XLV", "SPAB", "ANGL"]
    LEV_BULL  = ["TQQQ", "TECL", "SOXL", "UPRO", "QLD", "LTL", "ROM"]

    def Initialize(self):
        self.SetStartDate(2020, 1, 1)
        self.SetCash(100000)
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.Margin)

        all_tickers = (
            set(self.DEFENSIVE)
            | set(self.LEV_BULL)
            | {"QQQ", "XLK", "KMLM", "CORP", "IYT", "SPY"}
        )
        for ticker in all_tickers:
            self.AddEquity(ticker, Resolution.Daily)

        # EMA(200) for top gate
        self.ema_qqq_200 = self.EMA("QQQ", 200, Resolution.Daily)

        # RSI indicators keyed by (ticker, window)
        rsi_specs = [
            ("TQQQ", 2),
            ("XLK", 10), ("KMLM", 10),
            ("CORP", 15),
            ("IYT", 21), ("SPY", 21),
        ] + [(t, 10) for t in self.DEFENSIVE]

        self.rsi = {}
        for ticker, window in rsi_specs:
            key = (ticker, window)
            if key not in self.rsi:
                self.rsi[key] = self.RSI(ticker, window, MovingAverageType.Wilders, Resolution.Daily)

        self.SetWarmUp(210, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay("QQQ"),
            self.TimeRules.AfterMarketOpen("QQQ", 1),
            self.Rebalance,
        )

    def _is_ready(self):
        return (
            self.ema_qqq_200.IsReady
            and all(ind.IsReady for ind in self.rsi.values())
        )

    def _defensive_bottom1(self):
        """Select-bottom 1 by RSI(10) from defensive list."""
        selected = min(self.DEFENSIVE, key=lambda t: self.rsi[(t, 10)].Current.Value)
        return {selected: 1.0}

    def _top2_by_stdev_price(self, tickers, window=20):
        """Select top 2 by 20-day price standard deviation (highest volatility)."""
        scores = {}
        for ticker in tickers:
            history = self.History(ticker, window, Resolution.Daily)
            if not history.empty and len(history) >= window:
                scores[ticker] = history["close"].std()
        if not scores:
            return ["TQQQ", "QLD"]  # fallback
        top2 = sorted(scores, key=scores.get, reverse=True)[:2]
        return top2

    def _get_target(self):
        # Top gate: QQQ vs EMA(200)
        if self.Securities["QQQ"].Price <= self.ema_qqq_200.Current.Value:
            return self._defensive_bottom1()

        # Bull block
        if self.rsi[("TQQQ", 2)].Current.Value < 20:
            # Oversold: top 2 leveraged by price stdev, equal weight
            top2 = self._top2_by_stdev_price(self.LEV_BULL)
            w = 1.0 / len(top2)
            return {t: w for t in top2}

        rsi_xlk  = self.rsi[("XLK",  10)].Current.Value
        rsi_kmlm = self.rsi[("KMLM", 10)].Current.Value

        if rsi_xlk <= rsi_kmlm:
            return self._defensive_bottom1()

        # Tech momentum positive — weight-specified 80/20
        rsi_corp = self.rsi[("CORP", 15)].Current.Value
        rsi_iyt  = self.rsi[("IYT",  21)].Current.Value
        rsi_spy  = self.rsi[("SPY",  21)].Current.Value

        if rsi_corp > rsi_xlk or rsi_iyt > rsi_spy:
            # Both 80% and 20% portions → QLD
            return {"QLD": 1.0}
        else:
            # 80% defensive bottom-1, 20% QLD
            def_ticker = min(self.DEFENSIVE, key=lambda t: self.rsi[(t, 10)].Current.Value)
            target = {"QLD": 0.2}
            target[def_ticker] = target.get(def_ticker, 0.0) + 0.8
            return target

    def Rebalance(self):
        if self.IsWarmingUp or not self._is_ready():
            return

        target = self._get_target()

        for h in self.Portfolio.Values:
            if h.Invested and h.Symbol.Value not in target:
                self.Liquidate(h.Symbol)

        for ticker, weight in target.items():
            self.SetHoldings(ticker, weight)

    def OnData(self, data):
        pass
