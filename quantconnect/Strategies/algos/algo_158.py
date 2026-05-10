class Algo158(BaseSubAlgo):
    """
    Gap fill strategy: identifies intraday gaps (open vs previous close) and
    targets a fill within 3 trading days.
    """

    def initialize(self):
        """Set up strategy parameters and initial state."""
        self.gap_threshold = 0.01          # 1% gap significance
        self.max_hold_days = 3
        self.active_trades = {}            # symbol -> trade details
        self.day_counter = 0               # integer day count (no datetime imports)

    def update_targets(self):
        """Evaluate and manage gap fill trades."""
        self.day_counter += 1

        for symbol in self.symbols:
            data = self.GetLastData(symbol)
            if data is None:
                continue

            current_price = data.Close
            open_price = data.Open
            prev_close = data.PreviousClose

            # --- Detect new gap trades ---
            if prev_close != 0 and symbol not in self.active_trades:
                gap_pct = (open_price - prev_close) / prev_close
                if abs(gap_pct) > self.gap_threshold:
                    # Gap up → short, target = previous close
                    if gap_pct > 0:
                        trade = {
                            'direction': -1,
                            'entry_price': open_price,
                            'target_price': prev_close,
                            'entry_day': self.day_counter
                        }
                    # Gap down → long, target = previous close
                    else:
                        trade = {
                            'direction': 1,
                            'entry_price': open_price,
                            'target_price': prev_close,
                            'entry_day': self.day_counter
                        }
                    self.active_trades[symbol] = trade
                    self.Log(f"New gap trade on {symbol}: {trade}")

            # --- Manage existing trades ---
            for sym, trade in list(self.active_trades.items()):
                # Re‑fetch current price for this symbol
                data_sym = self.GetLastData(sym)
                if data_sym is None:
                    continue
                curr = data_sym.Close

                # 1) Check if target price reached (gap filled)
                if trade['direction'] == 1:          # long (gap down)
                    if curr >= trade['target_price']:
                        self.Log(f"Gap fill target reached for {sym} (long)")
                        del self.active_trades[sym]
                elif trade['direction'] == -1:       # short (gap up)
                    if curr <= trade['target_price']:
                        self.Log(f"Gap fill target reached for {sym} (short)")
                        del self.active_trades[sym]

                # 2) Check time expiry (3 days)
                if sym in self.active_trades:
                    days_held = self.day_counter - trade['entry_day']
                    if days_held > self.max_hold_days:
                        self.Log(f"Gap trade expired for {sym} after {days_held} days")
                        del self.active_trades[sym]
