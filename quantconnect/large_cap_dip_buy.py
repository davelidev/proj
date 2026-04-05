from AlgorithmImports import *


class LargeCapTechStrategy(QCAlgorithm):

    def initialize(self):
        self.SetStartDate(2015, 1, 1)
        self.SetStartDate(2015, 1, 1)
        self.set_cash(100_000)
        self.universe_settings.resolution = Resolution.DAILY
        self.settings.automatic_indicator_warm_up = True
        self.settings.seed_initial_prices = True
        self._selection_data = {}        
        self._universe = self.add_universe(self._select)
        self.schedule.on(
            self.date_rules.week_start("SPY"),
            self.time_rules.at(10, 5),
            self._rebalance,
        )
    
    def _select(self, fundamental):
        filtered = [
            f for f in fundamental
            if (f.has_fundamental_data and 
                f.asset_classification.morningstar_sector_code == MorningstarSectorCode.TECHNOLOGY)
        ]
        return [f.symbol for f in sorted(filtered, key=lambda f: f.market_cap,)[-5:]] 
    
    def on_securities_changed(self, changes):
        for security in changes.added_securities:
            security.rsi = self.rsi(security, 2)
            security.max = self.max(security, 252)
        for security in changes.removed_securities:
            self.liquidate(security)
    
    def _rebalance(self):
        for symbol in self._universe.selected:   
            security = self.securities[symbol]
            if not security.max.is_ready:
                continue                        
            # Buy signal: price below rsi and not invested
            if not security.invested and security.rsi.current.value < 25:
                self.set_holdings(security, 1 / len(self._universe.selected))
            # Sell signal: price at or above 1yr-high and invested
            elif security.invested and security.price >= security.max.current.value:
                self.liquidate(security)
