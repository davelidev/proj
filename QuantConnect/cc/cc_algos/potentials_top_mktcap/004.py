from AlgorithmImports import *

class NasdaqBreadthRotation(QCAlgorithm):
    def initialize(self):
        self.set_start_date(2014, 1, 1)
        self.set_end_date(2025, 12, 31)
        self.set_cash(100000)
        self.tqqq = self.add_equity("TQQQ", Resolution.DAILY).symbol
        self.universe_settings.resolution = Resolution.DAILY
        self.add_universe(self.coarse_selection, self.fine_selection)
        self.symbols = []
        self.emas = {}
        
    def coarse_selection(self, coarse):
        return [x.symbol for x in sorted(coarse, key=lambda x: x.dollar_volume, reverse=True)[:100]]

    def fine_selection(self, fine):
        self.symbols = [x.symbol for x in sorted(fine, key=lambda x: x.market_cap, reverse=True)[:10]]
        for symbol in self.symbols:
            self.add_equity(symbol, Resolution.DAILY)
            if symbol not in self.emas:
                self.emas[symbol] = self.ema(symbol, 50, Resolution.DAILY)
        return self.symbols

    def on_data(self, data):
        if not self.emas: return
        
        above_count = 0
        ready_count = 0
        for symbol in self.symbols:
            if symbol in self.emas and self.emas[symbol].is_ready:
                ready_count += 1
                if self.securities[symbol].price > self.emas[symbol].current.value:
                    above_count += 1
        
        if ready_count > 0:
            breadth = above_count / ready_count
            if breadth > 0.6:
                self.set_holdings(self.tqqq, 1.0)
            elif breadth < 0.4:
                self.liquidate(self.tqqq)
