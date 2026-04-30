from AlgorithmImports import *
from datetime import datetime, timedelta

class FeaverFrontrunnerV3(QCAlgorithm):             
                                                                                         
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
                                                                                                                      
        for ticker in [                                         
            "SGOV", "SPY", "IOO", "TQQQ", "VTV", "XLF", "QLD", "SPUU",
            "XLK", "KMLM", "ROM", "SSO", "REW", "SDS", "QID",
            "TLT", "PSQ", "CLSE", "AGG", "SH", "IEF", "BND", "QQQ",
        ]:
            self.AddEquity(ticker, Resolution.Daily)

        rsi_specs = (
            [(t, 10) for t in ["SPY", "IOO", "TQQQ", "VTV", "XLF",
                                "QLD", "SPUU", "XLK", "KMLM",
                                "PSQ", "IEF", "BND", "QQQ"]] +
            [(t, 20) for t in ["TLT", "PSQ", "AGG"]] +
            [("SH", 60)]
        )
        self._rsi = {s: self.RSI(s[0], s[1], MovingAverageType.Wilders, Resolution.Daily) for s in rsi_specs}

        self._spy200  = self.SMA("SPY",  200, Resolution.Daily)
        self._tqqq20  = self.SMA("TQQQ",  20, Resolution.Daily)
        self._kmlm20  = self.SMA("KMLM",  20, Resolution.Daily)
        self._qqq_roc = self.ROC("QQQ",   60, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay("SPY"),
            self.TimeRules.BeforeMarketClose("SPY", 30),
            self.Rebalance,
        )
        self.SetWarmUp(210, Resolution.Daily)

    def _ready(self):
        return (
            all(r.IsReady for r in self._rsi.values())
            and self._spy200.IsReady and self._tqqq20.IsReady
            and self._kmlm20.IsReady and self._qqq_roc.IsReady
        )

    def _r(self, ticker, window):
        return self._rsi[(ticker, window)].Current.Value

    def _p(self, ticker):
        return self.Securities[ticker].Price

    # ── Bull regime ───────────────────────────────────────────────────────────
    def _bull_allocs(self):
        if self._r("XLK", 10) > self._r("KMLM", 10):
            return [("ROM", 1/3), ("SSO", 1/3), ("QLD", 1/3)]
        # weight-specified: 0% "Don't Use" / 100% "Use 20d KMLM SMA"
        if self._p("KMLM") < self._kmlm20.Current.Value:
            return [("ROM", 1/3), ("SSO", 1/3), ("QLD", 1/3)]
        return [("REW", 1/3), ("SDS", 1/3), ("QID", 1/3)]

    # ── Bear regime ───────────────────────────────────────────────────────────
    def _bond_baller(self):
        """Feaver Bear Strat V1.1 (Bond Baller Mod) — returns single ticker."""
        if self._r("TLT", 20) > self._r("PSQ", 20):
            return "QLD"
        if self._p("TQQQ") > self._tqqq20.Current.Value:
            if self._r("PSQ", 10) < 35:
                return "CLSE"
            return "QLD" if self._r("AGG", 20) > self._r("SH", 60) else "CLSE"
        return "CLSE" if self._r("IEF", 10) > self._r("PSQ", 20) else "QID"

    def _feaver_bear(self):
        """Feaver Bear — returns single ticker.
        ROC returns % so -12.0 == -12%, matching Composer's cumulative-return."""
        if self._qqq_roc.Current.Value < -12.0:
            return "QLD" if self._r("BND", 10) > self._r("QQQ", 10) else "CLSE"
        if self._p("TQQQ") > self._tqqq20.Current.Value:
            if self._r("PSQ", 10) < 35:
                return "QID"
            return "QLD" if self._r("AGG", 20) > self._r("SH", 60) else "QID"
        return "CLSE" if self._r("IEF", 10) > self._r("PSQ", 20) else "QID"

    def _bear_allocs(self):
        """50% Bond Baller Mod + 50% Feaver Bear; merged if same target."""
        allocs = {}
        for sym in (self._bond_baller(), self._feaver_bear()):
            allocs[sym] = allocs.get(sym, 0.0) + 0.5
        return list(allocs.items())

    # ── Daily rebalance ───────────────────────────────────────────────────────
    def Rebalance(self):
        if self.IsWarmingUp or not self._ready():
            return

        # Overbought shield — any trigger sends everything to SGOV
        if any(self._r(t, 10) > 79 for t in ["SPY", "IOO", "TQQQ", "VTV", "XLF"]):
            allocs = [("SGOV", 1.0)]
        elif self._r("QLD",  10) < 30:
            allocs = [("QLD",  1.0)]
        elif self._r("SPUU", 10) < 30:
            allocs = [("SPUU", 1.0)]
        elif self._p("SPY") > self._spy200.Current.Value:
            allocs = self._bull_allocs()
        else:
            allocs = self._bear_allocs()

        targets = dict(allocs)

        for kvp in self.Portfolio:
            if kvp.Value.Invested and kvp.Key.Value not in targets:
                self.Liquidate(kvp.Key)

        for sym, weight in targets.items():
            self.SetHoldings(sym, weight)

    def OnData(self, data):
        pass
