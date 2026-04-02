# EM updated with 1x below spy200d and reduced lev FRs
# Converted from Composer symphony to QuantConnect
#
# Regime gate (SPY vs SMA 200):
#   Full lev  (SPY > SMA200): bull signal → EDC 100%,       bear signal → EDZ 100%
#   Reduced lev (SPY ≤ SMA200): bull signal → EEM 100%,    bear signal → EDZ 33% + BIL 67%
#
# Signal tree (same in both regimes):
#   1. RSI(EEM,10) < 25                        → EDC 68% + BIL 32%  (both regimes)
#   2. SHV > SMA(SHV,50):
#        EEM > SMA(EEM,200) → "IEI vs IWM":
#            RSI(IEI,10) > RSI(IWM,15)         → bull
#            else                               → bear
#        EEM ≤ SMA(EEM,200) → two groups equal-weighted:
#            Group A "IGIB vs EEM":
#                RSI(IGIB,15) > RSI(EEM,15)    → bull  (50%)
#                else                           → bear  (50%)
#            Group B "IGIB vs SPY":
#                RSI(IGIB,10) > RSI(SPY,10)    → bull  (50%)
#                else                           → bear  (50%)
#   3. SHV ≤ SMA(SHV,50) → "IGIB vs SPY":
#            RSI(IGIB,10) > RSI(SPY,10)        → bull
#            else                               → bear
#
# Rebalances daily.

from AlgorithmImports import *
from datetime import datetime, timedelta


class EMUpdatedReducedLev(QCAlgorithm):

    def Initialize(self):
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100000)
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.Margin)

        for ticker in ["SPY", "EEM", "SHV", "IEI", "IWM", "IGIB", "EDC", "EDZ", "BIL"]:
            self.AddEquity(ticker, Resolution.Daily)

        self.rsi_eem_10  = self.RSI("EEM",  10, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi_iei_10  = self.RSI("IEI",  10, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi_iwm_15  = self.RSI("IWM",  15, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi_igib_15 = self.RSI("IGIB", 15, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi_eem_15  = self.RSI("EEM",  15, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi_igib_10 = self.RSI("IGIB", 10, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi_spy_10  = self.RSI("SPY",  10, MovingAverageType.Wilders, Resolution.Daily)

        self.sma_spy_200 = self.SMA("SPY", 200, Resolution.Daily)
        self.sma_shv_50  = self.SMA("SHV",  50, Resolution.Daily)
        self.sma_eem_200 = self.SMA("EEM", 200, Resolution.Daily)

        self.SetWarmUp(210, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay("SPY"),
            self.TimeRules.AfterMarketOpen("SPY", 1),
            self.Rebalance,
        )

    def _is_ready(self):
        return all([
            self.rsi_eem_10.IsReady, self.rsi_iei_10.IsReady, self.rsi_iwm_15.IsReady,
            self.rsi_igib_15.IsReady, self.rsi_eem_15.IsReady,
            self.rsi_igib_10.IsReady, self.rsi_spy_10.IsReady,
            self.sma_spy_200.IsReady, self.sma_shv_50.IsReady, self.sma_eem_200.IsReady,
        ])

    @staticmethod
    def _merge(*dicts):
        """Equal-weight merge of multiple allocation dicts."""
        result = {}
        n = len(dicts)
        for d in dicts:
            for ticker, w in d.items():
                result[ticker] = result.get(ticker, 0) + w / n
        return result

    def _bull(self, full_lev):
        return {"EDC": 1.0} if full_lev else {"EEM": 1.0}

    def _bear(self, full_lev):
        return {"EDZ": 1.0} if full_lev else {"EDZ": 0.33, "BIL": 0.67}

    def _igib_vs_spy(self, full_lev):
        if self.rsi_igib_10.Current.Value > self.rsi_spy_10.Current.Value:
            return self._bull(full_lev)
        return self._bear(full_lev)

    def _get_target(self):
        full_lev = self.Securities["SPY"].Price > self.sma_spy_200.Current.Value

        # EEM oversold: EDC/BIL 68/32 in both regimes
        if self.rsi_eem_10.Current.Value < 25:
            return {"EDC": 0.68, "BIL": 0.32}

        if self.Securities["SHV"].Price > self.sma_shv_50.Current.Value:
            if self.Securities["EEM"].Price > self.sma_eem_200.Current.Value:
                # Single signal: IEI vs IWM
                if self.rsi_iei_10.Current.Value > self.rsi_iwm_15.Current.Value:
                    return self._bull(full_lev)
                return self._bear(full_lev)
            else:
                # Two equal-weighted signals: IGIB vs EEM, IGIB vs SPY
                g_igib_eem = (
                    self._bull(full_lev)
                    if self.rsi_igib_15.Current.Value > self.rsi_eem_15.Current.Value
                    else self._bear(full_lev)
                )
                g_igib_spy = self._igib_vs_spy(full_lev)
                return self._merge(g_igib_eem, g_igib_spy)
        else:
            # SHV weak: single signal IGIB vs SPY
            return self._igib_vs_spy(full_lev)

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
