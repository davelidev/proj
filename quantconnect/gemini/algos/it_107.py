from AlgorithmImports import *
import pandas as pd
import numpy as np

class FundamentalFactorAlgorithm(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1) 
        self.SetEndDate(2025, 12, 31) 
        self.SetCash(100000) 
        
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelectionFunction, self.FineSelectionFunction)
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol 
        
        self.num_screener = 100
        self.num_stocks = 10
        self.formation_days = 200
        self.lowmom = False
        
        # Schedule rebalancing
        self.Schedule.On(self.DateRules.MonthStart("SPY"), self.TimeRules.At(0, 0), self.monthly_rebalance_flag_set)
        self.Schedule.On(self.DateRules.MonthStart("SPY"), self.TimeRules.At(10, 0), self.rebalance)
        
        self.rebalance_flag = 0
        self.first_month_trade_flag = 1
        self.symbols = []
 
    def CoarseSelectionFunction(self, coarse):
        if self.rebalance_flag or self.first_month_trade_flag:
            # Drop stocks with no fundamental data or low price
            selected = [x for x in coarse if (x.HasFundamentalData) and (float(x.Price) > 5)]
            # Rank by dollar volume
            filtered = sorted(selected, key=lambda x: x.DollarVolume, reverse=True) 
            return [x.Symbol for x in filtered[:200]]
        else:
            return self.symbols

    def FineSelectionFunction(self, fine):
        if self.rebalance_flag or self.first_month_trade_flag:
            # Filter for positive EV/EBITDA and Market Cap > 2B
            filtered_fine = [x for x in fine if (x.ValuationRatios.EVToEBITDA > 0) 
                             and (x.EarningReports.BasicAverageShares.ThreeMonths > 0) 
                             and (x.EarningReports.BasicAverageShares.ThreeMonths * x.Price > 2e9)]

            # Rank by EV/EBITDA
            top = sorted(filtered_fine, key = lambda x: x.ValuationRatios.EVToEBITDA, reverse=True)[:self.num_screener]
            self.symbols = [x.Symbol for x in top]
            
            self.rebalance_flag = 0
            self.first_month_trade_flag = 0
            return self.symbols
        else:
            return self.symbols
 
    def OnData(self, data):
        pass
 
    def monthly_rebalance_flag_set(self):
        self.rebalance_flag = 1

    def rebalance(self):
        # Market Regime Filter: SPY vs 120-day SMA
        spy_hist = self.History(self.spy, 120, Resolution.Daily)
        if spy_hist.empty: return
        
        spy_sma = spy_hist['close'].mean()
        
        if self.Securities[self.spy].Price < spy_sma:
            # Market Exit: Liquidate and move to TLT
            self.Liquidate()
            if not self.Securities.ContainsKey("TLT"):
                self.AddEquity("TLT", Resolution.Daily)
            self.SetHoldings("TLT", 1.0)
            return

        if not self.symbols: return
        
        # Calculate 200-day momentum (return)
        chosen_symbols = self.calc_return(self.symbols)
        if not chosen_symbols: return
        
        top_symbols = chosen_symbols[:self.num_stocks]
        
        # Liquidate symbols no longer in the top momentum list
        for symbol in list(self.Portfolio.Keys):
            if symbol == self.spy or symbol.Value == "TLT": continue
            if symbol not in top_symbols: 
                self.Liquidate(symbol)
        
        # Allocate to top momentum stocks
        weight = 0.99 / len(top_symbols)
        for symbol in top_symbols:
            self.SetHoldings(symbol, weight)
 
    def calc_return(self, symbols):
        hist = self.History(symbols, self.formation_days, Resolution.Daily)
        if hist.empty: return []
        
        returns = {}
        for symbol in symbols:
            if symbol in hist.index.levels[0]:
                symbol_hist = hist.loc[symbol]
                if len(symbol_hist) > 1:
                    returns[symbol] = (symbol_hist['close'].iloc[-1] - symbol_hist['close'].iloc[0]) / symbol_hist['close'].iloc[0]
        
        if not returns: return []
        
        sorted_returns = sorted(returns.items(), key=lambda x: x[1], reverse=not self.lowmom)
        return [x[0] for x in sorted_returns]
