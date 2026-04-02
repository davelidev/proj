from datetime import datetime, timedelta
from AlgorithmImports import *

class PairSwitchingLeveraged(QCAlgorithm):
    def Initialize(self):
        # 12 year backtest
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100000)

        # Pair: Large-cap Tech vs Small-cap Tech
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.tna = self.AddEquity("TNA", Resolution.Daily).Symbol
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        
        self.sma_spy = self.SMA(self.spy, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.MonthStart("SPY"), 
                         self.TimeRules.AfterMarketOpen("SPY", 35), 
                         self.Rebalance)
        
        self.SetWarmUp(200)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma_spy.IsReady:
            return

        spy_price = self.Securities[self.spy].Price
        
        if spy_price > self.sma_spy.Current.Value:
            # Bull Market: Choose the leader between TQQQ and TNA
            # Using 20-day momentum
            hist_tqqq = self.History(self.tqqq, 20, Resolution.Daily)
            hist_tna = self.History(self.tna, 20, Resolution.Daily)
            
            if hist_tqqq.empty or hist_tna.empty: return
            
            mom_tqqq = (hist_tqqq['close'].iloc[-1] / hist_tqqq['close'].iloc[0]) - 1
            mom_tna = (hist_tna['close'].iloc[-1] / hist_tna['close'].iloc[0]) - 1
            
            if mom_tqqq > mom_tna:
                self.Log(f"Bull: TQQQ leader ({mom_tqqq:.2%}) > TNA ({mom_tna:.2%})")
                self.SetHoldings(self.tqqq, 1.0, liquidateExistingHoldings=True)
            else:
                self.Log(f"Bull: TNA leader ({mom_tna:.2%}) > TQQQ ({mom_tqqq:.2%})")
                self.SetHoldings(self.tna, 1.0, liquidateExistingHoldings=True)
        else:
            # Bear Market
            self.Log("Bear Market: Liquidating to cash.")
            self.Liquidate()
