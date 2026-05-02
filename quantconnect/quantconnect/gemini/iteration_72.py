from AlgorithmImports import *

class MacroTrendHybrid(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        # Macro Signals (simplified set for efficiency)
        self.signals = {
            "DBB": self.AddEquity("DBB", Resolution.Daily).Symbol,
            "UUP": self.AddEquity("UUP", Resolution.Daily).Symbol,
            "XLI": self.AddEquity("XLI", Resolution.Daily).Symbol,
            "XLU": self.AddEquity("XLU", Resolution.Daily).Symbol
        }
        
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        self.sma = self.SMA(self.tqqq, 50, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq), 
                         self.TimeRules.AfterMarketOpen(self.tqqq, 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(252)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma.IsReady: return
        
        # 1. Macro Signal (60-day ROC)
        hist = self.History(list(self.signals.values()), 61, Resolution.Daily)
        if hist.empty: return
        
        bear_signals = 0
        try:
            # Utils vs Industrials
            xlu_ret = (hist.loc[self.signals["XLU"]]['close'][-1] / hist.loc[self.signals["XLU"]]['close'][0]) - 1
            xli_ret = (hist.loc[self.signals["XLI"]]['close'][-1] / hist.loc[self.signals["XLI"]]['close'][0]) - 1
            if xlu_ret > xli_ret: bear_signals += 1
            
            # Dollar vs Metals
            uup_ret = (hist.loc[self.signals["UUP"]]['close'][-1] / hist.loc[self.signals["UUP"]]['close'][0]) - 1
            dbb_ret = (hist.loc[self.signals["DBB"]]['close'][-1] / hist.loc[self.signals["DBB"]]['close'][0]) - 1
            if uup_ret > dbb_ret: bear_signals += 1
        except:
            return
            
        # 2. Absolute Trend
        price_t = float(self.Securities[self.tqqq].Price)
        sma_val = float(self.sma.Current.Value)
        
        # 3. Hybrid Logic
        if bear_signals == 0 and price_t > sma_val:
            if not self.Portfolio[self.tqqq].Invested:
                self.SetHoldings(self.tqqq, 1.0)
                self.Liquidate(self.bil)
        else:
            if self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
