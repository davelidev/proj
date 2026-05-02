from AlgorithmImports import *
import numpy as np

class InAndOutStrategy(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        # --- Strategy Parameters ---
        self.lookback = 252      # 1 year lookback for ROC
        self.wait_days = 15      # "OUT_DAY" wait period to avoid whipsaws
        self.count = 0           # Counter for wait days
        self.be_in = True        # Current state (True = Equities, False = Bonds)
        
        # --- Assets ---
        # Signal Assets (The "Distilled Bear" components)
        self.signals = {
            "DBB": self.AddEquity("DBB", Resolution.Daily).Symbol, # Base Metals
            "UUP": self.AddEquity("UUP", Resolution.Daily).Symbol, # US Dollar
            "XLI": self.AddEquity("XLI", Resolution.Daily).Symbol, # Industrials
            "XLU": self.AddEquity("XLU", Resolution.Daily).Symbol, # Utilities
            "XLP": self.AddEquity("XLP", Resolution.Daily).Symbol, # Consumer Staples
            "XLY": self.AddEquity("XLY", Resolution.Daily).Symbol, # Consumer Discretionary
            "GLD": self.AddEquity("GLD", Resolution.Daily).Symbol, # Gold
            "SLV": self.AddEquity("SLV", Resolution.Daily).Symbol  # Silver
        }
        
        # Trading Assets
        # Using TQQQ for 'In' to see if this macro logic can tame leveraged volatility
        self.equity = self.AddEquity("TQQQ", Resolution.Daily).Symbol 
        self.bond = self.AddEquity("TLT", Resolution.Daily).Symbol   
        
        # Schedule the check daily
        self.Schedule.On(self.DateRules.EveryDay(self.equity), 
                         self.TimeRules.AfterMarketOpen(self.equity, 30), 
                         self.CheckSignal)
                         
        self.SetWarmUp(self.lookback)

    def CheckSignal(self):
        if self.IsWarmingUp: return

        # 1. Calculate Returns (ROC) for signal pairs
        returns = {}
        for symbol in self.signals.values():
            hist = self.History(symbol, self.lookback + 1, Resolution.Daily)
            if not hist.empty:
                prices = hist['close'].values
                returns[symbol] = (prices[-1] / prices[0]) - 1 if prices[0] > 0 else 0
            else:
                return # Wait for data

        # 2. Count Bearish Signals
        # Logic: Defensive assets outperforming offensive ones = Bearish
        bear_signals = 0
        if returns[self.signals["XLU"]] > returns[self.signals["XLI"]]: bear_signals += 1 # Utils > Industrials
        if returns[self.signals["UUP"]] > returns[self.signals["DBB"]]: bear_signals += 1 # Dollar > Metals
        if returns[self.signals["XLP"]] > returns[self.signals["XLY"]]: bear_signals += 1 # Staples > Discretionary
        if returns[self.signals["GLD"]] > returns[self.signals["SLV"]]: bear_signals += 1 # Gold > Silver

        # 3. Determine "In" or "Out" status
        # If any signal is bearish, we immediately go "Out"
        if bear_signals > 0:
            self.be_in = False
            self.count = 0 # Reset wait counter when we go Out
        else:
            # If all signals are bullish, wait for 'wait_days' before going back In
            self.count += 1
            if self.count >= self.wait_days:
                self.be_in = True

        # 4. Execute Trades
        if self.be_in:
            if not self.Portfolio[self.equity].Invested:
                self.Log(f"[{self.Time}] SIGNAL: IN (Equities) | Bear Count: {bear_signals}")
                self.Liquidate(self.bond)
                self.SetHoldings(self.equity, 1.0)
        else:
            if not self.Portfolio[self.bond].Invested:
                self.Log(f"[{self.Time}] SIGNAL: OUT (Bonds) | Bear Count: {bear_signals}")
                self.Liquidate(self.equity)
                self.SetHoldings(self.bond, 1.0)

    def OnData(self, data):
        pass
