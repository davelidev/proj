from datetime import datetime, timedelta
from AlgorithmImports import *

class SectorRSILeveraged(QCAlgorithm):
    def Initialize(self):
        # 12 year backtest
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100000)

        # High-beta sectors for >30% CAGR
        self.tickers = ["SOXL", "FAS", "TQQQ", "TECL"]
        self.symbols = [self.AddEquity(t, Resolution.Daily).Symbol for t in self.tickers]
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        
        # Indicators: Daily RSI(2) for each asset
        self.rsis = {s: self.RSI(s, 2, MovingAverageType.Wilders, Resolution.Daily) for s in self.symbols}
        self.sma_spy = self.SMA(self.spy, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.spy), 
                         self.TimeRules.AfterMarketOpen(self.spy, 35), 
                         self.Rebalance)
        
        self.SetWarmUp(200)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma_spy.IsReady:
            return

        spy_price = self.Securities[self.spy].Price
        
        if spy_price > self.sma_spy.Current.Value:
            # Bull Market: Look for oversold sectors
            oversold = [s for s in self.symbols if self.rsis[s].IsReady and self.rsis[s].Current.Value < 20]
            
            if oversold:
                # Rank by lowest RSI
                best_s = min(oversold, key=lambda s: self.rsis[s].Current.Value)
                if not self.Portfolio[best_s].Invested:
                    self.Log(f"Bull: {best_s.Value} RSI {self.rsis[best_s].Current.Value:.2f} < 20. Buying.")
                    # Liquidate others and enter the most oversold
                    self.Liquidate()
                    self.SetHoldings(best_s, 1.0)
            else:
                # If nothing is oversold, stay in the current position if it's still healthy
                # or move to cash if RSI > 80 to lock in gains
                for holdings in self.Portfolio.Values:
                    if holdings.Invested:
                        s = holdings.Symbol
                        if self.rsis[s].Current.Value > 80:
                            self.Log(f"Exiting {s.Value}: RSI {self.rsis[s].Current.Value:.2f} > 80.")
                            self.Liquidate(s)
        else:
            # Bear Market
            if self.Portfolio.Invested:
                self.Log("Bear Market: Liquidating.")
                self.Liquidate()
