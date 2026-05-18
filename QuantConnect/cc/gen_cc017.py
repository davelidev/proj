#!/usr/bin/env python3
"""Generate cc/cc_algos/cc017_001.py through cc017_100.py — 20 batches, 5 algos each."""
import os, textwrap

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cc_algos")

def w(n, code):
    path = os.path.join(OUT, f"cc017_{n:03d}.py")
    with open(path, "w") as f:
        f.write(textwrap.dedent(code).strip() + "\n")
    print(f"  wrote cc017_{n:03d}.py")

# ── Batch 1 (001-005): ADX strength — TQQQ ────────────────────────────────────
# Vary: ADX period + threshold
ADX_PARAMS = [(14,25),(20,20),(10,30),(25,15),(18,22)]
for i, (period, thresh) in enumerate(ADX_PARAMS, 1):
    w(i, f"""
        from AlgorithmImports import *
        class CC17_{i:03d}(QCAlgorithm):
            def Initialize(self):
                self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
                self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
                self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
                self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
                self._adx=self.ADX(self.q,{period},Resolution.Daily)
                self._n={period}; self._st=None; self.SetWarmUp({period+10},Resolution.Daily)
                self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
            def R(self):
                if self.IsWarmingUp or not self._adx.IsReady: return
                h=self.History(self.q,self._n+1,Resolution.Daily)
                if h.empty or len(h)<2: return
                trend_up=float(h['close'].iloc[-1])>float(h['close'].iloc[0])
                st=1 if self._adx.Current.Value>{thresh} and trend_up else 0
                if st==self._st: return
                self._st=st
                if st==1: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
                else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
            def OnData(self,d): pass
    """)

# ── Batch 2 (006-010): Bollinger Bands %B — TQQQ ─────────────────────────────
BB_PARAMS = [(20,2.0),(14,1.5),(30,2.5),(20,1.8),(25,2.2)]
for i, (period, k) in enumerate(BB_PARAMS, 6):
    w(i, f"""
        from AlgorithmImports import *
        class CC17_{i:03d}(QCAlgorithm):
            def Initialize(self):
                self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
                self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
                self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
                self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
                self._bb=self.BB(self.q,{period},{k},MovingAverageType.Simple,Resolution.Daily)
                self._st=None; self.SetWarmUp({period+5},Resolution.Daily)
                self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
            def R(self):
                if self.IsWarmingUp or not self._bb.IsReady: return
                p=self.Securities[self.q].Price
                upper=self._bb.UpperBand.Current.Value; lower=self._bb.LowerBand.Current.Value
                mid=self._bb.MiddleBand.Current.Value
                st=1 if p>mid else 0
                if st==self._st: return
                self._st=st
                if st==1: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
                else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
            def OnData(self,d): pass
    """)

# ── Batch 3 (011-015): ATR Breakout — TQQQ ────────────────────────────────────
ATR_PARAMS = [(14,1.5,20),(10,1.0,15),(20,2.0,25),(14,1.2,30),(18,1.8,20)]
for i, (atr_p, mult, ch_p) in enumerate(ATR_PARAMS, 11):
    w(i, f"""
        from AlgorithmImports import *
        class CC17_{i:03d}(QCAlgorithm):
            def Initialize(self):
                self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
                self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
                self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
                self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
                self._atr=self.ATR(self.q,{atr_p},MovingAverageType.Simple,Resolution.Daily)
                self._ch={ch_p}; self._mult={mult}; self._st=None
                self.SetWarmUp(max({atr_p},{ch_p})+5,Resolution.Daily)
                self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
            def R(self):
                if self.IsWarmingUp or not self._atr.IsReady: return
                h=self.History(self.q,self._ch+1,Resolution.Daily)
                if h.empty or len(h)<self._ch: return
                hi=float(h['high'].iloc[:-1].max())
                p=self.Securities[self.q].Price
                atr=self._atr.Current.Value
                st=1 if p>hi-self._mult*atr else 0
                if st==self._st: return
                self._st=st
                if st==1: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
                else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
            def OnData(self,d): pass
    """)

