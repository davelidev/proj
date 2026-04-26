from datetime import datetime, timedelta
from AlgorithmImports import *


class TQQQAsymmetricTriple(QCAlgorithm):

    def Initialize(self):
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100_000)
        
        self.sym = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        
        # TriAverage: SMA of an SMA
        self.sma_inner = self.SMA(self.sym, 10, Resolution.Daily)
        self.tri_avg = IndicatorExtensions.SMA(self.sma_inner, 10)
        
        self.sma200 = self.SMA(self.sym, 200, Resolution.Daily)
        self.atr = self.ATR(self.sym, 14, MovingAverageType.Wilders, Resolution.Daily)
        
        self.SetWarmUp(200, Resolution.Daily)
        
        self.Schedule.On(
            self.DateRules.EveryDay(self.sym),
            self.TimeRules.AfterMarketOpen(self.sym, 30),
            self.Rebalance,
        )
        
        self.trailing_stop = 0

    def Rebalance(self):
        if self.IsWarmingUp or not self.tri_avg.IsReady:
            return

        price = self.Securities[self.sym].Price
        tri_val = self.tri_avg.Current.Value
        sma_val = self.sma200.Current.Value
        atr_val = self.atr.Current.Value
        
        # Get previous day low
        history = self.History(self.sym, 2, Resolution.Daily)
        if len(history) < 2: return
        prev_low = history.iloc[-2].low

        if not self.Portfolio.Invested:
            # ENTRY: smoothed trend > prev low AND bull market
            if tri_val > prev_low and price > sma_val:
                self.SetHoldings(self.sym, 1.0)
                self.trailing_stop = price - (3 * atr_val)
                self.Debug(f"TRIPLE ENTRY at {price}")
        else:
            # EXIT: Price below smoothed average OR trend break OR trailing stop
            new_stop = price - (3 * atr_val)
            if new_stop > self.trailing_stop:
                self.trailing_stop = new_stop
                
            if price < tri_val or price < sma_val or price < self.trailing_stop:
                self.Liquidate(self.sym)
                self.Debug(f"TRIPLE EXIT at {price}")
