from AlgorithmImports import *

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

class QuantumOptimizedPrism(QCAlgorithm):

    def Initialize(self):
        self.lookback_period = int(self.GetParameter("lookback_period", 240))
        self.breakout_threshold_pct = float(self.GetParameter("breakout_threshold_pct", 0.98))
        self.volatility_low = float(self.GetParameter("volatility_low", 0.1))
        self.volatility_high = float(self.GetParameter("volatility_high", 0.15))
        self.holding_pct = float(self.GetParameter("holding_pct", 1))
        self.stop_loss_pct = float(self.GetParameter("stop_loss_pct", 0.01))

    
        assert self.volatility_low < self.volatility_high 
    
        self.SetStartDate(2020, 1, 1)
        self.SetCash(2000)
        
        self.sym = self.AddEquity("TQQQ", Resolution.Minute).Symbol
        
        self.volatility = AverageIntraBarVolatility(self.lookback_period)
        self.RegisterIndicator(self.sym, self.volatility, Resolution.Minute)
        
        self.high = self.MAX(self.sym, self.lookback_period, Resolution.Minute)
        
        self.stop_loss_ticket = None
        
        self.SetWarmUp(self.lookback_period, Resolution.Minute)
        
    def OnData(self, data):
        if self.Time.hour < 10: return
        if not self.volatility.IsReady or not self.high.IsReady or self.IsWarmingUp: 
            return
    
        current_price = self.Securities[self.sym].Price
        
        is_low_volatility = self.volatility.Current.Value < self.volatility_low 
        is_near_breakout = self.high.Current.Value * self.breakout_threshold_pct <= current_price
        
        if is_low_volatility and is_near_breakout and not self.Portfolio.Invested:
            self.SetHoldings(self.sym, self.holding_pct)
        
        is_high_volatility = self.volatility.Current.Value > self.volatility_high
        if is_high_volatility:
            self.Liquidate(self.sym)

    def OnOrderEvent(self, orderEvent):
        # Reset the stop loss ticket if the order is filled or canceled.
        if self.stop_loss_ticket and self.stop_loss_ticket.OrderId == orderEvent.OrderId:
            if orderEvent.Status == OrderStatus.Filled or orderEvent.Status == OrderStatus.Canceled:
                self.stop_loss_ticket = None

        # Place a stop loss order after a buy order is filled.
        if self.Portfolio.Invested and orderEvent.Status == OrderStatus.Filled and orderEvent.Direction == OrderDirection.Buy:
            stop_price = self.Portfolio[orderEvent.Symbol].AveragePrice * (1 - self.stop_loss_pct)
            quantity = -self.Portfolio[orderEvent.Symbol].Quantity
            
            if self.stop_loss_ticket:
                update_fields = UpdateOrderFields()
                update_fields.StopPrice = stop_price
                update_fields.Quantity = quantity
                self.stop_loss_ticket.Update(update_fields)
            else:
                self.stop_loss_ticket = self.StopMarketOrder(orderEvent.Symbol, quantity, stop_price)
