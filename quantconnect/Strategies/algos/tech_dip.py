from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class TechDipBuySub(BaseSubAlgo):
    def initialize(self):
        # DISABLE orchestrator warmup to match Day 1 start of tech_dip_orig.py
        self.algo.Settings.AutomaticIndicatorWarmUp = True
        self.algo.Settings.SeedInitialPrices = True

    def get_universes(self):
        return {
            "TechTop5": self.universe_selection
        }

    def universe_selection(self, fundamental):
        # Mirror LargeCapTechStrategy._select exactly
        filtered = [
            f for f in fundamental
            if (f.HasFundamentalData and
                f.AssetClassification.MorningstarSectorCode == MorningstarSectorCode.Technology)
        ]
        top5 = sorted(filtered, key=lambda f: f.MarketCap)[-5:]
        return [f.Symbol for f in top5]

    def on_securities_changed(self, changes):
        # Mirror LargeCapTechStrategy.on_securities_changed exactly
        tech_group = self.universe_groups.get("TechTop5", set())
        
        for sec in changes.AddedSecurities:
            # Check if this security belongs to our specific TechTop5 group
            if sec.Symbol not in tech_group: continue
            
            sec.rsi   = self.algo.RSI(sec.Symbol, 2)
            sec.max   = self.algo.MAX(sec.Symbol, 252)
            sec.sma50 = self.algo.SMA(sec.Symbol, 50)
            
            # Manual Warmup (Claude's hint) to ensure parity from Day 1
            hist = self.algo.History(sec.Symbol, 252, Resolution.Daily)
            for bar in hist.itertuples():
                sec.rsi.Update(bar.Index[1], bar.close)
                sec.max.Update(bar.Index[1], bar.close)
                sec.sma50.Update(bar.Index[1], bar.close)

        for sec in changes.RemovedSecurities:
            # Cleanup targets only if it was one of ours
            if sec.Symbol in tech_group:
                self.targets.pop(sec.Symbol, None)
                self.algo.Liquidate(sec.Symbol)

    def update_targets(self):
        # Check for Weekly parity (Monday)
        if self.algo.Time.weekday() != 0: return
        
        tech_group = self.universe_groups.get("TechTop5", set())
        if not tech_group: return
        
        # Use dynamic weight to match tech_dip_orig.py behavior
        num_selected = len(tech_group)
        w_entry = 1.0 / num_selected if num_selected > 0 else 0.2
        
        for s in tech_group:
            sec = self.algo.Securities[s]
            if not (hasattr(sec, "max") and sec.max.IsReady and sec.sma50.IsReady): continue
            
            if not sec.Invested:
                if sec.rsi.Current.Value < 30 and sec.Price > sec.sma50.Current.Value:
                    self.algo.Log(f"ENTRY {self.algo.Time.date()} {sec.Symbol.Value} rsi={sec.rsi.Current.Value:.1f} price={sec.Price:.2f} max={sec.max.Current.Value:.2f}")
                    self.targets[s] = w_entry
            else:
                reason = "STOP" if sec.Price <= sec.Holdings.AveragePrice * 0.85 else "ATH"
                if sec.Price <= sec.Holdings.AveragePrice * 0.85 or sec.Price >= sec.max.Current.Value:
                    self.algo.Log(f"EXIT  {self.algo.Time.date()} {sec.Symbol.Value} {reason} price={sec.Price:.2f} avg={sec.Holdings.AveragePrice:.2f} max={sec.max.Current.Value:.2f}")
                    if s in self.targets:
                        del self.targets[s]
                else:
                    # PRESERVE DRIFT: Set target to current weight so SetHoldings does nothing
                    # This allows winners to grow past 20%, matching the 31% CAGR of orig
                    # We only do this if it's already in targets
                    if s in self.targets:
                        current_w = sec.Holdings.Quantity * sec.Price / self.algo.Portfolio.TotalPortfolioValue
                        self.targets[s] = current_w


TechDipBuyAlgo = _make_standalone(TechDipBuySub)
