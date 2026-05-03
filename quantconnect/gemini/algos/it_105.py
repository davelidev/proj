from AlgorithmImports import *
import numpy as np

class InOutStrategy(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        # Risk-On / Risk-Off Assets
        self.risk_on = self.AddEquity("SPY", Resolution.Daily).Symbol
        self.risk_off = self.AddEquity("TLT", Resolution.Daily).Symbol
        
        # Signal Assets
        self.signals = {
            "XLI": self.AddEquity("XLI", Resolution.Daily).Symbol, # Industrials
            "XLP": self.AddEquity("XLP", Resolution.Daily).Symbol, # Staples
            "DBB": self.AddEquity("DBB", Resolution.Daily).Symbol, # Base Metals
            "GLD": self.AddEquity("GLD", Resolution.Daily).Symbol, # Gold
            "SLV": self.AddEquity("SLV", Resolution.Daily).Symbol, # Silver
            "UUP": self.AddEquity("UUP", Resolution.Daily).Symbol  # USD
        }
        
        self.wait_days = 15
        self.out_day = -100
        
        # Rebalance daily before close
        self.Schedule.On(self.DateRules.EveryDay(self.risk_on),
                         self.TimeRules.BeforeMarketClose(self.risk_on, 15),
                         self.Rebalance)
                         
        self.SetWarmUp(65, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp:
            return
            
        is_risk_off = self.GetSignal()
        
        if is_risk_off:
            self.out_day = self.Time.toordinal()
            
        # If we signaled risk-off recently, stay in bonds
        if (self.Time.toordinal() - self.out_day) < self.wait_days:
            if not self.Portfolio[self.risk_off].Invested:
                self.SetHoldings(self.risk_on, 0)
                self.SetHoldings(self.risk_off, 1.0)
        else:
            if not self.Portfolio[self.risk_on].Invested:
                self.SetHoldings(self.risk_off, 0)
                self.SetHoldings(self.risk_on, 1.0)

    def GetSignal(self):
        # Calculate 60-day ROC for signals
        returns = {}
        for name, symbol in self.signals.items():
            hist = self.History(symbol, 65, Resolution.Daily)
            if hist.empty or len(hist) < 61:
                return False # Default to risk-on if data missing
            
            closes = hist['close']
            returns[name] = (closes.iloc[-1] / closes.iloc[-61]) - 1
            
        # In & Out Logic (Simplified V8 style)
        # 1. Industrials vs Staples
        # 2. Base Metals vs Gold
        # 3. Silver vs Gold
        # 4. USD Strength
        
        risk_off_votes = 0
        if returns["XLI"] < returns["XLP"]: risk_off_votes += 1
        if returns["DBB"] < returns["GLD"]: risk_off_votes += 1
        if returns["SLV"] < returns["GLD"]: risk_off_votes += 1
        if returns["UUP"] > 0.01: risk_off_votes += 1 # USD spike
        
        # If 2 or more indicators signal risk-off, go to safety
        return risk_off_votes >= 2
