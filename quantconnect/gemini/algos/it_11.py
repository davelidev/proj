from AlgorithmImports import *

class VAALeveraged(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        # 3x Leveraged Offensive Assets
        self.offensive = ["TQQQ", "SOXL", "TECL", "TNA"]
        self.defensive = ["TLT", "IEF", "BIL"]
        
        self.symbols = {}
        for ticker in self.offensive + self.defensive:
            self.symbols[ticker] = self.AddEquity(ticker, Resolution.Daily).Symbol
            
        self.Schedule.On(self.DateRules.MonthStart("TQQQ"), 
                         self.TimeRules.AfterMarketOpen("TQQQ", 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(252)

    def GetVigilantMomentum(self, symbol):
        hist = self.History(symbol, 253, Resolution.Daily)
        if hist.empty or len(hist) < 253: return -1000
        
        prices = hist['close'].values
        # 1m, 3m, 6m, 12m returns
        r1 = (prices[-1] / prices[-22]) - 1
        r3 = (prices[-1] / prices[-63]) - 1
        r6 = (prices[-1] / prices[-126]) - 1
        r12 = (prices[-1] / prices[-252]) - 1
        
        return 12 * r1 + 4 * r3 + 2 * r6 + 1 * r12

    def Rebalance(self):
        if self.IsWarmingUp: return
        
        off_m = {t: self.GetVigilantMomentum(self.symbols[t]) for t in self.offensive}
        def_m = {t: self.GetVigilantMomentum(self.symbols[t]) for t in self.defensive}
        
        # Logic: If ANY offensive asset has negative momentum, go defensive
        if any(m < 0 for m in off_m.values()):
            best_def = max(def_m, key=def_m.get)
            self.Log(f"[{self.Time}] CRASH PROTECTION. Holding {best_def}.")
            self.SetHoldings(self.symbols[best_def], 1.0)
            for t in self.offensive: self.Liquidate(self.symbols[t])
            for t in self.defensive: 
                if t != best_def: self.Liquidate(self.symbols[t])
        else:
            best_off = max(off_m, key=off_m.get)
            self.Log(f"[{self.Time}] RISK ON. Holding {best_off}.")
            self.SetHoldings(self.symbols[best_off], 1.0)
            for t in self.defensive: self.Liquidate(self.symbols[t])
            for t in self.offensive:
                if t != best_off: self.Liquidate(self.symbols[t])

    def OnData(self, data):
        pass
