from datetime import datetime, timedelta
from AlgorithmImports import *

class CommodityEquityMomentum(QCAlgorithm):
    def Initialize(self):
        # 12 year backtest
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100000)

        # Equity (TQQQ) and Commodities (UCO for Oil, GLD for Gold, or GUSH for Oil & Gas LETF)
        # Note: GUSH is 2x/3x leveraged oil & gas.
        self.offensive = ["TQQQ", "GUSH", "GLD"]
        self.defensive = ["IEF"]
        self.spy = "SPY"
        
        self.symbols = {}
        for ticker in self.offensive + self.defensive + [self.spy]:
            self.symbols[ticker] = self.AddEquity(ticker, Resolution.Daily).Symbol

        self.sma_spy = self.SMA(self.symbols[self.spy], 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.MonthStart(self.spy), 
                         self.TimeRules.AfterMarketOpen(self.spy, 35), 
                         self.Rebalance)
        
        self.SetWarmUp(253)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma_spy.IsReady:
            return

        # Simple Momentum (12-month)
        # GUSH inception is 2015. Handle gracefully.
        momentum = {}
        for ticker in self.offensive:
            symbol = self.symbols[ticker]
            if not self.Securities[symbol].HasData: continue
            
            history = self.History(symbol, 252, Resolution.Daily)
            if history.empty or len(history) < 252: continue
            
            mom = (history['close'].iloc[-1] / history['close'].iloc[0]) - 1
            momentum[ticker] = mom

        if not momentum: return
        
        best_ticker = max(momentum, key=momentum.get)
        
        spy_bull = self.Securities[self.symbols[self.spy]].Price > self.sma_spy.Current.Value
        
        if momentum[best_ticker] > 0:
            if best_ticker == "TQQQ":
                # Only hold TQQQ if SPY is in a bull trend to manage drawdown
                if spy_bull:
                    self.Log(f"Risk-On: TQQQ momentum {momentum['TQQQ']:.2%}")
                    self.SetHoldings(self.symbols["TQQQ"], 1.0, liquidateExistingHoldings=True)
                else:
                    self.Log("TQQQ has momentum but SPY < 200 SMA. Moving to Defensive.")
                    self.SetHoldings(self.symbols["IEF"], 1.0, liquidateExistingHoldings=True)
            else:
                # Commodities (GLD, GUSH) often thrive when equities fail.
                self.Log(f"Risk-On: {best_ticker} momentum {momentum[best_ticker]:.2%}")
                self.SetHoldings(self.symbols[best_ticker], 1.0, liquidateExistingHoldings=True)
        else:
            self.Log("No positive momentum. Moving to Defensive.")
            self.SetHoldings(self.symbols["IEF"], 1.0, liquidateExistingHoldings=True)
