from datetime import datetime, timedelta
from AlgorithmImports import *

class RotationStrategyV14(QCAlgorithm):
    """
    Rotation V14: Volatility Targeting
    Adjusts the exposure to TQQQ based on the current volatility of QQQ.
    High volatility -> Lower TQQQ exposure, more Cash.
    Low volatility -> 100% TQQQ.
    """
    def Initialize(self):
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100_000)

        self.Schedule.On(
            self.DateRules.EveryDay("QQQ"),
            self.TimeRules.AfterMarketOpen("QQQ", 35),
            self.Rebalance,
        )

        self.sym_qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.sym_tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.sym_bil = self.AddEquity("BIL", Resolution.Daily).Symbol

        # 14-day ATR for volatility
        self.atr = self.ATR(self.sym_qqq, 14, MovingAverageType.Wilders, Resolution.Daily)
        self.sma200 = self.SMA(self.sym_qqq, 200, Resolution.Daily)

        self.SetWarmUp(200, Resolution.Daily)
        self.target_vol_pct = 1.8 # Target 1.8% daily volatility on QQQ equivalent

    def Rebalance(self):
        if self.IsWarmingUp or not self.atr.IsReady or not self.sma200.IsReady:
            return

        qqq_price = self.Securities[self.sym_qqq].Price
        if qqq_price == 0: return

        # Current QQQ daily volatility in %
        current_vol_pct = (self.atr.Current.Value / qqq_price) * 100
        
        if current_vol_pct == 0: return

        # We want our QQQ-equivalent exposure to have target_vol_pct volatility.
        # So exposure = target_vol_pct / current_vol_pct
        # Since TQQQ is 3x QQQ, TQQQ allocation = exposure / 3
        
        target_exposure = self.target_vol_pct / current_vol_pct
        
        # Max exposure is 100% TQQQ (which is 3x QQQ exposure)
        tqqq_weight = min(1.0, target_exposure / 3.0)
        
        # In a bear market (QQQ < 200 SMA), we halve the exposure to be safe
        if qqq_price < self.sma200.Current.Value:
            tqqq_weight *= 0.5
            
        cash_weight = 1.0 - tqqq_weight

        self.SetHoldings(self.sym_tqqq, tqqq_weight)
        self.SetHoldings(self.sym_bil, cash_weight)

        self.Debug(f"[Rebalance] Vol: {current_vol_pct:.2f}% -> TQQQ: {tqqq_weight*100:.1f}%")

    def OnData(self, data):
        pass