# ── Batch 4 (016-020): CCI — TQQQ ─────────────────────────────────────────────
CCI_PARAMS = [(14,100),(20,80),(10,120),(25,100),(18,90)]
for i, (period, thresh) in enumerate(CCI_PARAMS, 16):
    w(i, f"""
        from AlgorithmImports import *
        class CC17_{i:03d}(QCAlgorithm):
            def Initialize(self):
                self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
                self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
                self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
                self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
                self._cci=self.CCI(self.q,{period},MovingAverageType.Simple,Resolution.Daily)
                self._st=None; self.SetWarmUp({period+5},Resolution.Daily)
                self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
            def R(self):
                if self.IsWarmingUp or not self._cci.IsReady: return
                v=self._cci.Current.Value
                st=1 if v>-{thresh} else 0
                if st==self._st: return
                self._st=st
                if st==1: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
                else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
            def OnData(self,d): pass
    """)

# ── Batch 5 (021-025): Stochastic Oscillator — TQQQ ──────────────────────────
STO_PARAMS = [(14,3,3,80,20),(10,3,3,75,25),(20,5,3,85,15),(14,5,5,80,20),(12,3,3,70,30)]
for i, (k,d,s,ob,os_) in enumerate(STO_PARAMS, 21):
    w(i, f"""
        from AlgorithmImports import *
        class CC17_{i:03d}(QCAlgorithm):
            def Initialize(self):
                self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
                self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
                self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
                self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
                self._sto=self.STO(self.q,{k},{d},{s},Resolution.Daily)
                self._st=None; self.SetWarmUp({k+d+s+10},Resolution.Daily)
                self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
            def R(self):
                if self.IsWarmingUp or not self._sto.IsReady: return
                sk=self._sto.StochK.Current.Value; sd=self._sto.StochD.Current.Value
                st=1 if sk>sd and sk>{os_} else 0
                if st==self._st: return
                self._st=st
                if st==1: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
                else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
            def OnData(self,d): pass
    """)

# ── Batch 6 (026-030): MACD — TQQQ ────────────────────────────────────────────
MACD_PARAMS = [(12,26,9),(8,21,5),(10,30,9),(12,26,5),(15,35,9)]
for i, (fast,slow,sig) in enumerate(MACD_PARAMS, 26):
    w(i, f"""
        from AlgorithmImports import *
        class CC17_{i:03d}(QCAlgorithm):
            def Initialize(self):
                self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
                self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
                self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
                self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
                self._macd=self.MACD(self.q,{fast},{slow},{sig},MovingAverageType.Exponential,Resolution.Daily)
                self._st=None; self.SetWarmUp({slow+sig+10},Resolution.Daily)
                self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
            def R(self):
                if self.IsWarmingUp or not self._macd.IsReady: return
                st=1 if self._macd.Current.Value>self._macd.Signal.Current.Value else 0
                if st==self._st: return
                self._st=st
                if st==1: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
                else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
            def OnData(self,d): pass
    """)

# ── Batch 7 (031-035): Williams %R — TQQQ ─────────────────────────────────────
WILR_PARAMS = [(14,-20,-80),(20,-15,-85),(10,-25,-75),(14,-30,-70),(18,-20,-80)]
for i, (period, ob, os_) in enumerate(WILR_PARAMS, 31):
    w(i, f"""
        from AlgorithmImports import *
        class CC17_{i:03d}(QCAlgorithm):
            def Initialize(self):
                self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
                self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
                self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
                self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
                self._wr=self.WILR(self.q,{period},Resolution.Daily)
                self._st=None; self.SetWarmUp({period+5},Resolution.Daily)
                self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
            def R(self):
                if self.IsWarmingUp or not self._wr.IsReady: return
                v=self._wr.Current.Value
                st=1 if v>{os_} else 0
                if st==self._st: return
                self._st=st
                if st==1: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
                else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
            def OnData(self,d): pass
    """)

# ── Batch 8 (036-040): Keltner Channel (manual, ATR-based) — TQQQ ─────────────
KC_PARAMS = [(20,14,2.0),(14,10,1.5),(25,14,2.5),(20,14,1.8),(20,20,2.0)]
for i, (ema_p, atr_p, mult) in enumerate(KC_PARAMS, 36):
    w(i, f"""
        from AlgorithmImports import *
        class CC17_{i:03d}(QCAlgorithm):
            def Initialize(self):
                self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
                self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
                self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
                self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
                self._ema=self.EMA(self.q,{ema_p},Resolution.Daily)
                self._atr=self.ATR(self.q,{atr_p},MovingAverageType.Simple,Resolution.Daily)
                self._mult={mult}; self._st=None
                self.SetWarmUp(max({ema_p},{atr_p})+5,Resolution.Daily)
                self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
            def R(self):
                if self.IsWarmingUp or not self._ema.IsReady or not self._atr.IsReady: return
                mid=self._ema.Current.Value; atr=self._atr.Current.Value
                upper=mid+self._mult*atr
                p=self.Securities[self.q].Price
                st=1 if p>mid else 0
                if st==self._st: return
                self._st=st
                if st==1: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
                else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
            def OnData(self,d): pass
    """)

