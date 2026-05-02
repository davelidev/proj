from AlgorithmImports import *

class MomentumVolScaling(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.spy_sma = self.SMA(self.spy, 200, Resolution.Daily)
        
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelection, self.FineSelection)
        
        self.lookback = 252
        self.num_stocks = 5
        self.selected_symbols = []
        
        # Monthly rebalance
        self.Schedule.On(self.DateRules.MonthStart(self.spy), 
                         self.TimeRules.AfterMarketOpen(self.spy, 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(self.lookback)

    def CoarseSelection(self, coarse):
        # Filter for stocks with fundamental data and minimum price/volume
        sorted_by_dollar_volume = sorted([x for x in coarse if x.HasFundamentalData and x.Price > 5],
                                         key=lambda x: x.DollarVolume, reverse=True)
        return [x.Symbol for x in sorted_by_dollar_volume[:100]]

    def FineSelection(self, fine):
        # We could refine here, but for now we just take the top 100 liquid stocks
        return [x.Symbol for x in fine]

    def Rebalance(self):
        if self.IsWarmingUp or not self.spy_sma.IsReady: return
        
        spy_price = self.Securities[self.spy].Price
        sma_val = self.spy_sma.Current.Value
        
        if spy_price < sma_val:
            self.Log(f"[{self.Time}] MARKET BEARISH (SPY < SMA200). Moving to Cash.")
            self.Liquidate()
            self.SetHoldings(self.bil, 1.0)
            return

        # Market is bullish, rank by momentum
        momentum_scores = {}
        for symbol in self.ActiveSecurities.Keys:
            if symbol == self.spy or symbol == self.bil: continue
            
            hist = self.History(symbol, self.lookback + 1, Resolution.Daily)
            if not hist.empty:
                prices = hist['close'].values
                # 12-month Momentum (252 days)
                momentum_scores[symbol] = (prices[-1] / prices[0]) - 1
        
        if not momentum_scores: return
        
        # Sort by momentum score
        sorted_symbols = sorted(momentum_scores.items(), key=lambda x: x[1], reverse=True)
        top_symbols = [x[0] for x in sorted_symbols[:self.num_stocks]]
        
        # Liquidate symbols no longer in top N
        for symbol in self.Portfolio.Keys:
            if symbol not in top_symbols and self.Portfolio[symbol].Invested:
                self.Liquidate(symbol)
                
        # Equal weight Top N
        weight = 1.0 / self.num_stocks
        for symbol in top_symbols:
            self.SetHoldings(symbol, weight)

    def OnData(self, data):
        pass
