from AlgorithmImports import *

class CMO_Top1Defense(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection, self.FineSelection)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(40, Resolution.Daily); self.symbols=[]

    def CoarseSelection(self, coarse):
        return [x.Symbol for x in sorted(coarse, key=lambda x: x.DollarVolume, reverse=True)[:100]]
    def FineSelection(self, fine):
        self.symbols=[x.Symbol for x in sorted(fine, key=lambda x: x.MarketCap, reverse=True)[:1]]
        return self.symbols

    def Rebalance(self):
        if self.IsWarmingUp or not self.symbols: return
        top1=self.symbols[0]
        h=self.History(self.qqq, 21, Resolution.Daily)
        if h.empty or len(h)<21: return
        c=[float(x) for x in h["close"].values]
        ch=[c[i]-c[i-1] for i in range(1,len(c))]
        up=sum(x for x in ch if x>0); dn=sum(-x for x in ch if x<0); tot=up+dn
        if tot<=0: return
        cmo=100.0*(up-dn)/tot
        bull = cmo > 0
        if bull:
            for sym in list(self.Securities.Keys):
                if sym in (self.qqq, self.tqqq): continue
                if self.Portfolio[sym].Invested: self.Liquidate(sym)
            if not self.Portfolio[self.tqqq].Invested:
                self.SetHoldings(self.tqqq,1.0)
        else:
            if self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.tqqq)
            for sym in list(self.Securities.Keys):
                if sym in (self.qqq, self.tqqq, top1): continue
                if self.Portfolio[sym].Invested: self.Liquidate(sym)
            self.SetHoldings(top1, 1.0)

    def OnData(self, data): pass