# ── Batch 9 (041-045): Ultimate Oscillator — TQQQ ─────────────────────────────
UO_PARAMS = [(7,14,28,50),(5,10,20,45),(7,14,28,55),(6,12,24,50),(7,14,28,40)]
for i, (s,m,l,thresh) in enumerate(UO_PARAMS, 41):
    w(i, f"""
        from AlgorithmImports import *
        class CC17_{i:03d}(QCAlgorithm):
            def Initialize(self):
                self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
                self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
                self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
                self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
                self._ws={s}; self._wm={m}; self._wl={l}; self._thresh={thresh}
                self._st=None; self.SetWarmUp({l+5},Resolution.Daily)
                self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
            def R(self):
                if self.IsWarmingUp: return
                import numpy as np
                n=self._wl+1
                h=self.History(self.q,n,Resolution.Daily)
                if h.empty or len(h)<n: return
                hi=h['high'].values; lo=h['low'].values; cl=h['close'].values
                pc=np.roll(cl,1); pc[0]=cl[0]
                bp=cl-np.minimum(lo,pc); tr=np.maximum(hi,pc)-np.minimum(lo,pc)
                tr=np.where(tr==0,1e-10,tr)
                def avg(p): return np.sum(bp[-p:])/max(np.sum(tr[-p:]),1e-10)
                uo=100*(4*avg(self._ws)+2*avg(self._wm)+avg(self._wl))/7
                st=1 if uo>self._thresh else 0
                if st==self._st: return
                self._st=st
                if st==1: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
                else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
            def OnData(self,d): pass
    """)

# ── Batch 10 (046-050): Fisher Transform — TQQQ ───────────────────────────────
FT_PARAMS = [(10,0.0),(14,0.5),(9,0.0),(14,0.3),(10,0.2)]
for i, (period, thresh) in enumerate(FT_PARAMS, 46):
    w(i, f"""
        from AlgorithmImports import *
        class CC17_{i:03d}(QCAlgorithm):
            def Initialize(self):
                self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
                self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
                self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
                self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
                self._n={period}; self._thresh={thresh}; self._st=None
                self.SetWarmUp({period+5},Resolution.Daily)
                self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
            def R(self):
                if self.IsWarmingUp: return
                import math
                h=self.History(self.q,self._n,Resolution.Daily)
                if h.empty or len(h)<self._n: return
                hi=float(h['high'].max()); lo=float(h['low'].min())
                cl=float(h['close'].iloc[-1])
                rng=hi-lo if hi!=lo else 1e-10
                val=2*((cl-lo)/rng-0.5)
                val=max(-0.999,min(0.999,val))
                fisher=0.5*math.log((1+val)/(1-val))
                st=1 if fisher>self._thresh else 0
                if st==self._st: return
                self._st=st
                if st==1: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
                else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
            def OnData(self,d): pass
    """)

# ── Batch 11 (051-055): OBV Trend — TQQQ ─────────────────────────────────────
OBV_PARAMS = [(20,),(30,),(14,),(25,),(10,)]
for i, (obv_smooth,) in enumerate(OBV_PARAMS, 51):
    w(i, f"""
        from AlgorithmImports import *
        class CC17_{i:03d}(QCAlgorithm):
            def Initialize(self):
                self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
                self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
                self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
                self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
                self._n={obv_smooth}; self._obv=0.0; self._prev=None; self._st=None
                self._hist=[]; self.SetWarmUp({obv_smooth+5},Resolution.Daily)
                self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
            def R(self):
                if self.IsWarmingUp: return
                bar=self.History(self.q,2,Resolution.Daily)
                if bar.empty or len(bar)<2: return
                cl=bar['close'].values; vol=bar['volume'].values
                if cl[1]>cl[0]: self._obv+=vol[1]
                elif cl[1]<cl[0]: self._obv-=vol[1]
                self._hist.append(self._obv)
                if len(self._hist)>self._n*2: self._hist=self._hist[-self._n*2:]
                if len(self._hist)<self._n: return
                avg=sum(self._hist[-self._n:])/self._n
                st=1 if self._obv>avg else 0
                if st==self._st: return
                self._st=st
                if st==1: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
                else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
            def OnData(self,d): pass
    """)

