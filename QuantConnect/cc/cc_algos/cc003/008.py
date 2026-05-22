from AlgorithmImports import *

class MegaCapDipBuy(QCAlgorithm):
    def initialize(self):
        self.set_start_date(2014, 1, 1)
        self.set_end_date(2025, 12, 31)
        self.set_cash(100000)
        self.universe_settings.resolution = Resolution.DAILY
        self.add_universe(self.coarse_selection, self.fine_selection)
        self.symbols = []
        
    def coarse_selection(self, coarse):
        return [x.symbol for x in sorted(coarse, key=lambda x: x.dollar_volume, reverse=True)[:100]]

    def fine_selection(self, fine):
        self.symbols = [x.symbol for x in sorted(fine, key=lambda x: x.market_cap, reverse=True)[:5]]
        return self.symbols

    def on_data(self, data):
        for symbol in self.symbols:
            if not data.contains_key(symbol) or data[symbol] is None: continue
            
            hist = self.history(symbol, 20, Resolution.DAILY)
            if len(hist) < 20: continue
            
            high_20 = hist['high'].max()
            price = data[symbol].price
            
            if not self.portfolio[symbol].invested:
                if price < high_20 * 0.95:
                    self.set_holdings(symbol, 0.2)
            else:
                if price >= high_20:
                    self.liquidate(symbol)
