from datetime import timedelta
from QuantConnect import *
from QuantConnect.Indicators import *
from QuantConnect.Data.Market import TradeBar

class Algo103(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014,1,1)
        self.SetEndDate(2025,12,31)
        self.SetCash(100000)

        self.symbol = self.AddEquity("TQQQ", Resolution.Daily).Symbol

        # Parameters
        self.lookback = 30
        self.pullback_threshold = 0.02  # 2% proximity to support/resistance
        self.stop_loss_pct = 0.05      # 5% stop loss from entry
        self.rsi_period = 14

        # Indicators
        self.rsi = self.RSI(self.symbol, self.rsi_period, Resolution.Daily)
        self.window = RollingWindow[TradeBar](self.lookback)

        # State
        self.entry_price = None
        self.stop_loss = None
        self.invested = False

    def OnData(self, data):
        if not self.window.IsReady or not self.rsi.IsReady:
            return

        if not data.ContainsKey(self.symbol):
            return

        bar = data[self.symbol]
        close = bar.Close

        # Update rolling window
        self.window.Add(bar)

        # Compute support and resistance using lows/highs of the window (excluding current bar? use full window)
        lows = [b.Low for b in self.window]
        highs = [b.High for b in self.window]
        support = min(lows)
        resistance = max(highs)

        # Check if we have a previous bar for RSI cross
        # Use current RSI and previous RSI (from history)
        history = self.History(self.symbol, 2, Resolution.Daily)
        if history.empty or len(history) < 2:
            return
        prev_close = history.iloc[-2].close
        prev_rsi = None
        # Compute previous RSI manually or use stored value? Simpler: use current RSI and previous RSI from history
        # We'll compute RSI on previous bar using the indicator's current value? RSI.IsReady only after enough data.
        # Instead, we can store RSI values in a rolling list.
        # For simplicity, we'll check if previous close was below support and current close above support (bounce)
        # Or use RSI: if previous RSI < 30 and current RSI > 30, that's confirmation.
        # We'll trust RSI current value and check if it just crossed above 30.
        # We can compare rsi.Current.Value with rsi.Previous.Value (if available). Not all indicators store previous.
        # Let's use a simple check: current RSI > 30 and close > prev_close (if close was near support) as confirmation.

        # If not invested, look for buy signal
        if not self.invested:
            # Check pullback to support: price within threshold of support and today's close > yesterday's close
            if close <= support * (1 + self.pullback_threshold) and close > prev_close and self.rsi.Current.Value > 30:
                # Buy with all available cash
                quantity = int(self.Portfolio.Cash / close)
                if quantity > 0:
                    self.MarketOrder(self.symbol, quantity)
                    self.entry_price = close
                    self.stop_loss = close * (1 - self.stop_loss_pct)
                    self.invested = True
                    self.Debug(f"BUY {quantity} shares at {close:.2f}, stop loss {self.stop_loss:.2f}")
        else:
            # Check exit conditions: stop loss, or touch resistance
            if close <= self.stop_loss:
                self.Liquidate()
                self.invested = False
                self.Debug(f"STOP LOSS at {close:.2f}")
            elif close >= resistance * (1 - self.pullback_threshold) and close < prev_close:
                # Price near resistance and falling - take profit
                self.Liquidate()
                self.invested = False
                self.Debug(f"TAKE PROFIT at {close:.2f}")
