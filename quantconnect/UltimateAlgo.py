from AlgorithmImports import *

# --- Sub-Algo Definitions (Strictly Independent Logic) ---

class BaseSubAlgo:
    def __init__(self, algo, identifier):
        self.algo = algo
        self.id = identifier
        self.equity = 20000.0
        self.targets = {}
        self.active = False
    def update_targets(self): return False

class VolatilityBreakoutSub(BaseSubAlgo):
    def __init__(self, algo):
        super().__init__(algo, "VolBreakout")
        self.sym = self.algo.AddEquity("TQQQ", Resolution.Minute).Symbol
        self.volatility = AverageIntraBarVolatility(240)
        self.algo.RegisterIndicator(self.sym, self.volatility, Resolution.Minute)
        self.high = self.algo.MAX(self.sym, 240, Resolution.Minute)
        self.entry_price = 0

    def update_targets(self):
        if self.algo.IsWarmingUp or self.algo.Time.hour < 10: return False
        price = self.algo.Securities[self.sym].Price
        changed = False
        if not self.active:
            if self.volatility.Value < 0.1 and price >= self.high.Current.Value * 0.98:
                self.active = True
                self.entry_price = price
                changed = True
        else:
            if self.volatility.Value > 0.15 or price <= self.entry_price * 0.97:
                self.active = False
                changed = True
        self.targets = {self.sym: 1.0 if self.active else 0}
        return changed

class TechDipBuySub(BaseSubAlgo):
    def __init__(self, algo):
        super().__init__(algo, "TechDip")
        self.selected_syms = []
        self.targets = {}
    def update_targets(self):
        changed = False
        if not self.selected_syms: return False
        w = 1.0 / len(self.selected_syms)
        for s in self.selected_syms:
            sec = self.algo.Securities[s]
            if not (hasattr(sec, "rsi") and sec.rsi.IsReady): continue
            old_w = self.targets.get(s, 0)
            if old_w == 0:
                if sec.rsi.Current.Value < 30 and sec.Price > sec.sma50.Current.Value:
                    self.targets[s] = w
                    changed = True
            else:
                avg_price = sec.Holdings.AveragePrice if sec.Invested else 0
                if (avg_price > 0 and sec.Price <= avg_price * 0.85) or sec.Price >= sec.max.Current.Value:
                    self.targets[s] = 0
                    changed = True
        return changed

class LeveragedRebalanceSub(BaseSubAlgo):
    def __init__(self, algo):
        super().__init__(algo, "LevRebal")
        assets = ["TQQQ", "SOXL", "TECL"]
        self.syms = [self.algo.AddEquity(t, Resolution.Daily).Symbol for t in assets]
        self.targets = {s: 0.20 for s in self.syms}
    def update_targets(self): return False

class RSIDipChampionSub(BaseSubAlgo):
    def __init__(self, algo):
        super().__init__(algo, "RSIDip")
        self.algo.AddEquity("QQQ", Resolution.Daily)
        self.rsi2 = self.algo.RSI("QQQ", 2, MovingAverageType.Wilders, Resolution.Daily)
        assets = ["TQQQ", "SOXL", "TECL"]
        self.syms = [self.algo.AddEquity(t, Resolution.Daily).Symbol for t in assets]
    def update_targets(self):
        if not self.rsi2.IsReady: return False
        weight = 0.333 if self.rsi2.Current.Value < 25 else 0
        changed = (self.targets.get(self.syms[0], -1) != weight)
        self.targets = {s: weight for s in self.syms}
        return changed

