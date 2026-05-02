from AlgorithmImports import *

class UltimateApexEnsemble(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.assets = ["TQQQ", "SOXL"]
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.symbols = {}
        self.smas = {}
        for ticker in self.assets:
            symbol = self.AddEquity(ticker, Resolution.Daily).Symbol
            self.symbols[ticker] = symbol
            self.smas[symbol] = self.SMA(symbol, 200, Resolution.Daily)
            
        self.sma_qqq = self.SMA(self.qqq, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay("QQQ"), 
                         self.TimeRules.AfterMarketOpen("QQQ", 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma_qqq.IsReady: return
        
        price_q = float(self.Securities[self.qqq].Price)
        sma_q = float(self.sma_qqq.Current.Value)
        
        target_weights = {}
        total_w = 0
        
        # 1. Broad Trend Filter
        if price_q > sma_q:
            # 2. Individual Asset Stretch Filter
            for ticker, symbol in self.symbols.items():
                if not self.smas[symbol].IsReady: continue
                
                price = float(self.Securities[symbol].Price)
                sma_val = float(self.smas[symbol].Current.Value)
                stretch = (price - sma_val) / sma_val if sma_val > 0 else 0
                
                # Exit if > 15% above SMA (Overextended)
                if stretch < 0.15:
                    target_weights[symbol] = 0.5
                    total_w += 0.5
                else:
                    target_weights[symbol] = 0
        
        # 3. Defensive Allocation
        target_weights[self.bil] = 1.0 - total_w
        
        # 4. Execute
        for symbol, weight in target_weights.items():
            self.SetHoldings(symbol, weight)
            
        # Liquidate removed
        for symbol in self.Portfolio.Keys:
            if symbol not in target_weights and symbol != self.qqq:
                self.Liquidate(symbol)

    def OnData(self, data):
        pass
