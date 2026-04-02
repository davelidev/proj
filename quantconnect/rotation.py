# region imports
from AlgorithmImports import *
# endregion

class TQQQForTheLongTerm(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 1, 1)
        self.SetCash(100_000)

        self.Schedule.On(
            self.DateRules.EveryDay("QQQ"),
            self.TimeRules.AfterMarketOpen("QQQ", 35),
            self.Rebalance,
        )

        tickers = ["SPY", "QQQ", "TQQQ", "SPXL", "UVXY", "TECL", "UPRO", "SQQQ", "TLT"]
        self.syms = {t: self.AddEquity(t, Resolution.Daily).Symbol for t in tickers}

        self.rsi10 = {
            t: self.RSI(self.syms[t], 10, MovingAverageType.Wilders, Resolution.Daily)
            for t in tickers
        }
        self.sma_spy200 = self.SMA(self.syms["SPY"],  200, Resolution.Daily)
        self.sma_tqqq20 = self.SMA(self.syms["TQQQ"], 20,  Resolution.Daily)

        self.SetWarmUp(200, Resolution.Daily)

    def _pick(self) -> str:
        rsi10 = self.rsi10
        spy_price  = self.Securities[self.syms["SPY"]].Price
        tqqq_price = self.Securities[self.syms["TQQQ"]].Price

        bull = (
            self.sma_spy200.IsReady
            and spy_price > self.sma_spy200.Current.Value
        )

        if bull:
            # ── BULL: SPY above 200-day MA ─────────────────────────────────
            if rsi10["QQQ"].Current.Value < 20 or rsi10["SPY"].Current.Value < 20:
                return "UVXY"
            return "TQQQ"

        else:
            # ── BEAR: SPY at or below 200-day MA ──────────────────────────
            if rsi10["QQQ"].Current.Value < 30 or rsi10["SPY"].Current.Value < 30:
                return "TQQQ"

            tqqq_below_20sma = (
                self.sma_tqqq20.IsReady
                and tqqq_price < self.sma_tqqq20.Current.Value)

            if tqqq_below_20sma:
                # alternative: ["TECS", "BSV"]
                # Top 1 of [SQQQ, TLT] by RSI(10) — higher RSI wins
                return max(["SQQQ", "TLT"], key=lambda t: rsi10[t].Current.Value)

            # TQQQ at or above its 20-day MA
            if rsi10["SQQQ"].Current.Value < 30:
                return "SQQQ"
            return "TQQQ"

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma_spy200.IsReady or not all(i.IsReady for i in self.rsi10.values()):
            return

        pick = self._pick()
        self.Debug(f"[Rebalance] → {pick}")
        self.SetHoldings(self.syms[pick], 1.0, liquidateExistingHoldings=True)

    def OnData(self, data):
        pass