class TQQQDynamicSub(BaseSubAlgo):
    def __init__(self, algo):
        super().__init__(algo, "TQQQDyn")
        self.sym = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.rsi2 = self.algo.RSI(self.sym, 2, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi10 = self.algo.RSI(self.sym, 10, MovingAverageType.Wilders, Resolution.Daily)
        self.sma200 = self.algo.SMA(self.sym, 200, Resolution.Daily)
        self.current_weight = 0
    def update_targets(self):
        if not (self.rsi2.IsReady and self.sma200.IsReady): return False
        price = self.algo.Securities[self.sym].Price
        new_w = 0.5
        if price > self.sma200.Current.Value:
            if self.rsi10.Current.Value > 80: new_w = 0.2
            elif self.rsi2.Current.Value < 30: new_w = 1.0
        else: new_w = 0
        changed = (self.current_weight != new_w)
        self.current_weight = new_w
        self.targets = {self.sym: self.current_weight}
        return changed

class AverageIntraBarVolatility(PythonIndicator):
    def __init__(self, period):
        super().__init__()
        self.sma = SimpleMovingAverage(period)
    def Update(self, input):
        if not hasattr(input, "Open") or input.Open == 0: return False
        self.sma.Update(input.EndTime, abs((input.Open - input.Close) / input.Open) * 100)
        self.Current.Value = self.sma.Current.Value
        return self.sma.IsReady
    @property
    def Value(self): return self.Current.Value

class UltimateAlgo(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        
        # ADD BIL FOR HEDGING REMAINING CASH
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.sub_algos = [VolatilityBreakoutSub(self), TechDipBuySub(self), LeveragedRebalanceSub(self), RSIDipChampionSub(self), TQQQDynamicSub(self)]
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.TechUniverseSelection)
        self.SetWarmUp(252)
        self.Schedule.On(self.DateRules.EveryDay("SPY"), self.TimeRules.AfterMarketOpen("SPY", 45), self.PerformDailyUpdate)

    def TechUniverseSelection(self, fundamental):
        tech = [f for f in fundamental if f.AssetClassification.MorningstarSectorCode == MorningstarSectorCode.Technology]
        top5 = sorted(tech, key=lambda x: x.MarketCap, reverse=True)[:5]
        return [x.Symbol for x in top5]

    def OnSecuritiesChanged(self, changes):
        tech_sub = self.sub_algos[1]
        for sec in changes.AddedSecurities:
            if sec.Symbol.Value in ["TQQQ", "QQQ", "SOXL", "TECL", "SPY", "BIL"]: continue
            sec.rsi = self.RSI(sec.Symbol, 2); sec.max = self.MAX(sec.Symbol, 252); sec.sma50 = self.SMA(sec.Symbol, 50)
            hist = self.History(sec.Symbol, 252, Resolution.Daily)
            for bar in hist.itertuples():
                sec.rsi.Update(bar.Index[1], bar.close)
                sec.max.Update(bar.Index[1], bar.close)
                sec.sma50.Update(bar.Index[1], bar.close)
            if sec.Symbol not in tech_sub.selected_syms: tech_sub.selected_syms.append(sec.Symbol)
        for sec in changes.RemovedSecurities:
            if sec.Symbol in tech_sub.selected_syms: tech_sub.selected_syms.remove(sec.Symbol)
            if sec.Symbol in tech_sub.targets: del tech_sub.targets[sec.Symbol]

    def PerformDailyUpdate(self):
        if self.IsWarmingUp: return
        reset_val = self.Portfolio.TotalPortfolioValue / 5.0
        for algo in self.sub_algos: algo.equity = reset_val
        for algo in self.sub_algos: algo.update_targets()
        self.ExecuteAggregation()

    def ExecuteAggregation(self):
        total_val = self.Portfolio.TotalPortfolioValue
        if total_val <= 0: return
        agg_weights = {}
        for algo in self.sub_algos:
            for sym, weight in algo.targets.items():
                agg_weights[sym] = agg_weights.get(sym, 0) + (weight * 0.2)
        
        # BUY REMAINING IN BIL
        total_used = sum(agg_weights.values())
        remaining = max(0, 1.0 - total_used)
        if remaining > 0.01:
            agg_weights[self.bil] = remaining

        total_w = sum(agg_weights.values())
        if total_w > 1.0:
            for s in agg_weights: agg_weights[s] /= total_w
        for sym, weight in agg_weights.items():
            if weight > 0 or self.Portfolio[sym].Invested: self.SetHoldings(sym, weight)
        for x in self.Portfolio.Values:
            if x.Invested and x.Symbol not in agg_weights: self.Liquidate(x.Symbol)

    def OnData(self, data):
        if self.IsWarmingUp: return
        if self.sub_algos[0].update_targets(): self.ExecuteAggregation()
