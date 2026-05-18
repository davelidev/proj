from AlgorithmImports import *
class CC15_600(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection,self.FineSelection)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._aroon=self.AROON("QQQ",25,Resolution.Daily)
        self.SetWarmUp(35,Resolution.Daily); self._st=None; self.symbols=[]
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),self.TimeRules.AfterMarketOpen(self.qqq,30),self.Rebalance)
    def CoarseSelection(self,coarse):
        return [x.Symbol for x in sorted(coarse,key=lambda x:x.DollarVolume,reverse=True)[:100]]
    def FineSelection(self,fine):
        self.symbols=[x.Symbol for x in sorted(fine,key=lambda x:x.MarketCap,reverse=True)[:5]]; return self.symbols
    def Rebalance(self):
        if self.IsWarmingUp or not self._aroon.IsReady or not self.symbols: return
        osc=self._aroon.AroonUp.Current.Value-self._aroon.AroonDown.Current.Value
        if osc>0:
            self.SetHoldings(self.bil,0)
            per=1.0/len(self.symbols)
            for sym in list(self.Portfolio.Keys):
                if sym in (self.qqq,self.bil): continue
                if sym not in self.symbols and self.Portfolio[sym].Invested: self.Liquidate(sym)
            for s in self.symbols: self.SetHoldings(s,per)
            self._st=1
        elif self._st!=0:
            for sym in list(self.Portfolio.Keys):
                if sym in (self.qqq,self.bil): continue
                if self.Portfolio[sym].Invested: self.Liquidate(sym)
            self.SetHoldings(self.bil,1.0); self._st=0
    def OnData(self,data): pass
