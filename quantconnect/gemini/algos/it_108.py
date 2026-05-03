from AlgorithmImports import *
import numpy as np
import pandas as pd

class AdaptiveInOut(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.INI_WAIT_DAYS = 15
        
        # 'In' and 'out' holdings
        self.MRKT = self.AddEquity("SPY", Resolution.Daily).Symbol
        self.TLT = self.AddEquity("TLT", Resolution.Daily).Symbol
        self.IEF = self.AddEquity("IEF", Resolution.Daily).Symbol
        
        self.risk_off = [self.TLT, self.IEF]
        
        # Signals
        self.PRDC = self.AddEquity("XLI", Resolution.Daily).Symbol
        self.METL = self.AddEquity("DBB", Resolution.Daily).Symbol
        self.NRES = self.AddEquity("IGE", Resolution.Daily).Symbol
        self.DEBT = self.AddEquity("SHY", Resolution.Daily).Symbol
        self.USDX = self.AddEquity("UUP", Resolution.Daily).Symbol
        self.SIGNALS = [self.PRDC, self.METL, self.NRES, self.DEBT, self.USDX]
        
        # Pairs for comparative returns
        self.GOLD = self.AddEquity("GLD", Resolution.Daily).Symbol
        self.SLVA = self.AddEquity("SLV", Resolution.Daily).Symbol
        self.UTIL = self.AddEquity("XLU", Resolution.Daily).Symbol
        self.INDU = self.PRDC
        self.SHCU = self.AddEquity("FXF", Resolution.Daily).Symbol
        self.RICU = self.AddEquity("FXA", Resolution.Daily).Symbol
        self.FORPAIRS = [self.GOLD, self.SLVA, self.UTIL, self.SHCU, self.RICU]
        
        self.be_in = True
        self.dcount = 0
        self.outday = 0
        self.WDadjvar = self.INI_WAIT_DAYS
        
        self.Schedule.On(self.DateRules.EveryDay(self.MRKT), 
                         self.TimeRules.AfterMarketOpen(self.MRKT, 75), 
                         self.Rebalance)
        
        self.SetWarmUp(253, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp: return
        
        # History for signals
        all_symbols = self.SIGNALS + [self.MRKT] + self.FORPAIRS
        hist = self.History(all_symbols, 253, Resolution.Daily)
        if hist.empty: return
        
        # Pivot history to get close prices
        hist = hist['close'].unstack(level=0)
        
        # Shifted history (60 days ago)
        hist_shift = hist.shift(60)
        returns_sample = (hist / hist_shift - 1).dropna()
        
        if returns_sample.empty: return
        
        # Reverse code USDX
        returns_sample[self.USDX] = returns_sample[self.USDX] * (-1)
        
        # Comparative returns signals
        returns_sample['G_S'] = -(returns_sample[self.GOLD] - returns_sample[self.SLVA])
        returns_sample['U_I'] = -(returns_sample[self.UTIL] - returns_sample[self.INDU])
        returns_sample['C_A'] = -(returns_sample[self.SHCU] - returns_sample[self.RICU])
        pairlist = ['G_S', 'U_I', 'C_A']
        
        # Extreme observations (1% percentile)
        pctl_b = returns_sample.quantile(0.01)
        extreme_b = returns_sample.iloc[-1] < pctl_b
        
        # Adaptive wait days
        g_s_val = returns_sample[self.GOLD].iloc[-1]
        s_l_v_val = returns_sample[self.SLVA].iloc[-1]
        u_t_i_val = returns_sample[self.UTIL].iloc[-1]
        i_n_d_val = returns_sample[self.INDU].iloc[-1]
        s_h_c_val = returns_sample[self.SHCU].iloc[-1]
        r_i_c_val = returns_sample[self.RICU].iloc[-1]
        
        g_s_ratio = g_s_val / s_l_v_val if s_l_v_val != 0 else 1
        u_i_ratio = u_t_i_val / i_n_d_val if i_n_d_val != 0 else 1
        c_a_ratio = s_h_c_val / r_i_c_val if r_i_c_val != 0 else 1
        
        self.WDadjvar = int(max(0.50 * self.WDadjvar, self.INI_WAIT_DAYS * max(1, g_s_ratio, u_i_ratio, c_a_ratio)))
        adjwaitdays = min(60, self.WDadjvar)
        
        # Market state logic
        if any(extreme_b[self.SIGNALS]) or any(extreme_b[pairlist]):
            self.be_in = False
            self.outday = self.dcount
            
        if self.dcount >= self.outday + adjwaitdays:
            self.be_in = True
            
        self.dcount += 1
        
        if self.be_in:
            if not self.Portfolio[self.MRKT].Invested:
                self.Liquidate()
                self.SetHoldings(self.MRKT, 1.0)
        else:
            if not (self.Portfolio[self.risk_off[0]].Invested or self.Portfolio[self.risk_off[1]].Invested):
                self.Liquidate()
                self.SetHoldings(self.risk_off[0], 0.5)
                self.SetHoldings(self.risk_off[1], 0.5)
