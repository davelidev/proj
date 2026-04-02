from datetime import datetime, timedelta
from AlgorithmImports import *

class VIXSectorRSI(QCAlgorithm):
    def Initialize(self):
        # 12 year backtest
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100000)

        # High-alpha candidates
        self.tickers = ["SOXL", "FAS", "TQQQ"]
        self.symbols = [self.AddEquity(t, Resolution.Daily).Symbol for t in self.tickers]
        self.vix = self.AddData(CBOE, "VIX", Resolution.Daily).Symbol
        
        # Indicators
        self.rsis = {s: self.RSI(s, 2, MovingAverageType.Wilders, Resolution.Daily) for s in self.symbols}
        self.sma_vix = self.SMA(self.vix, 20, Resolution.Daily) # VIX 20-day trend
        
        self.Schedule.On(self.DateRules.EveryDay(self.symbols[0]), 
                         self.TimeRules.AfterMarketOpen(self.symbols[0], 35), 
                         self.Rebalance)
        
        self.SetWarmUp(30)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma_vix.IsReady:
            return

        vix_price = self.Securities[self.vix].Price
        
        # Logic: Only enter if VIX is relatively calm or declining
        # If VIX > 20-SMA, we are in a high-volatility regime (avoid dip buying)
        is_calm = vix_price < self.sma_vix.Current.Value
        
        if is_calm:
            oversold = [s for s in self.symbols if self.rsis[s].IsReady and self.rsis[s].Current.Value < 20]
            if oversold:
                best_s = min(oversold, key=lambda s: self.rsis[s].Current.Value)
                if not self.Portfolio[best_s].Invested:
                    self.Log(f"VIX Calm ({vix_price:.2f}). {best_s.Value} RSI {self.rsis[best_s].Current.Value:.2f} < 20. Buying.")
                    self.Liquidate()
                    self.SetHoldings(best_s, 1.0)
            else:
                # If invested and RSI becomes overbought, exit
                for holdings in self.Portfolio.Values:
                    if holdings.Invested and holdings.Symbol in self.symbols:
                        if self.rsis[holdings.Symbol].Current.Value > 80:
                            self.Log(f"Exiting {holdings.Symbol.Value} RSI {self.rsis[holdings.Symbol].Current.Value:.2f} > 80.")
                            self.Liquidate(holdings.Symbol)
        else:
            # High Vol Regime: Liquidate everything
            if self.Portfolio.Invested:
                self.Log(f"VIX Spike ({vix_price:.2f} > {self.sma_vix.Current.Value:.2f}). Liquidating.")
                self.Liquidate()
