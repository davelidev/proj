from AlgorithmImports import *

class BinanceTopVolumeMomentum(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)

        # (Optional but recommended for Binance USDT trading to avoid conversion quirks)
        self.SetAccountCurrency("USDT")
        self.SetCash(100000)

        self.SetBrokerageModel(BrokerageName.Binance, AccountType.Margin)

        self.UniverseSettings.Resolution = Resolution.Daily
        self.UniverseSettings.Leverage = 1.0
        self.UniverseSettings.Asynchronous = True  # QC recommends async for crypto universes

        # --- Strategy parameters
        self.TOP_N_UNIVERSE = 7
        self.N_HOLD = 2
        self.WEIGHT = 0.15
        self.MOM_LOOKBACK = 252

        # --- Optional: always keep these subscribed (if you still want them)
        self.extra_pairs = ["USDCUSDT", "TUSDUSDT"]
        for ticker in self.extra_pairs:
            self.AddCrypto(ticker, Resolution.Daily, Market.Binance)

        self.rebalance = False
        self.current_universe = []

        # Universe = top 7 USDT pairs by USD volume (previous day snapshot)
        self.AddUniverse(CryptoUniverse.Binance(self.SelectUniverse))

        # Monthly rebalance
        self.Schedule.On(self.DateRules.MonthStart(), self.TimeRules.At(0, 0), self.TriggerRebalance)

        self.SetWarmUp(self.MOM_LOOKBACK + 5, Resolution.Daily)

    def TriggerRebalance(self):
        self.rebalance = True

    def SelectUniverse(self, universe_day):
        # Keep only USDT-quoted pairs with valid USD volume
        candidates = []
        for c in universe_day:
            sym = getattr(c, "Symbol", None)
            if sym is None:
                continue

            # USDT quote only (avoids unsupported quote currencies)
            if not sym.Value.endswith("USDT"):
                continue

            vol_usd = getattr(c, "VolumeInUsd", None)
            if vol_usd is None:
                vol_usd = getattr(c, "volume_in_usd", None)

            if not vol_usd:
                continue

            candidates.append((sym, float(vol_usd)))

        # Top N by USD volume
        candidates.sort(key=lambda x: x[1], reverse=True)
        selected = [x[0] for x in candidates[:self.TOP_N_UNIVERSE]]

        self.current_universe = selected
        return selected

    def OnSecuritiesChanged(self, changes: SecurityChanges):
        for sec in changes.AddedSecurities:
            sec.SetLeverage(1.0)

    def OnData(self, data: Slice):
        if self.IsWarmingUp or not self.rebalance:
            return
        self.rebalance = False

        symbols = list(self.current_universe)

        # Ensure extra pairs are included even if not selected via universe
        for ticker in self.extra_pairs:
            sym = self.Symbol(ticker)
            if sym not in symbols:
                symbols.append(sym)

        if len(symbols) == 0:
            return

        # Always assign hist before using it
        hist = self.History(symbols, self.MOM_LOOKBACK + 1, Resolution.Daily)
        if hist is None or hist.empty:
            return

        mom = []

        # Iterate only symbols that actually came back from History
        for sym, df in hist.groupby(level=0):
            if df is None or "close" not in df.columns:
                continue

            closes = df["close"].dropna()
            if len(closes) < (self.MOM_LOOKBACK + 1):
                continue

            close_now = float(closes.iloc[-1])
            close_then = float(closes.iloc[-(self.MOM_LOOKBACK + 1)])
            if close_then <= 0:
                continue

            momentum_12m = close_now / close_then - 1.0
            mom.append((sym, momentum_12m))

        if not mom:
            return

        mom.sort(key=lambda x: x[1], reverse=True)
        selected = [x[0] for x in mom[:self.N_HOLD]]

        # Liquidate anything not selected
        for sym in list(self.Securities.Keys):
            if self.Portfolio[sym].Invested and sym not in selected:
                self.Liquidate(sym)

        # Allocate
        for sym in selected:
            if sym in self.Securities and self.Securities[sym].HasData:
                self.SetHoldings(sym, self.WEIGHT)

        self.Debug(f"{self.Time.date()} Selected: {', '.join([s.Value for s in selected])}")