# ── Batch 12 (056-060): Money Flow Index — TQQQ ───────────────────────────────
MFI_PARAMS = [(14,55,45),(10,60,40),(20,50,50),(14,65,35),(18,55,45)]
for i, (period, ob, os_) in enumerate(MFI_PARAMS, 56):
    w(i, f"""
        from AlgorithmImports import *
        class CC17_{i:03d}(QCAlgorithm):
            def Initialize(self):
                self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
                self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
                self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
                self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
                self._mfi=self.MFI(self.q,{period},Resolution.Daily)
                self._st=None; self.SetWarmUp({period+5},Resolution.Daily)
                self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
            def R(self):
                if self.IsWarmingUp or not self._mfi.IsReady: return
                v=self._mfi.Current.Value
                st=1 if v>{os_} else 0
                if st==self._st: return
                self._st=st
                if st==1: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
                else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
            def OnData(self,d): pass
    """)

# ── Batch 13 (061-065): ROC Momentum Ranking — Top-5 Cap ─────────────────────
ROC_PARAMS = [(12,0),(20,0),(10,2),(14,0),(12,1)]
TICKERS = ["AAPL","MSFT","AMZN","NVDA","GOOGL"]
TIX_STR = str(TICKERS)
for i, (roc_p, thresh) in enumerate(ROC_PARAMS, 61):
    w(i, f"""
        from AlgorithmImports import *
        class CC17_{i:03d}(QCAlgorithm):
            def Initialize(self):
                self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
                self.tix={TIX_STR}
                self.syms={{t:self.AddEquity(t,Resolution.Daily).Symbol for t in self.tix}}
                self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
                self._roc={{t:self.ROC(self.syms[t],{roc_p},Resolution.Daily) for t in self.tix}}
                self._thresh={thresh}; self.SetWarmUp({roc_p+5},Resolution.Daily)
                self.Schedule.On(self.DateRules.MonthStart("AAPL"),self.TimeRules.AfterMarketOpen("AAPL",30),self.R)
            def R(self):
                if self.IsWarmingUp: return
                bulls=[t for t in self.tix if self._roc[t].IsReady and self._roc[t].Current.Value>self._thresh]
                n=len(bulls)
                for t in self.tix: self.SetHoldings(self.syms[t],1.0/n if t in bulls else 0)
                self.SetHoldings(self.b,0 if bulls else 1.0)
            def OnData(self,d): pass
    """)

# ── Batch 14 (066-070): Aroon Oscillator — Top-5 Cap ─────────────────────────
AROON_PARAMS = [(25,0),(14,10),(25,20),(20,0),(25,-20)]
for i, (period, thresh) in enumerate(AROON_PARAMS, 66):
    w(i, f"""
        from AlgorithmImports import *
        class CC17_{i:03d}(QCAlgorithm):
            def Initialize(self):
                self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
                self.tix={TIX_STR}
                self.syms={{t:self.AddEquity(t,Resolution.Daily).Symbol for t in self.tix}}
                self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
                self._aroon={{t:self.AROON(self.syms[t],{period},Resolution.Daily) for t in self.tix}}
                self._thresh={thresh}; self.SetWarmUp({period+5},Resolution.Daily)
                self.Schedule.On(self.DateRules.MonthStart("AAPL"),self.TimeRules.AfterMarketOpen("AAPL",30),self.R)
            def R(self):
                if self.IsWarmingUp: return
                bulls=[t for t in self.tix if self._aroon[t].IsReady and self._aroon[t].AroonOscillator.Current.Value>self._thresh]
                n=len(bulls)
                for t in self.tix: self.SetHoldings(self.syms[t],1.0/n if t in bulls else 0)
                self.SetHoldings(self.b,0 if bulls else 1.0)
            def OnData(self,d): pass
    """)

