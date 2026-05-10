from collections import deque
import numpy as np
from QuantConnect import *
from QuantConnect.Algorithm import *
from QuantConnect.Data.UniverseSelection import *
from QuantConnect.Indicators import *

class Algo042(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.AddEquity("TQQQ", Resolution.Daily)
        self.AddUniverse(self.CoarseSelectionFunction)
        self.basket = {}
        self.volume_windows = {}
        self.return_windows = {}
        self.corr_indicators = {}
        self.dispersion_buffer = deque(maxlen=252)
        self.vol_indicator = StandardDeviation(20)
        self.vol_history = deque(maxlen=252)
        self.monthly_returns = self.ComputeMonthlyReturnTable()
        self.seasonality_factor = {}

    def CoarseSelectionFunction(self, coarse):
        # Filter for stocks with fundamental data and sort by market cap
        sorted_by_mc = sorted([c for c in coarse if c.HasFundamentalData],
                              key=lambda x: x.DollarVolume, reverse=True)
        top10 = [c.Symbol for c in sorted_by_mc[:10]]
        return top10

    def OnSecuritiesChanged(self, changes):
        for symbol in changes.RemovedSecurities:
            if symbol in self.basket:
                del self.basket[symbol]
            if symbol in self.volume_windows:
                del self.volume_windows[symbol]
            if symbol in self.return_windows:
                del self.return_windows[symbol]
            if symbol in self.corr_indicators:
                del self.corr_indicators[symbol]
        for symbol in changes.AddedSecurities:
            self.basket[symbol] = symbol
            self.volume_windows[symbol] = deque(maxlen=200)
            self.return_windows[symbol] = deque(maxlen=30)
            self.corr_indicators[symbol] = RollingCorrelation(30)
            # Populate initial history
            history = self.History(symbol, 200, Resolution.Daily)
            if not history.empty:
                for index, row in history.iterrows():
                    self.volume_windows[symbol].append(row['volume'])
                    self.return_windows[symbol].append(row['close'])  # will use for return later

    def OnData(self, data):
        # Update all windows and indicators for basket symbols
        tqqq = self.Securities["TQQQ"]
        if not data.ContainsKey("TQQQ"):
            return
        tqqq_bar = data["TQQQ"]
        tqqq_close = tqqq_bar.Close
        # Update TQQQ volatility
        tqqq_return = tqqq_close / tqqq.Open - 1 if tqqq.Open != 0 else 0
        self.vol_indicator.Update(tqqq.EndTime, tqqq_return)
        if self.vol_indicator.IsReady:
            self.vol_history.append(self.vol_indicator.Current.Value)

        # Prepare to compute dispersion later
        returns_10d = {}
        for symbol in list(self.basket.keys()):
            if symbol not in data or not data.ContainsKey(symbol):
                continue
            bar = data[symbol]
            # Update volume window
            self.volume_windows[symbol].append(bar.Volume)
            # Update return window (store closes for return calculation)
            self.return_windows[symbol].append(bar.Close)
            # Update correlation indicator with TQQQ
            self.corr_indicators[symbol].Update(bar.EndTime, bar.Close, tqqq_close)
            # Compute 10-day return for dispersion
            if len(self.return_windows[symbol]) >= 10:
                ret_10 = bar.Close / list(self.return_windows[symbol])[-10] - 1
                returns_10d[symbol] = ret_10

        # Compute dispersion (cross-sectional std of 10-day returns)
        if len(returns_10d) > 1:
            ret_values = list(returns_10d.values())
            current_disp = np.std(ret_values)
            self.dispersion_buffer.append(current_disp)

        # Compute signals and weights
        scores = {}
        for symbol in list(self.basket.keys()):
            if symbol not in data or not data.ContainsKey(symbol):
                continue
            if len(self.volume_windows[symbol]) < 200:
                continue
            # Volume percentile
            volumes = list(self.volume_windows[symbol])
            p10 = np.percentile(volumes, 10)
            p90 = np.percentile(volumes, 90)
            current_vol = data[symbol].Volume
            if current_vol > p90:
                volume_score = 1.0
            elif current_vol < p10:
                volume_score = -1.0
            else:
                volume_score = 0.0

            # Only proceed if volume is extreme
            if volume_score == 0:
                continue

            # Correlation factor
            corr_indicator = self.corr_indicators[symbol]
            if corr_indicator.IsReady:
                corr = corr_indicator.Current.Value
                corr_factor = 0.2 * corr  # range -0.2 to +0.2
            else:
                corr_factor = 0

            # Dispersion factor
            if len(self.dispersion_buffer) > 20:
                disp_array = np.array(list(self.dispersion_buffer))
                disp_mean = np.mean(disp_array)
                disp_std = np.std(disp_array)
                if disp_std > 0:
                    disp_z = (current_disp - disp_mean) / disp_std
                    dispersion_factor = 0.1 * np.clip(disp_z, -1, 1)  # range -0.1 to +0.1
                else:
                    dispersion_factor = 0
            else:
                dispersion_factor = 0

            # Seasonality factor
            month = self.Time.month
            if month in self.monthly_returns:
                avg_month_ret = self.monthly_returns[month]
                seasonality_factor = 0.2 * np.clip(avg_month_ret * 10, -1, 1)
            else:
                seasonality_factor = 0

            # Regime factor (volatility regime)
            if len(self.vol_history) > 50:
                vol_array = np.array(list(self.vol_history))
                vol_pct = np.percentile(vol_array, 90)
                current_vol = self.vol_indicator.Current.Value
                if current_vol > vol_pct:
                    regime_factor = -0.2  # high vol -> reduce
                else:
                    vol_pct_low = np.percentile(vol_array, 10)
                    if current_vol < vol_pct_low:
                        regime_factor = 0.2  # low vol -> increase
                    else:
                        regime_factor = 0
            else:
                regime_factor = 0

            # Composite signal
            raw = volume_score * (1 + corr_factor + dispersion_factor + seasonality_factor + regime_factor)
            scores[symbol] = max(0, raw)  # long only

        # Normalize weights to sum <= 1 (cash) and apply max position size 0.2
        if scores:
            total_score = sum(scores.values())
            if total_score > 0:
                for sym in scores:
                    scores[sym] /= total_score
                # Cap individual weight at 0.2
                for sym in list(scores.keys()):
                    if scores[sym] > 0.2:
                        scores[sym] = 0.2
                # Renormalize (after capping)
                total_capped = sum(scores.values())
                if total_capped > 1:
                    for sym in scores:
                        scores[sym] /= total_capped

        # Execute orders
        for symbol in self.basket:
            if symbol in scores:
                self.SetHoldings(symbol, scores[symbol])
            else:
                self.SetHoldings(symbol, 0)

        # Also ensure TQQQ is not held (unless we want it? Not in basket)
        self.SetHoldings("TQQQ", 0)

    def ComputeMonthlyReturnTable(self):
        # Compute average monthly returns for TQQQ from history
        history = self.History("TQQQ", 10*365, Resolution.Daily)  # 10 years
        if history.empty:
            # Fallback to a simple table
            return {1: 0.02, 2: 0.01, 3: 0.02, 4: 0.0, 5: -0.01, 6: -0.01,
                    7: 0.0, 8: -0.02, 9: -0.01, 10: 0.01, 11: 0.02, 12: 0.02}
        # Resample to monthly returns
        monthly = history['close'].resample('M').last()
        monthly_returns = monthly.pct_change().dropna()
        monthly_avg = monthly_returns.groupby(monthly_returns.index.month).mean()
        return monthly_avg.to_dict()
