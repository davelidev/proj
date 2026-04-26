from datetime import datetime, timedelta
from AlgorithmImports import *


class VolatilityBreakoutV2(QCAlgorithm):

    def Initialize(self):
        self.lookback_period = int(self.GetParameter("lookback_period", 240))
        self.breakout_threshold_pct = float(self.GetParameter("breakout_threshold_pct", 0.98))
        self.volatility_low = float(self.GetParameter("volatility_low", 0.1))
        self.volatility_high = float(self.GetParameter("volatility_high", 0.15))
        self.rsi_overbought = float(self.GetParameter("rsi_overbought", 80))
        self.holding_pct = float(self.GetParameter("holding_pct", 1))
        self.stop_loss_pct = float(self.GetParameter("stop_loss_pct", 0.01))

    
        assert self.volatility_low < self.volatility_high 
    
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        
        self.sym = self.AddEquity("TQQQ", Resolution.Minute).Symbol
        
        # Custom indicator for intra-bar volatility
        self.volatility = AverageIntraBarVolatility(self.lookback_period)
        self.RegisterIndicator(self.sym, self.volatility, Resolution.Minute)
        
        # RSI for overbought exit
        self.rsi = self.RSI(self.sym, 10, MovingAverageType.Wilders, Resolution.Minute)
        
        # Indicator for the breakout high
        self.high = self.MAX(self.sym, self.lookback_period, Resolution.Minute)
        
        self.SetWarmUp(self.lookback_period, Resolution.Minute)
        
    def OnData(self, data):
        # Wait for indicators and trade only after the first hour
        if self.IsWarmingUp or self.Time.hour < 10 or not self.rsi.IsReady:
            return
    
        if not self.Portfolio.Invested:
            # Enter on low volatility when price is near a recent high
            is_low_volatility = self.volatility.Value < self.volatility_low
            is_near_breakout = self.Securities[self.sym].Price >= self.high.Current.Value * self.breakout_threshold_pct
            
            if is_low_volatility and is_near_breakout:
                self.SetHoldings(self.sym, self.holding_pct)
        else:
            is_high_volatility = self.volatility.Value > self.volatility_high
            is_overbought = self.rsi.Current.Value > self.rsi_overbought

            # Exit if volatility becomes too high or price is overextended
            if is_high_volatility or is_overbought:
                self.Liquidate(self.sym)
                self.Transactions.CancelOpenOrders(self.sym)

    def OnOrderEvent(self, orderEvent):
        # When a buy order is filled, place a corresponding stop loss order.
        if orderEvent.Status == OrderStatus.Filled and orderEvent.Direction == OrderDirection.Buy:
            stop_price = orderEvent.FillPrice * (1 - self.stop_loss_pct)
            self.StopMarketOrder(orderEvent.Symbol, -orderEvent.FillQuantity, stop_price)


class AverageIntraBarVolatility(PythonIndicator):
    def __init__(self, period):
        super().__init__()
        self.Name = "AverageIntraBarVolatility"
        self.sma = SimpleMovingAverage(period)
        self.WarmUpPeriod = period

    @property
    def Value(self):
        """Gets the current value of this indicator."""
        return self.Current.Value

    def Update(self, input: BaseData) -> bool:
        if not hasattr(input, "Open") or input.Open == 0: 
            return False
        
        rang = abs((input.Open - input.Close) / input.Open) * 100
        self.sma.Update(input.EndTime, rang)
        self.Current.Value = self.sma.Current.Value
        
        return self.sma.IsReady
