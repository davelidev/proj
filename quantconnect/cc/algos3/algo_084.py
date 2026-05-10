from QuantConnect import *
from QuantConnect.DataSource import *
from QuantConnect.Algorithm import QCAlgorithm
from QuantConnect.Data.UniverseSelection import *
from datetime import timedelta
import numpy as np

class Algo084(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.Resolution = Resolution.Daily
        self.UniverseSettings.Resolution = Resolution.Daily
        
        self.AddUniverse(self.CoarseSelectionFunction)
        
        # Warm up period to ensure we have enough history (20 days for MA + 21 for vol)
        self.SetWarmUp(timedelta(50))
        
        # Schedule rebalance daily at market close
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.AfterMarketOpen("SPY", 0))
        
        self.symbols = []
        self.selected = []

    def CoarseSelectionFunction(self, coarse):
        # Choose the top 500 liquid stocks based on dollar volume
        sorted_by_volume = sorted(coarse, key=lambda x: x.DollarVolume, reverse=True)
        top500 = [x.Symbol for x in sorted_by_volume[:500] if x.HasFundamentalData and x.Price > 5]
        return top500

    def OnData(self, data):
        if self.IsWarmingUp:
            return
        
        # Get latest history for volatility calculation
        tickers = [sym.Value for sym in self.symbols if sym in data.Bars]
        if len(tickers) == 0:
            return
        
        # Request 21 days of history (to compute standard deviation of last 21 daily returns)
        history = self.History(self.symbols, 21, Resolution.Daily)
        if history.empty:
            return
        
        # Compute daily volatility for each symbol (std of daily returns over 21 days)
        vol_data = {}
        for sym in self.symbols:
            if sym in data.Bars and sym in history.index.levels[0]:
                price_series = history.loc[sym]['close']
                if len(price_series) < 21:
                    continue
                returns = price_series.pct_change().dropna()
                if len(returns) >= 20:
                    current_vol = np.std(returns[-20:])  # current vol (last 20 days)
                    # Compute 20-day moving average of daily vol (using earlier 20 vols)
                    # We need a rolling vol series; compute vol for each rolling window of 20 returns
                    vols = []
                    for i in range(1, len(returns) - 19):
                        window = returns.iloc[i:i+20]
                        vols.append(np.std(window))
                    if len(vols) >= 20:
                        ma_vol = np.mean(vols[-20:])  # 20-day MA of vol
                        if current_vol < ma_vol:
                            vol_data[sym] = current_vol
        
        # Rebalance: hold only those with vol < 20d MA vol
        selected = list(vol_data.keys())
        self.selected = selected
        
        # If no selection, invest in cash
        if len(selected) == 0:
            self.SetHoldings([PortfolioTarget("SPY", 0)])  # liquidate all
            return
        
        # Equal weight, sum <= 1.0
        weight = 1.0 / len(selected)
        
        # Set holdings
        for sym in self.symbols:
            if sym in selected:
                self.SetHoldings(sym, weight)
            else:
                self.Liquidate(sym)

    def OnSecuritiesChanged(self, changes):
        # Update the universe symbols list
        for added in changes.AddedSecurities:
            self.symbols.append(added.Symbol)
        for removed in changes.RemovedSecurities:
            self.symbols.remove(removed.Symbol)