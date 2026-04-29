from AlgorithmImports import *

class BaseSubAlgo:
    def __init__(self, algo, weight_pct):
        self.algo = algo
        self.weight_pct = weight_pct
        self.symbols = []

    def initialize(self):
        pass

    def on_data(self, data):
        pass

    def rebalance(self):
        pass

class VolatilityBreakoutSub(BaseSubAlgo):
    def __init__(self, algo, weight_pct):
        super().__init__(algo, weight_pct)
        self.lookback_period = 240
        self.breakout_threshold_pct = 0.98
        self.volatility_low = 0.1
        self.volatility_high = 0.15
        self.stop_loss_pct = 0.03

    def initialize(self):
        self.sym = self.algo.AddEquity("TQQQ", Resolution.Minute).Symbol
        self.symbols.append(self.sym)
        self.volatility = AverageIntraBarVolatility(self.lookback_period)
        self.algo.RegisterIndicator(self.sym, self.volatility, Resolution.Minute)
        self.high = self.algo.MAX(self.sym, self.lookback_period, Resolution.Minute)

    def on_data(self, data):
        if self.algo.IsWarmingUp or self.algo.Time.hour < 10:
            return
        
        # We use a custom SetHoldings logic in the main algo to manage the 1/5th slice
        # But for now, we just check signals
        invested = self.algo.Portfolio[self.sym].Invested
        if not invested:
            if self.volatility.Value < self.volatility_low and self.algo.Securities[self.sym].Price >= self.high.Current.Value * self.breakout_threshold_pct:
                self.algo.SetHoldings(self.sym, self.weight_pct)
                # Note: Stop loss logic handled via main algo's OnOrderEvent or manual check
        else:
            if self.volatility.Value > self.volatility_high:
                self.algo.Liquidate(self.sym)

    def check_stop_loss(self, orderEvent):
        if orderEvent.Status == OrderStatus.Filled and orderEvent.Direction == OrderDirection.Buy and orderEvent.Symbol == self.sym:
            stop_price = orderEvent.FillPrice * (1 - self.stop_loss_pct)
            self.algo.StopMarketOrder(self.sym, -orderEvent.FillQuantity, stop_price)

class TechDipBuySub(BaseSubAlgo):
    def __init__(self, algo, weight_pct):
        super().__init__(algo, weight_pct)
        self.stocks = []

    def initialize(self):
        # This one uses a universe, which is tricky for sub-algos.
        # We will hardcode the top 5 tech for the composite to avoid universe collisions.
        self.tickers = ["AAPL", "MSFT", "NVDA", "AVGO", "ORCL"]
        for t in self.tickers:
            s = self.algo.AddEquity(t, Resolution.Daily).Symbol
            self.symbols.append(s)
            sec = self.algo.Securities[s]
            sec.rsi = self.algo.RSI(s, 2)
            sec.max = self.algo.MAX(s, 252)
            sec.sma50 = self.algo.SMA(s, 50)

    def rebalance(self):
        # Weekly logic normally, but we can call it daily
        for s in self.symbols:
            sec = self.algo.Securities[s]
            if not (sec.rsi.IsReady and sec.max.IsReady and sec.sma50.IsReady): continue
            
            if not sec.Invested:
                if sec.rsi.Current.Value < 30 and sec.Price > sec.sma50.Current.Value:
                    self.algo.SetHoldings(s, self.weight_pct / 5)
            else:
                if sec.Price <= sec.Holdings.AveragePrice * 0.85 or sec.Price >= sec.max.Current.Value:
                    self.algo.Liquidate(s)

class LeveragedRebalanceSub(BaseSubAlgo):
    def __init__(self, algo, weight_pct):
        super().__init__(algo, weight_pct)
        # 20% each of TQQQ, SOXL, TECL within the 20% slice = 0.066 each of total
        self.weights = {"TQQQ": 0.2, "SOXL": 0.2, "TECL": 0.2} 

    def initialize(self):
        for t in self.weights:
            s = self.algo.AddEquity(t, Resolution.Daily).Symbol
            self.symbols.append(s)

    def rebalance_yearly(self):
        for s, w in self.weights.items():
            self.algo.SetHoldings(s, self.weight_pct * w * 2.5) # Rebalance to target weights

class RSIDipChampionSub(BaseSubAlgo):
    def __init__(self, algo, weight_pct):
        super().__init__(algo, weight_pct)
        self.tickers = ["TQQQ", "SOXL", "TECL"]
        self.is_long = False

    def initialize(self):
        self.algo.AddEquity("QQQ", Resolution.Daily)
        self.rsi2 = self.algo.RSI("QQQ", 2, MovingAverageType.Wilders, Resolution.Daily)
        for t in self.tickers:
            self.symbols.append(self.algo.AddEquity(t, Resolution.Daily).Symbol)

    def rebalance(self):
        if not self.rsi2.IsReady: return
        
        should_be_long = self.rsi2.Current.Value < 25
        if should_be_long != self.is_long:
            self.is_long = should_be_long
            if not self.is_long:
                for s in self.symbols: self.algo.Liquidate(s)
            else:
                for s in self.symbols: self.algo.SetHoldings(s, self.weight_pct / 3)

class TQQQDynamicSub(BaseSubAlgo):
    def __init__(self, algo, weight_pct):
        super().__init__(algo, weight_pct)

    def initialize(self):
        self.sym = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.symbols.append(self.sym)
        self.rsi2 = self.algo.RSI(self.sym, 2, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi10 = self.algo.RSI(self.sym, 10, MovingAverageType.Wilders, Resolution.Daily)
        self.sma200 = self.algo.SMA(self.sym, 200, Resolution.Daily)

    def rebalance(self):
        if not (self.rsi2.IsReady and self.sma200.IsReady): return
        
        price = self.algo.Securities[self.sym].Price
        sma = self.sma200.Current.Value
        r2 = self.rsi2.Current.Value
        r10 = self.rsi10.Current.Value

        if price > sma:
            if r10 > 80:
                self.algo.SetHoldings(self.sym, self.weight_pct * 0.2)
            elif r2 < 30:
                self.algo.SetHoldings(self.sym, self.weight_pct * 1.0)
            elif not self.algo.Portfolio[self.sym].Invested:
                self.algo.SetHoldings(self.sym, self.weight_pct * 0.5)
        else:
            self.algo.Liquidate(self.sym)

class AverageIntraBarVolatility(PythonIndicator):
    def __init__(self, period):
        super().__init__()
        self.Name = "AverageIntraBarVolatility"
        self.sma = SimpleMovingAverage(period)
        self.WarmUpPeriod = period

    @property
    def Value(self):
        return self.Current.Value

    def Update(self, input: BaseData) -> bool:
        if not hasattr(input, "Open") or input.Open == 0: return False
        rang = abs((input.Open - input.Close) / input.Open) * 100
        self.sma.Update(input.EndTime, rang)
        self.Current.Value = self.sma.Current.Value
        return self.sma.IsReady
