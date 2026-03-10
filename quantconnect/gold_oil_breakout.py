# region imports
from AlgorithmImports import *
from datetime import datetime, timedelta
import numpy as np
# endregion

class VolatilitySqueezeAlpha(QCAlgorithm):
    
    def initialize(self) -> None:
        self.set_start_date(2015, 1, 1)
        self.set_end_date(datetime.now()) 
        self.set_cash(2000)

        self.max_equity = 2000 
        self.tickers = ["XAUUSD", "WTICOUSD"]
        self.data_objects = {}
        
        self.base_risk = 0.025 
        self.max_active_positions = 2 

        for ticker in self.tickers:
            symbol = self.add_cfd(ticker, Resolution.HOUR, Market.OANDA).symbol
            self.data_objects[symbol] = SymbolData(self, symbol)

        self.set_warm_up(200, Resolution.DAILY)

    def on_data(self, data: Slice):
        if self.is_warming_up: return

        current_equity = self.portfolio.total_portfolio_value
        if current_equity > self.max_equity:
            self.max_equity = current_equity
            
        current_drawdown = (self.max_equity - current_equity) / self.max_equity
        risk_multiplier = 1.0 if current_drawdown < 0.15 else 0.5
        current_risk = self.base_risk * risk_multiplier

        active_positions = len([x for x in self.portfolio.values() if x.invested])

        for symbol, sd in self.data_objects.items():
            if not data.contains_key(symbol) or not sd.is_ready: continue

            price = data[symbol].price
            holdings = self.portfolio[symbol]
            
            if self.time < sd.next_entry_time: continue

            # --- ENTRY LOGIC: SQUEEZE BREAKOUT ---
            if not holdings.invested:
                # 1. Daily Trend Guard
                if price > sd.daily_ema.current.value:
                    
                    # 2. Squeeze Check: Is current Bandwidth below the median of last 100 hours?
                    # This ensures we aren't buying a 'blown out' move.
                    current_bw = sd.get_bandwidth()
                    is_squeezed = sd.bandwidth_is_low(current_bw)

                    # 3. Bollinger Breakout
                    if is_squeezed and price > sd.bb.upper_band.current.value:
                        if active_positions < self.max_active_positions:
                            
                            stop_dist = sd.atr.current.value * 2.5
                            if stop_dist > 0:
                                quantity = (current_equity * current_risk) / stop_dist
                                self.market_order(symbol, quantity)
                                
                                sd.entry_price = price
                                sd.highest_price = price
                                sd.stop_price = price - stop_dist
                                sd.entry_time = self.time

            # --- EXIT LOGIC ---
            else:
                if price > sd.highest_price:
                    sd.highest_price = price

                profit_pct = (price - sd.entry_price) / sd.entry_price
                multiplier = 1.5 if profit_pct > 0.02 else 2.5
                trailing_level = sd.highest_price - (sd.atr.current.value * multiplier)
                
                sd.stop_price = max(sd.stop_price, trailing_level)

                if price < sd.stop_price or price < sd.daily_ema.current.value:
                    self.liquidate(symbol)
                    sd.next_entry_time = self.time + timedelta(hours=12)

class SymbolData:
    def __init__(self, algo, symbol):
        self.symbol = symbol
        self.bb = algo.bb(symbol, 20, 2, MovingAverageType.SIMPLE, Resolution.HOUR)
        self.atr = algo.atr(symbol, 14, MovingAverageType.SIMPLE, Resolution.HOUR)
        
        # Daily Filter
        self.daily_consolidator = QuoteBarConsolidator(timedelta(days=1))
        self.daily_ema = ExponentialMovingAverage(50)
        algo.subscription_manager.add_consolidator(symbol, self.daily_consolidator)
        self.daily_consolidator.data_consolidated += lambda sender, bar: self.daily_ema.update(bar.end_time, bar.value)

        # Bandwidth Rolling Window to track "Squeeze"
        self.bw_window = RollingWindow[float](100)

        self.entry_price = 0.0
        self.highest_price = 0.0
        self.stop_price = 0.0
        self.entry_time = datetime.min
        self.next_entry_time = datetime.min

    def get_bandwidth(self):
        # Bandwidth formula: (Upper - Lower) / Middle
        upper = self.bb.upper_band.current.value
        lower = self.bb.lower_band.current.value
        middle = self.bb.middle_band.current.value
        return (upper - lower) / middle if middle != 0 else 0

    def bandwidth_is_low(self, current_bw):
        self.bw_window.add(current_bw)
        if not self.bw_window.is_ready: return True # Allow trading during warmup
        
        # Compare current bandwidth to the historical average
        avg_bw = sum(self.bw_window) / self.bw_window.count
        return current_bw < (avg_bw * 1.1) # Within 10% of the average or lower

    @property
    def is_ready(self):
        return self.daily_ema.is_ready and self.bb.is_ready