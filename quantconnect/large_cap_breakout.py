from AlgorithmImports import *

class AverageIntraBarVolatility(PythonIndicator):
    def __init__(self, period):
        super().__init__()
        self.Name = "AverageIntraBarVolatility"
        self.sma = SimpleMovingAverage(period)
        self.WarmUpPeriod = period

    @property
    def Value(self):
        """Gets the current value of this indicator."""
        return self.Current.Value

    def Update(self, input: BaseData) -> bool:
        if not hasattr(input, "Open") or input.Open == 0: 
            return False
        
        rang = abs((input.Open - input.Close) / input.Open) * 100
        self.sma.Update(input.EndTime, rang)
        self.Current.Value = self.sma.Current.Value
        
        return self.sma.IsReady

class LargeCapBreakout(QCAlgorithm):

    def initialize(self):
        self.lookback_period = int(self.get_parameter("lookback_period", 240))
        self.breakout_threshold_pct = float(self.get_parameter("breakout_threshold_pct", 0.98))
        self.volatility_low = float(self.get_parameter("volatility_low", 0.1))
        self.volatility_high = float(self.get_parameter("volatility_high", 0.15))
        self.stop_loss_pct = float(self.get_parameter("stop_loss_pct", 0.01))

        assert self.volatility_low < self.volatility_high 

        self.set_start_date(2015, 1, 1)
        self.set_cash(100_000)
        
        # Need minute resolution for the breakout and volatility indicators
        self.universe_settings.resolution = Resolution.MINUTE
        self.settings.automatic_indicator_warm_up = True
        
        self._universe = self.add_universe(self._select)
        
    def _select(self, fundamental):
        filtered = [
            f for f in fundamental
            if (f.has_fundamental_data and 
                f.asset_classification.morningstar_sector_code == MorningstarSectorCode.TECHNOLOGY)
        ]
        # Select the top 5 by market cap
        return [f.symbol for f in sorted(filtered, key=lambda f: f.market_cap)[-5:]] 
    
    def on_securities_changed(self, changes):
        for security in changes.added_securities:
            # Attach custom indicators to each incoming security in the universe
            security.volatility = AverageIntraBarVolatility(self.lookback_period)
            self.register_indicator(security.symbol, security.volatility, Resolution.MINUTE)
            
            security.max_price = self.max(security.symbol, self.lookback_period, Resolution.MINUTE)

        for security in changes.removed_securities:
            self.liquidate(security.symbol)
            self.transactions.cancel_open_orders(security.symbol)
    
    def on_data(self, data):
        # Wait for indicators to warm up and trade only after the first hour of the market
        if self.is_warming_up or self.time.hour < 10:
            return
    
        active_symbols = self._universe.selected
        if not active_symbols:
            return

        # Dynamically size position based on the number of universe selections
        target_weight = 1.0 / len(active_symbols)

        for symbol in active_symbols:
            # Ensure we have data for this symbol in the current slice
            if not data.contains_key(symbol) or data[symbol] is None:
                continue
                
            security = self.securities[symbol]
            
            # Ensure indicators are attached and ready
            if not hasattr(security, 'volatility') or not security.volatility.is_ready or not security.max_price.is_ready:
                continue

            if not security.invested:
                # --- ENTRY LOGIC ---
                # Enter on low volatility when price is near a recent high
                is_low_volatility = security.volatility.Value < self.volatility_low
                is_near_breakout = security.price >= security.max_price.current.value * self.breakout_threshold_pct
                
                if is_low_volatility and is_near_breakout:
                    self.set_holdings(symbol, target_weight)
            else:
                # --- EXIT LOGIC ---
                # Exit if volatility becomes too high
                is_high_volatility = security.volatility.Value > self.volatility_high
                if is_high_volatility:
                    # Liquidate position and cancel the stop loss order to prevent it from firing
                    self.liquidate(symbol)
                    self.transactions.cancel_open_orders(symbol)

    def on_order_event(self, order_event):
        # When a buy order is filled, place a corresponding stop loss order.
        if order_event.status == OrderStatus.FILLED and order_event.direction == OrderDirection.BUY:
            stop_price = order_event.fill_price * (1 - self.stop_loss_pct)
            self.stop_market_order(order_event.symbol, -order_event.fill_quantity, stop_price)