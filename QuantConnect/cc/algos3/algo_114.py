import numpy as np
import scipy.optimize
from QuantConnect import Resolution
from QuantConnect.Algorithm import QCAlgorithm

class Algo114(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.symbol = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        
        # GARCH estimation parameters
        self.estimation_window = 252      # number of days for GARCH MLE
        self.vol_of_vol_window = 60       # rolling window for vol-of-vol
        self.target_vol = 0.2             # annual target volatility
        
        # Warm-up to have enough historical data
        self.SetWarmup(self.estimation_window + 1)
        
        self.sigma_history = []           # stores recent conditional volatilities
        
    def OnData(self, data):
        if self.IsWarmingUp:
            return
        if not data.ContainsKey(self.symbol) or data[self.symbol] is None:
            return
        
        # Fetch history for estimation window + 1 (to get one extra for returns)
        history = self.History([self.symbol], self.estimation_window + 1, Resolution.Daily)
        if history.empty or len(history) < self.estimation_window + 1:
            return
        
        prices = history.loc[self.symbol].close.values
        returns = np.diff(np.log(prices))      # log returns of length estimation_window
        
        # Estimate GARCH(1,1) and get the conditional volatility series
        sigma_series, last_sigma = self.estimate_garch(returns)
        
        if sigma_series is None:
            # Fallback: simple rolling volatility
            last_sigma = np.std(returns[-21:])
            # Clear history to avoid stale data
            self.sigma_history = []
        else:
            # Update sigma_history with the latest vol_of_vol_window values
            self.sigma_history = list(sigma_series[-self.vol_of_vol_window:])
        
        # Compute vol-of-vol (standard deviation of recent conditional volatilities)
        if len(self.sigma_history) >= 2:
            vol_of_vol = np.std(self.sigma_history)
        else:
            vol_of_vol = 0.0
        
        # Calculate target daily volatility
        daily_target_vol = self.target_vol / np.sqrt(252)
        
        # Weight: inversely proportional to (sigma_t * (1 + vol_of_vol))
        # This scales down exposure when vol is high or vol-of-vol is high.
        if last_sigma > 0:
            weight = daily_target_vol / (last_sigma * (1.0 + vol_of_vol))
        else:
            weight = 1.0
        
        # Enforce no leverage (weight <= 1.0)
        weight = min(weight, 1.0)
        
        # Set holdings
        self.SetHoldings(self.symbol, weight)
    
    def estimate_garch(self, returns):
        """
        Fit GARCH(1,1) via MLE and return (sigma_series, last_sigma).
        sigma_series: array of conditional volatilities for each day in returns.
        last_sigma: conditional volatility for the most recent date.
        Returns (None, None) on failure.
        """
        def neg_log_likelihood(params, r):
            omega, alpha, beta = params
            if omega <= 0 or alpha < 0 or beta < 0 or alpha + beta >= 1:
                return 1e10
            n = len(r)
            sigma2 = np.var(r)  # initial variance
            logL = 0.0
            for t in range(n):
                # Apply GARCH recursion
                sigma2 = omega + alpha * (r[t-1]**2 if t>0 else 0.0) + beta * sigma2
                if sigma2 <= 0:
                    return 1e10
                logL += -0.5 * (np.log(sigma2) + (r[t]**2 / sigma2))
            return -logL   # minimize negative log-likelihood
        
        # Initial parameter guess
        init_params = [0.0001, 0.1, 0.8]
        bounds = [(1e-6, None), (0, 1), (0, 1)]
        constraints = ({'type': 'ineq', 'fun': lambda x: 1 - x[1] - x[2]})
        
        try:
            res = scipy.optimize.minimize(
                neg_log_likelihood, init_params, args=(returns,),
                method='SLSQP', bounds=bounds, constraints=constraints,
                options={'maxiter': 1000, 'ftol': 1e-12}
            )
            if not res.success:
                return None, None
            omega, alpha, beta = res.x
        except:
            return None, None
        
        # Reconstruct conditional variance series
        sigma2_series = np.empty(len(returns))
        sigma2 = np.var(returns)
        for t in range(len(returns)):
            sigma2 = omega + alpha * (returns[t-1]**2 if t>0 else 0.0) + beta * sigma2
            sigma2_series[t] = sigma2
        sigma_series = np.sqrt(sigma2_series)
        last_sigma = sigma_series[-1]
        
        return sigma_series, last_sigma
