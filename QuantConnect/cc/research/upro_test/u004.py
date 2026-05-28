from AlgorithmImports import *
class U004(QCAlgorithm):
    """QQQ expanding range + ADX(10)>25 → UPRO with 3×ATR trailing stop. UPRO generalization of ensemble/004."""
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.upro      = self.AddEquity("UPRO", Resolution.Daily).Symbol
        self.q         = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.adx       = self.ADX(self.q, 10, Resolution.Daily)
        self.sma200    = self.SMA(self.q, 200, Resolution.Daily)
        self.atr       = self.ATR(self.upro, 14, MovingAverageType.Wilders, Resolution.Daily)
        self.max20     = self.MAX(self.upro, 20, Resolution.Daily)
        self.trail     = 0
        self.SetWarmUp(210, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),
                         self.TimeRules.AfterMarketOpen(self.q, 30), self.R)
    def R(self):
        if self.IsWarmingUp or not (self.adx.IsReady and self.sma200.IsReady and self.max20.IsReady): return
        price = self.Securities[self.upro].Price
        qprice = self.Securities[self.q].Price
        hist  = self.History(self.q, 3, Resolution.Daily)
        if len(hist) < 3: return
        r2 = hist.iloc[-3]['high'] - hist.iloc[-3]['low']
        r1 = hist.iloc[-2]['high'] - hist.iloc[-2]['low']
        invested = self.Portfolio[self.upro].Invested
        if not invested:
            if qprice > self.sma200.Current.Value and r1 > r2 and self.adx.Current.Value > 25:
                self.SetHoldings(self.upro, 1.0)
                self.trail = price - 3.0 * self.atr.Current.Value
        else:
            new_stop = price - 3.0 * self.atr.Current.Value
            if new_stop > self.trail: self.trail = new_stop
            if price >= self.max20.Current.Value or price < self.trail or qprice < self.sma200.Current.Value:
                self.Liquidate(self.upro)
                self.trail = 0
    def OnData(self, d): pass
