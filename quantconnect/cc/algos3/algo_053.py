from QuantConnect import *
from QuantConnect.Algorithm import *
from QuantConnect.Indicators import *
from QuantConnect.Data.Market import TradeBar
from System.Collections.Generic import List

class Algo053(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        # Hardcoded TQQQ (required by rules)
        self.AddEquity("TQQQ", Resolution.Daily)
        
        # Universe selection: top 10 by market cap (all sectors)
        self.AddUniverse(self.CoarseFilter)
        
        # Data structures
        self.basket = {}               # Symbol -> (SMA, ATR) indicators
        self.entry_signal = {}         # Symbol -> bool (active entry signal)
        self.position_state = {}       # Symbol -> bool (currently holding)
        self.warmup_period = 21        # Number of bars for indicator warmup
        
        # Warm up period
        self.SetWarmUp(self.warmup_period)
        
        # Schedule rebalance at market close (after daily bar)
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.AfterMarketOpen("TQQQ", 5), self.Rebalance)
        
    def CoarseFilter(self, coarse):
        # Filter for liquid stocks with fundamentals
        filtered = [c for c in coarse if c.HasFundamentalData and c.Price > 5 and c.Volume > 1e6]
        # Sort by market cap descending, take top 10
        sorted_coarse = sorted(filtered, key=lambda c: c.MarketCap, reverse=True)
        top10 = sorted_coarse[:10]
        return [c.Symbol for c in top10]
    
    def OnSecuritiesChanged(self, changes):
        # Handle additions and removals from universe
        for added in changes.AddedSecurities:
            symbol = added.Symbol
            if symbol not in self.basket:
                # Create indicators
                sma = self.SMA(symbol, 20, Resolution.Daily)
                atr = self.ATR(symbol, 14, MovingAverageType.Simple, Resolution.Daily)
                self.basket[symbol] = (sma, atr)
                self.entry_signal[symbol] = False
                self.position_state[symbol] = False
                
        for removed in changes.RemovedSecurities:
            symbol = removed.Symbol
            if symbol in self.basket:
                # Clean up
                self.DeregisterIndicator(self.basket[symbol][0])
                self.DeregisterIndicator(self.basket[symbol][1])
                del self.basket[symbol]
                del self.entry_signal[symbol]
                if symbol in self.position_state:
                    del self.position_state[symbol]
    
    def OnData(self, data):
        # Update indicators for all symbols in basket
        for symbol, (sma, atr) in self.basket.items():
            if data.Bars.ContainsKey(symbol):
                bar = data.Bars[symbol]
                # The indicators are automatically updated via consolidator.
                # No manual update needed since we registered them with the security.
                pass
            elif data.QuoteBars.ContainsKey(symbol):
                # If no trade bar, use quote bar (rare for daily)
                pass
                
        # After warmup, evaluate entry and exit signals
        if self.IsWarmingUp:
            return
            
        self.EvaluateSignals()
            
    def EvaluateSignals(self):
        # Check entry signals for new positions
        for symbol, (sma, atr) in self.basket.items():
            if not self.position_state.get(symbol, False) and sma.IsReady and atr.IsReady:
                price = self.Securities[symbol].Price
                if price > sma.Current.Value + 2.0 * atr.Current.Value:
                    self.entry_signal[symbol] = True
        
        # Check exit signals for existing positions (trailing stop based on SMA - 2*ATR)
        for symbol, (sma, atr) in self.basket.items():
            if self.position_state.get(symbol, False):
                price = self.Securities[symbol].Price
                if price < sma.Current.Value - 2.0 * atr.Current.Value:
                    self.entry_signal[symbol] = False
                    self.position_state[symbol] = False
                    self.Log(f"Exit {symbol} at {price}")
    
    def Rebalance(self):
        # Build target weights based on current entry signals
        # Only symbols that are in the basket and have active entry signal get equal weight
        active_symbols = [s for s, signal in self.entry_signal.items() if signal and s in self.basket]
        if len(active_symbols) == 0:
            # Liquidate all positions
            self.SetHoldings({})
            return
        
        target_weight = 1.0 / len(active_symbols)
        targets = {s: target_weight for s in active_symbols}
        
        # Also ensure we exit positions that are no longer in universe or have no signal
        for symbol in self.position_state:
            if symbol not in targets and self.Portfolio[symbol].Invested:
                targets[symbol] = 0
        
        # Execute
        self.SetHoldings(targets)
        
        # Update position state
        for symbol in targets:
            if targets[symbol] > 0 and not self.position_state.get(symbol, False):
                self.position_state[symbol] = True
                self.Log(f"Enter {symbol} at {self.Securities[symbol].Price}")
