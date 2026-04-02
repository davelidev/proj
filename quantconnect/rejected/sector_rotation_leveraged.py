from datetime import datetime, timedelta
from AlgorithmImports import *

class SectorRotationLeveraged(QCAlgorithm):
    def Initialize(self):
        # 12 year backtest
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100000)

        # High-beta sector LETFs
        # SOXL (Semi), TECL (Tech), FAS (Financials), RETL (Retail), UPRO (S&P 500)
        self.offensive = ["SOXL", "TECL", "FAS", "TQQQ", "UPRO"]
        self.defensive = ["IEF", "TLT"]
        self.spy = "SPY"
        
        self.symbols = {}
        for ticker in self.offensive + self.defensive + [self.spy]:
            self.symbols[ticker] = self.AddEquity(ticker, Resolution.Daily).Symbol

        # SMA for regime filter
        self.sma_spy = self.SMA(self.symbols[self.spy], 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.MonthStart(self.spy), 
                         self.TimeRules.AfterMarketOpen(self.spy, 35), 
                         self.Rebalance)
        
        self.SetWarmUp(200)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma_spy.IsReady:
            return

        spy_price = self.Securities[self.symbols[self.spy]].Price
        
        if spy_price > self.sma_spy.Current.Value:
            # Risk-On: Pick the best performing sector over the last 3 months
            # Using 3-month momentum (63 trading days)
            momentum = {}
            for ticker in self.offensive:
                symbol = self.symbols[ticker]
                history = self.History(symbol, 63, Resolution.Daily)
                if history.empty or len(history) < 63:
                    continue
                
                ret = (history['close'].iloc[-1] / history['close'].iloc[0]) - 1
                momentum[ticker] = ret
            
            if momentum:
                best_ticker = max(momentum, key=momentum.get)
                self.Log(f"RISK-ON: {best_ticker} (3m Momentum: {momentum[best_ticker]:.2%})")
                self.Liquidate()
                self.SetHoldings(self.symbols[best_ticker], 1.0)
        else:
            # Risk-Off
            self.Log("RISK-OFF: Switching to defensive")
            self.Liquidate()
            self.SetHoldings(self.symbols["IEF"], 1.0)
