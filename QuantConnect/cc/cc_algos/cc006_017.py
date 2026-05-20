from AlgorithmImports import *

class MegaCapDispersionRegime(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection, self.FineSelection)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.hi200=self.MAX(self.qqq,200,Resolution.Daily); self.lo200=self.MIN(self.qqq,200,Resolution.Daily)
        self.SetWarmUp(220, Resolution.Daily); self.symbols=[]
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)

    def CoarseSelection(self, coarse):
        return [x.Symbol for x in sorted(coarse, key=lambda x: x.DollarVolume, reverse=True)[:100]]
    def FineSelection(self, fine):
        self.symbols=[x.Symbol for x in sorted(fine, key=lambda x: x.MarketCap, reverse=True)[:5]]
        return self.symbols

    def Rebalance(self):
        if self.IsWarmingUp or not(self.hi200.IsReady and self.lo200.IsReady): return
        if not self.symbols: return
        mid=(self.hi200.Current.Value+self.lo200.Current.Value)/2.0
        in_trend = self.Securities[self.qqq].Price>mid
        rets=[]
        for s in self.symbols:
            h=self.History(s, 20, Resolution.Daily)
            if h.empty or len(h)<20: continue
            try:
                r=float(h["close"].iloc[-1])/float(h["close"].iloc[0])-1.0
                rets.append(r)
            except Exception: pass
        if len(rets)<3: return
        mean=sum(rets)/len(rets); var=sum((x-mean)**2 for x in rets)/len(rets); sd=var**0.5
        cohesive = sd < 0.05  # std dev of returns across top-5 mega-caps under 5%
        bull = in_trend and cohesive
        if bull:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq,1.0)
        else:
            if not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil,1.0)

    def OnData(self, data): pass
