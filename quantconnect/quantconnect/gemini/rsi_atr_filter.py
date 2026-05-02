from AlgorithmImports import *

class RSIATRFilter(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.rsi = self.RSI(self.tqqq, 2, MovingAverageType.Wilders, Resolution.Daily)
        self.atr = self.ATR(self.tqqq, 14, MovingAverageType.Wilders, Resolution.Daily)
        
        self.SetWarmUp(20)

    def OnData(self, data):
        if self.IsWarmingUp or not (self.rsi.IsReady and self.atr.IsReady): return
        
        price = self.Securities[self.tqqq].Price
        rsi_val = self.rsi.Current.Value
        atr_val = self.atr.Current.Value
        
        # Volatility Filter: ATR as % of Price
        vol_pct = atr_val / price if price > 0 else 1.0
        
        if not self.Portfolio[self.tqqq].Invested:
            # Entry: Oversold AND low volatility (orderly pullback)
            if rsi_val < 20 and vol_pct < 0.05:
                self.Log(f"[{self.Time}] ORDERLY DIP BUY. RSI: {rsi_val:.2f} | Vol: {vol_pct:.1%}. Entering.")
                self.SetHoldings(self.tqqq, 1.0)
        else:
            # Exit: Recovery OR Volatility Spike (Panic)
            if rsi_val > 80 or vol_pct > 0.08:
                self.Log(f"[{self.Time}] EXIT. RSI: {rsi_val:.2f} | Vol: {vol_pct:.1%}. Exiting.")
                self.Liquidate(self.tqqq)
