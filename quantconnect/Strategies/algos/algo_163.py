class Algo163(BaseSubAlgo):
    def initialize(self):
        # Parameters for ADX calculation
        self.period = 14
        self.data_buffer = []  # list of dicts with keys: high, low, close
        self.tr_sum = 0.0
        self.plus_dm_sum = 0.0
        self.minus_dm_sum = 0.0
        self.dx_sum = 0.0
        self.adx = 0.0
        self.initialized = False
        self.prev_high = None
        self.prev_low = None
        self.prev_close = None

    def update_targets(self):
        # Assume self.current_data() returns dict with 'high', 'low', 'close'
        data = self.current_data()
        high = data['high']
        low = data['low']
        close = data['close']

        self.data_buffer.append({'high': high, 'low': low, 'close': close})

        # Need at least 2 bars for True Range and Directional Movement
        if self.prev_high is not None:
            # True Range
            tr = max(high - low,
                     abs(high - self.prev_close),
                     abs(low - self.prev_close))

            # Directional movements
            up_move = high - self.prev_high
            down_move = self.prev_low - low

            plus_dm = up_move if up_move > down_move and up_move > 0 else 0.0
            minus_dm = down_move if down_move > up_move and down_move > 0 else 0.0

            # Accumulate initial sums for first 'period' bars
            if len(self.data_buffer) <= self.period:
                self.tr_sum += tr
                self.plus_dm_sum += plus_dm
                self.minus_dm_sum += minus_dm
            else:
                # Wilder's smoothing from bar period+1 onward
                self.tr_sum = self.tr_sum - (self.tr_sum / self.period) + tr
                self.plus_dm_sum = self.plus_dm_sum - (self.plus_dm_sum / self.period) + plus_dm
                self.minus_dm_sum = self.minus_dm_sum - (self.minus_dm_sum / self.period) + minus_dm

            # Compute DX (first valid after 'period' bars)
            if len(self.data_buffer) > self.period:
                atr = self.tr_sum / self.period
                plus_di = (self.plus_dm_sum / self.period) / atr * 100.0
                minus_di = (self.minus_dm_sum / self.period) / atr * 100.0
                di_sum = plus_di + minus_di
                if di_sum != 0:
                    dx = abs(plus_di - minus_di) / di_sum * 100.0
                else:
                    dx = 0.0

                # Accumulate DX sum for ADX (first period of DX smoothing)
                if not self.initialized:
                    self.dx_sum += dx
                    if len(self.data_buffer) >= self.period * 2:
                        self.initialized = True
                        self.adx = self.dx_sum / self.period
                else:
                    # Wilder's smoothing of DX
                    self.adx = ((self.adx * (self.period - 1)) + dx) / self.period

        # Update previous values
        self.prev_high = high
        self.prev_low = low
        self.prev_close = close

        # Trading decision: stay long if ADX > 25
        if self.initialized and self.adx > 25:
            # Assume self.set_position(1) sets long position
            self.set_position(1)
        else:
            self.set_position(0)
