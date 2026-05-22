# region imports
from AlgorithmImports import *
from datetime import datetime, timedelta
# endregion

class VolatilitySqueezeAlpha(QCAlgorithm):
    
    def initialize(self) -> None:
        self.set_start_date(2014, 1, 1)
        self.set_end_date(2025, 12, 31)
        self.set_cash(2000)

        self.max_equity = 2000 
        self.base_risk = 0.025 
        self.max_active_positions = 2 

        self.data_objects = {}
        for ticker in ["XAUUSD", "WTICOUSD"]:
            symbol = self.add_cfd(ticker, Resolution.HOUR, Market.OANDA).symbol
            self.data_objects[symbol] = SymbolData(self, symbol)

        self.set_warm_up(200, Resolution.DAILY)

    def on_data(self, data: Slice):
        if self.is_warming_up: 
            return

        equity = self.portfolio.total_portfolio_value
        self.max_equity = max(self.max_equity, equity)
        
        current_risk = self.base_risk * (1.0 if (self.max_equity - equity) / self.max_equity < 0.15 else 0.5)
        active_positions = sum(1 for h in self.portfolio.values() if h.invested)

        for symbol, sd in self.data_objects.items():
            if not data.contains_key(symbol) or not sd.is_ready: 
                continue

            price = data[symbol].price
            holdings = self.portfolio[symbol]
            
            if self.time < sd.next_entry_time: 
                continue

            if not holdings.invested:
                if price > sd.daily_ema.current.value and sd.update_and_check_squeeze():
                    if price > sd.bb.upper_band.current.value and active_positions < self.max_active_positions:
                        stop_dist = sd.atr.current.value * 2.5
                        if stop_dist > 0:
                            self.market_order(symbol, (equity * current_risk) / stop_dist)
                            sd.entry_price = sd.highest_price = price
                            sd.stop_price = price - stop_dist
                            active_positions += 1
            else:
                sd.highest_price = max(sd.highest_price, price)

                profit_pct = (price - sd.entry_price) / sd.entry_price
                multiplier = 1.5 if profit_pct > 0.02 else 2.5
                sd.stop_price = max(sd.stop_price, sd.highest_price - (sd.atr.current.value * multiplier))

                if price < sd.stop_price or price < sd.daily_ema.current.value:
                    self.liquidate(symbol)
                    sd.next_entry_time = self.time + timedelta(hours=12)
                    active_positions -= 1

class SymbolData:
    def __init__(self, algo, symbol):
        self.bb = algo.bb(symbol, 20, 2, MovingAverageType.SIMPLE, Resolution.HOUR)
        self.atr = algo.atr(symbol, 14, MovingAverageType.SIMPLE, Resolution.HOUR)
        self.daily_ema = algo.ema(symbol, 50, Resolution.DAILY)
        
        self.bw_window = RollingWindow[float](100)
        self.entry_price = self.highest_price = self.stop_price = 0.0
        self.next_entry_time = datetime.min

    def update_and_check_squeeze(self):
        middle = self.bb.middle_band.current.value
        bw = (self.bb.upper_band.current.value - self.bb.lower_band.current.value) / middle if middle != 0 else 0
        self.bw_window.add(bw)
        
        if not self.bw_window.is_ready: 
            return True
            
        return bw < (sum(self.bw_window) / self.bw_window.count * 1.1)

    @property
    def is_ready(self):
        return self.daily_ema.is_ready and self.bb.is_ready