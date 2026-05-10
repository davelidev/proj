from QuantConnect import *
from QuantConnect.Algorithm import *
from QuantConnect.Indicators import *
from QuantConnect.Data.Market import TradeBar
from QuantConnect.Data.Fundamental import Fundamental
from Selection.FundamentalUniverseSelectionModel import FundamentalUniverseSelectionModel
from System.Collections.Generic import List
import numpy as np

class Algo006(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        # Always add TQQQ
        self.tqqq = self.AddEquity('TQQQ', Resolution.Daily).Symbol

        # Universe for top-10 market cap stocks
        self.AddUniverse(self._fine_selection, self._fine_selection)

        # Basket dictionary to track holdings and indicators
        self.basket = {}

        # Initialize indicators for TQQQ
        self._add_symbol(self.tqqq)

    def _fine_selection(self, fundamental):
        sorted_by_market_cap = sorted(fundamental, key=lambda x: x.MarketCap, reverse=True)
        top10 = sorted_by_market_cap[:10]
        return [x.Symbol for x in top10]

    def _add_symbol(self, symbol):
        if symbol in self.basket:
            return
        # Add equity if not already added (for universe symbols)
        if not self.Securities.ContainsKey(symbol):
            self.AddEquity(symbol, Resolution.Daily)
        # Create ATR indicator and rolling window
        atr = self.ATR(symbol, 14, Resolution.Daily)
        atr_window = RollingWindow[Decimal](20)
        self.basket[symbol] = {
            'atr': atr,
            'atr_window': atr_window,
            'prev_high': None,
            'prev_low': None
        }

    def OnSecuritiesChanged(self, changes):
        for added in changes.AddedSecurities:
            symbol = added.Symbol
            if symbol not in self.basket and symbol != self.tqqq:
                self._add_symbol(symbol)
        for removed in changes.RemovedSecurities:
            symbol = removed.Symbol
            if symbol in self.basket:
                self.basket.pop(symbol, None)
                self.Liquidate(symbol)

    def _median(self, window):
        if window.Count == 0:
            return Decimal(0)
        values = [float(v) for v in window]
        return Decimal(np.median(values))

    def OnData(self, data):
        # Update rolling windows and compute signal for each symbol
        long_signals = []
        short_signals = []

        for symbol, info in self.basket.items():
            if not data.Bars.ContainsKey(symbol):
                continue
            bar = data.Bars[symbol]
            atr = info['atr']
            atr_window = info['atr_window']

            # Update ATR value into rolling window (current ATR is from previous bar's close)
            # We need to push after the bar is processed; ATR indicator updates with new bar
            # So we push the current ATR value after it updates
            if atr.IsReady:
                atr_window.Add(atr.Current.Value)

            if not atr.IsReady or atr_window.Count < 20:
                # Not enough data, store previous bar info for future use
                info['prev_high'] = bar.High
                info['prev_low'] = bar.Low
                continue

            median_atr = self._median(atr_window)
            if median_atr == 0:
                continue
            ratio = atr.Current.Value / median_atr

            # Check breakout condition (using previous bar's high/low)
            if info['prev_high'] is not None and info['prev_low'] is not None:
                current_close = bar.Close
                if ratio < 0.6:  # Volatility contraction filter
                    if current_close > info['prev_high']:
                        long_signals.append(symbol)
                    elif current_close < info['prev_low']:
                        short_signals.append(symbol)

            # Update previous bar values for next iteration
            info['prev_high'] = bar.High
            info['prev_low'] = bar.Low

        # Set portfolio weights
        total_positions = len(long_signals) + len(short_signals)
        if total_positions == 0:
            # Flat all positions
            for symbol in self.basket:
                if self.Portfolio[symbol].Invested:
                    self.SetHoldings(symbol, 0)
        else:
            weight_per_position = 1.0 / total_positions
            # First set all to zero, then set active positions
            for symbol in self.basket:
                if symbol in long_signals:
                    self.SetHoldings(symbol, weight_per_position)
                elif symbol in short_signals:
                    self.SetHoldings(symbol, -weight_per_position)
                else:
                    self.SetHoldings(symbol, 0)