# ── Batch 15 (071-075): Chande Momentum Oscillator — Top-5 Cap ────────────────
CMO_PARAMS = [(14,0),(20,10),(10,-5),(14,5),(18,0)]
for i, (period, thresh) in enumerate(CMO_PARAMS, 71):
    w(i, f"""
        from AlgorithmImports import *
        class CC17_{i:03d}(QCAlgorithm):
            def Initialize(self):
                self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
                self.tix={TIX_STR}
                self.syms={{t:self.AddEquity(t,Resolution.Daily).Symbol for t in self.tix}}
                self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
                self._n={period}; self._thresh={thresh}; self.SetWarmUp({period+5},Resolution.Daily)
                self.Schedule.On(self.DateRules.MonthStart("AAPL"),self.TimeRules.AfterMarketOpen("AAPL",30),self.R)
            def R(self):
                if self.IsWarmingUp: return
                bulls=[]
                for t in self.tix:
                    h=self.History(self.syms[t],self._n+1,Resolution.Daily)
                    if h.empty or len(h)<self._n+1: continue
                    cl=h['close'].values
                    diffs=[cl[j]-cl[j-1] for j in range(1,len(cl))]
                    up=sum(d for d in diffs if d>0); dn=sum(-d for d in diffs if d<0)
                    cmo=100*(up-dn)/(up+dn+1e-10)
                    if cmo>self._thresh: bulls.append(t)
                n=len(bulls)
                for t in self.tix: self.SetHoldings(self.syms[t],1.0/n if t in bulls else 0)
                self.SetHoldings(self.b,0 if bulls else 1.0)
            def OnData(self,d): pass
    """)

# ── Batch 16 (076-080): Donchian Channel Breakout — Top-5 Cap ─────────────────
DCH_PARAMS = [(20,),(14,),(25,),(20,),(30,)]
for i, (period,) in enumerate(DCH_PARAMS, 76):
    w(i, f"""
        from AlgorithmImports import *
        class CC17_{i:03d}(QCAlgorithm):
            def Initialize(self):
                self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
                self.tix={TIX_STR}
                self.syms={{t:self.AddEquity(t,Resolution.Daily).Symbol for t in self.tix}}
                self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
                self._n={period}; self.SetWarmUp({period+5},Resolution.Daily)
                self.Schedule.On(self.DateRules.MonthStart("AAPL"),self.TimeRules.AfterMarketOpen("AAPL",30),self.R)
            def R(self):
                if self.IsWarmingUp: return
                bulls=[]
                for t in self.tix:
                    h=self.History(self.syms[t],self._n+1,Resolution.Daily)
                    if h.empty or len(h)<self._n+1: continue
                    hi=float(h['high'].iloc[:-1].max())
                    lo=float(h['low'].iloc[:-1].min())
                    cl=float(h['close'].iloc[-1])
                    mid=(hi+lo)/2
                    if cl>mid: bulls.append(t)
                n=len(bulls)
                for t in self.tix: self.SetHoldings(self.syms[t],1.0/n if t in bulls else 0)
                self.SetHoldings(self.b,0 if bulls else 1.0)
            def OnData(self,d): pass
    """)

# ── Batch 17 (081-085): ATR Percentile Volatility Regime — Top-5 Cap ──────────
ATRPCT_PARAMS = [(14,100,50),(14,252,40),(10,100,50),(20,100,60),(14,60,50)]
for i, (atr_p, lookback, pct_thresh) in enumerate(ATRPCT_PARAMS, 81):
    w(i, f"""
        from AlgorithmImports import *
        class CC17_{i:03d}(QCAlgorithm):
            def Initialize(self):
                self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
                self.tix={TIX_STR}
                self.syms={{t:self.AddEquity(t,Resolution.Daily).Symbol for t in self.tix}}
                self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
                self._atr={{t:self.ATR(self.syms[t],{atr_p},MovingAverageType.Simple,Resolution.Daily) for t in self.tix}}
                self._lb={lookback}; self._pct={pct_thresh}; self._atrhist={{t:[] for t in self.tix}}
                self.SetWarmUp({lookback+atr_p+5},Resolution.Daily)
                self.Schedule.On(self.DateRules.MonthStart("AAPL"),self.TimeRules.AfterMarketOpen("AAPL",30),self.R)
            def R(self):
                if self.IsWarmingUp: return
                import numpy as np
                for t in self.tix:
                    if self._atr[t].IsReady:
                        self._atrhist[t].append(self._atr[t].Current.Value)
                        if len(self._atrhist[t])>self._lb*2: self._atrhist[t]=self._atrhist[t][-self._lb*2:]
                bulls=[]
                for t in self.tix:
                    hist=self._atrhist[t]
                    if len(hist)<self._lb: continue
                    cur=hist[-1]; ref=hist[-self._lb:]
                    pct=100*sum(1 for x in ref if cur>x)/len(ref)
                    if pct<self._pct: bulls.append(t)
                n=len(bulls)
                for t in self.tix: self.SetHoldings(self.syms[t],1.0/n if t in bulls else 0)
                self.SetHoldings(self.b,0 if bulls else 1.0)
            def OnData(self,d): pass
    """)

# ── Batch 18 (086-090): VWAP Deviation — Top-5 Cap ───────────────────────────
VWAP_PARAMS = [(20,0),(14,0),(20,0.005),(30,0),(20,-0.01)]
for i, (period, thresh) in enumerate(VWAP_PARAMS, 86):
    w(i, f"""
        from AlgorithmImports import *
        class CC17_{i:03d}(QCAlgorithm):
            def Initialize(self):
                self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
                self.tix={TIX_STR}
                self.syms={{t:self.AddEquity(t,Resolution.Daily).Symbol for t in self.tix}}
                self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
                self._n={period}; self._thresh={thresh}; self.SetWarmUp({period+5},Resolution.Daily)
                self.Schedule.On(self.DateRules.MonthStart("AAPL"),self.TimeRules.AfterMarketOpen("AAPL",30),self.R)
            def R(self):
                if self.IsWarmingUp: return
                bulls=[]
                for t in self.tix:
                    h=self.History(self.syms[t],self._n,Resolution.Daily)
                    if h.empty or len(h)<self._n: continue
                    import numpy as np
                    hi=h['high'].values; lo=h['low'].values; cl=h['close'].values; vol=h['volume'].values
                    tp=(hi+lo+cl)/3
                    vwap=np.sum(tp*vol)/max(np.sum(vol),1)
                    cur=cl[-1]
                    if cur>vwap*(1+self._thresh): bulls.append(t)
                n=len(bulls)
                for t in self.tix: self.SetHoldings(self.syms[t],1.0/n if t in bulls else 0)
                self.SetHoldings(self.b,0 if bulls else 1.0)
            def OnData(self,d): pass
    """)

# ── Batch 19 (091-095): Awesome Oscillator — TQQQ ────────────────────────────
AO_PARAMS = [(5,34,0),(5,34,0.5),(5,34,-0.5),(3,21,0),(5,34,1.0)]
for i, (fast, slow, thresh) in enumerate(AO_PARAMS, 91):
    w(i, f"""
        from AlgorithmImports import *
        class CC17_{i:03d}(QCAlgorithm):
            def Initialize(self):
                self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
                self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
                self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
                self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
                self._fast={fast}; self._slow={slow}; self._thresh={thresh}; self._st=None
                self.SetWarmUp({slow+5},Resolution.Daily)
                self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
            def R(self):
                if self.IsWarmingUp: return
                h=self.History(self.q,self._slow+1,Resolution.Daily)
                if h.empty or len(h)<self._slow: return
                import numpy as np
                mid=(h['high'].values+h['low'].values)/2
                ao=np.mean(mid[-self._fast:])-np.mean(mid[-self._slow:])
                st=1 if ao>self._thresh else 0
                if st==self._st: return
                self._st=st
                if st==1: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
                else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
            def OnData(self,d): pass
    """)

# ── Batch 20 (096-100): Chaikin Money Flow — TQQQ ────────────────────────────
CMF_PARAMS = [(20,0),(14,0.05),(20,-0.05),(20,0.1),(25,0)]
for i, (period, thresh) in enumerate(CMF_PARAMS, 96):
    w(i, f"""
        from AlgorithmImports import *
        class CC17_{i:03d}(QCAlgorithm):
            def Initialize(self):
                self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
                self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
                self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
                self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
                self._n={period}; self._thresh={thresh}; self._st=None
                self.SetWarmUp({period+5},Resolution.Daily)
                self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
            def R(self):
                if self.IsWarmingUp: return
                h=self.History(self.q,self._n,Resolution.Daily)
                if h.empty or len(h)<self._n: return
                import numpy as np
                hi=h['high'].values; lo=h['low'].values; cl=h['close'].values; vol=h['volume'].values
                rng=hi-lo; rng=np.where(rng==0,1e-10,rng)
                mfm=((cl-lo)-(hi-cl))/rng
                cmf=np.sum(mfm*vol)/max(np.sum(vol),1)
                st=1 if cmf>self._thresh else 0
                if st==self._st: return
                self._st=st
                if st==1: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
                else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
            def OnData(self,d): pass
    """)

print("\nDone — 100 files written.")
