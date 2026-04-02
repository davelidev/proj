# Entry and Exit Confessions of a Champion Trader
## 52 Ways a Professional Speculator Gets In and Out of the Stock, Futures and Forex Markets
**Author:** Kevin J. Davey
**Copyright:** © 2019 by Kevin J Davey. All Rights Reserved.

---

## TABLE OF CONTENTS
- [Introduction](#introduction)
- [Part 1: Entries (#1 - #41)](#part-1-entries)
- [Part 2: Exits (#1 - #11)](#part-2-exits)
- [Part 3: Bonus Material](#part-3-bonus-material)
- [Part 4: Some Odds and Ends](#part-4-some-odds-and-ends)
- [Part 5: Suggested Plan of Attack](#part-5-suggested-plan-of-attack)

---

## INTRODUCTION
I create “algos” – trading strategy algorithms that make the buy and sell decisions for me. I also automate most of them, which keeps me from interfering! Using algos I created, I was able to finish in 1st or 2nd place three different years in a worldwide, real money, year-long futures trading contest.

The process to properly develop an algo is complicated – it is not as simple as applying the strategy to a chart and optimizing like crazy– and is advanced material not included in this book. But any algo has to start with the basic components: entries and exits.

---

# PART 1: ENTRIES

## ENTRY #1 – “GO WITH THE FLOW”
**Concept:** Trade in the direction of 1-bar momentum. Reverse position if a bar closes with a loss.
**Tradestation Code:**
```pascal
Var: openloss(1000); //allowable loss per contract
if close<close[1] and (openpositionprofit<-openloss or marketposition=0) then sellshort next bar at market;
if close>close[1] and (openpositionprofit<-openloss or marketposition=0) then buy next bar at market;
```

## ENTRY #2 – “EVERYONE LOVES FRIDAY”
**Concept:** Enters once per week at the open of Monday. If Friday's close is the highest of the last `bbars`, go long.
**Tradestation Code:**
```pascal
Var:bbars(25); 
if dayofweek(date)=5 and close=highest(close,bbars) then buy next bar at market;
if dayofweek(date)=5 and close=lowest(close,bbars) then sellshort next bar at market;
```

## ENTRY #3 – “BOOKS CAN BE GREAT”
**Concept:** Moving average crossover where price must also be below/above the short MA.
**Tradestation Code:**
```pascal
Var: shortma(5), longma(10);
If average(close,shortma) crosses below average(close,longma) and close<average(close,shortma) then buy next bar at market;
If average(close,shortma) crosses above average(close,longma) and close>average(close,shortma) then sellshort next bar at market;
```

## ENTRY #4 – “BREAKOUT WITH A TWIST”
**Concept:** Take breakouts only when ADX(15) < 20 (non-trending period).
**Tradestation Code:**
```pascal
Var: len(10); 
If adx(15)< 20 then Buy next bar at highest(high,len) stop;
If adx(15)< 20 then Sellshort next bar at lowest(low,len) stop;
```

## ENTRY #5 – “AVERAGE TRUE RANGE BASED BREAKOUT”
**Concept:** Breakout must be current close +/- (XX * ATR).
**Tradestation Code:**
```pascal
Var: XX(1), ATRval(15);
Buy next bar at close+XX*AvgTrueRange(ATRVal) stop;
Sellshort next bar at close-XX*AvgTrueRange(ATRVal) stop;
```

## ENTRY #6 – “PERCENT RANKER”
**Concept:** Buy when close is in high percentile of recent history, sell when in low, with an ADX filter (20 < ADX < 30).
**Tradestation Code:**
```pascal
Var: xbars(25);
Value1=percentile(.25,close,xbars); 
Value2=percentile(.75,close,xbars);
If ADX(14) >20 AND ADX(14) <30 AND close<Value1 then sellshort next bar at market;
If ADX(14) >20 AND ADX(14) <30 AND close>Value2 then buy next bar at market;
```

## ENTRY #7 – “INTRADAY BREAKOUT”
**Concept:** Breakout of yesterday's high/low during a specific time window (e.g., 9:45-10:45) if ADX is high.
**Tradestation Code:**
```pascal
Var: tbeg(945), tend(1045), offset(.1), adxP(10), adxThresh(20);
if time>=tbeg and time<=tend then begin
    if EntriesToday(date[0])<1 and adx(adxP) >= AdxThresh then begin
        buy next bar at highd(1) + Offset Points stop;
        sellshort next bar at lowd(1) - Offset points stop;
    end;
end;
```

## ENTRY #8 – “INTRADAY BREAKOUT WITH EXPANDING RANGE”
**Concept:** Same as Entry #7, but yesterday's range must be greater than the range two days ago.
**Tradestation Code:**
```pascal
if time>=tbeg and time<=tend then begin
    if EntriesToday(date[0])<1 and adx(adxP) >= AdxThresh and (highd(1)-lowd(1) > highd(2)-lowd(2)) then begin
        buy next bar at highd(1) + Offset Points stop;
        sellshort next bar at lowd(1) - Offset points stop;
    end;
end;
```

## ENTRY #9 – “DAY OF WEEK TRADING”
**Concept:** Entry based on specific daily biases (e.g., Wednesday long, Thursday short).
**Tradestation Code:**
```pascal
If time=935 and dayofweek(date)= 3 then Buy next bar at highd(1) stop;
If time=935 and dayofweek(date)= 4 then SellShort next bar at lowd(1) stop;
```

## ENTRY #10 – “ENHANCED DAY OF WEEK TRADING”
**Concept:** Adds a momentum filter to Entry #9.
**Tradestation Code:**
```pascal
Var: xbars(10);
If time=935 and dayofweek(date)= 3 and close>close[xbars] then Buy next bar at highd(1) stop;
If time=935 and dayofweek(date)= 4 and close<close[xbars] then SellShort next bar at lowd(1) stop;
```

## ENTRY #11 – “NOT DAY OF WEEK TRADING”
**Concept:** Excludes specific days for entries (e.g., any day except Wednesday for longs).
**Tradestation Code:**
```pascal
If dayofweek(date)<> 3 then Buy next bar at highd(1) stop;
If dayofweek(date)<> 4 then SellShort next bar at lowd(1) stop;
```

## ENTRY #12 – “RSI TRIGGER”
**Concept:** Long if RSI is low and price is above MA; Short if RSI is high and price is below MA.
**Tradestation Code:**
```pascal
Var: RSILength(5), RSIThreshold(80), XBars(5);
If RSI(Close,RSILength)< RSIThreshold And Close > Average(Close,Xbars) Then buy next bar at market;
If RSI(Close,RSILength)> 100-RSIThreshold And Close < Average(Close,Xbars) Then Sellshort next bar at market;
```

## ENTRY #13 – “MOVING AVERAGE CROSS, WITH A TWIST”
**Concept:** MA cross only triggers if price hasn't "run away" from the previous bar's low/high.
**Tradestation Code:**
```pascal
Var: FastLength(10), SlowLength(20), XX(3);
If Average(Close, FastLength) crosses above Average(Close, SlowLength) and close<low+ XX then Buy next bar at market;
If Average(Close, FastLength) crosses below Average(Close, SlowLength) and close>high - XX then Sell Short next bar at market;
```

## ENTRY #14 – “SPLIT WEEK, PART 1”
**Concept:** Mid-week trading (Tue/Wed/Thu) with volatility filter and high/low breakout.
**Tradestation Code:**
```pascal
Var: bbars(15), maxl(2500);
Condition1 = dayofweek(date)=2 or dayofweek(date)=3 or dayofweek(date)=4;
If Condition1 and high=highest(high,bbars) and close=highest(close,bbars) and avgtruerange(14)*BigPointValue<maxl then buy next bar at market;
If Condition1 and low=lowest(low,bbars) and close=lowest(close,bbars) and avgtruerange(14)*BigPointValue<maxl then sellshort next bar at market;
```

## ENTRY #15 – “SPLIT WEEK, PART 2”
**Concept:** Weekend effect trading (Fri/Mon) using similar filters as Part 1.
**Tradestation Code:**
```pascal
Condition1 = dayofweek(date)=5 or dayofweek(date)=1;
// Rest of logic same as Entry 14
```

## ENTRY #16 – “INTRODUCING SERIAL CORRELATION”
**Concept:** Countertrend entry that waits `X` bars after a win or `Y` bars after a loss before re-entering.
**Tradestation Code:**
```pascal
Var: xbars(15);
If ((PositionProfit(1)>0 and BarsSinceExit(1)>=5) or (PositionProfit(1)<=0 and BarsSinceExit(1)>=20) or TotalTrades=0) then begin
    if Close = Lowest( Close, xbars ) then buy next bar at market;
    if Close = Highest( Close, xbars ) then SellShort next bar at market;
end;
```

## ENTRY #17 – “BACK IN STYLE”
**Concept:** Specific price pattern logic modified from Michael Harris.
**Tradestation Code:**
```pascal
if (l[3] > h[0] AND h[0] > l[1] AND l[0] > l[2] AND l[1] > l[2]) then sellshort Next Bar at open;
if (h[3] < l[0] AND l[0] < h[1] AND h[0] < h[2] AND h[1] < h[2]) then buy Next Bar at open;
```

## ENTRY #18 – “WHERE YOU AT?”
**Concept:** Mean-reversion based on stochastic-style range positioning. Disregards early nighttime hours.
**Tradestation Code:**
```pascal
Var: ll(0), hh(0), Thresh(.5);
if time<1600 or time>2300 then begin
    ll=minlist(l,l[1]); hh=maxlist(h,h[1]);
    if (c-ll)/(hh-ll+.000001)>=thresh then sellshort next bar at market;
    if (c-ll)/(hh-ll+.000001)<=(1-thresh) then buy next bar at market;
end;
```

## ENTRY #19 – “EXPONENTIALLY BETTER”
**Concept:** Dual Exponential Moving Average (EMA) crossover.
**Tradestation Code:**
```pascal
var:avg1(10),avg2(20),lookbackdays(10);
avg1=xaverage(close,lookbackdays);
avg2=xaverage(close,lookbackdays*4);
If (avg1>avg2 and avg1[1]<avg2[1]) then Buy next bar at high stop;
If (avg1<avg2 and avg1[1]>avg2[1]) then SellShort next bar at low stop;
```

## ENTRY #20 – “RANGE BREAKOUT”
**Concept:** Uses previous day's range to set breakout levels for the current day. Only allows entry before 13:00.
**Tradestation Code:**
```pascal
// Complex logic to track daily high/low and yesterday's range
If Time <1300 then begin
    Buy next bar at todayopen + xfl*rangeavg stop;
    SellShort next bar at todayopen - xfs*rangeavg stop;
End;
```

## ENTRY #21 – “ASYMMETRIC TRIPLE”
**Concept:** Uses a "triple average" (average of an average) and asymmetric levels for long/short.
**Tradestation Code:**
```pascal
Value1 = TriAverage(LowD(0), Length1);
Value2 = L[Length2];
If Value1>=Value2 then Buy next bar at EntryL stop; // EntryL = C + ATRmult * ATR(14)
If true then SellShort next bar at EntryS stop; // EntryS = LowD(0) - ATRmult * ATR(14)
```

## ENTRY #22 – “ASYMMETRIC AGAIN”
**Concept:** Another asymmetric entry using Open and Previous Close as conditional triggers.
**Tradestation Code:**
```pascal
Value1 = OpenD(0); Value2 = CloseD(1);
If Value1>=Value2 then Buy next bar at EntryL stop;
If true then SellShort next bar at EntryS stop;
```

## ENTRY #23 – “STOCHASTIC CROSS”
**Concept:** Simple cross of the stochastic %k and %d lines.
**Tradestation Code:**
```pascal
Value1 = Stochastic(H, L, C, SLength, Smoothing1, Smoothing2, SmoothingType, oFastK, oFastD, oSlowK, oSlowD);
if oSlowk crosses over oSlowd then buy next bar at market;
if oSlowk crosses under oSlowd then sellshort next bar at market;
```

## ENTRY #24 – “SHOW ME THE MONEY (FLOW)”
**Concept:** Uses Money Flow indicator regions (20 oversold, 80 overbought).
**Tradestation Code:**
```pascal
MoneyFlowVal = MoneyFlow(Length);
if MoneyFlowVal Crosses above OverSold then buy next bar at market;
if MoneyFlowVal Crosses below Overbought then Sellshort next bar at market;
```

## ENTRY #25 – “CLASSIC BOLLINGER BANDS”
**Concept:** Cross of Bollinger Bands with a momentum filter.
**Tradestation Code:**
```pascal
if Close crosses over LowerBand and close>close[Length2] then Buy next bar at market;
if Close crosses under UpperBand and close<close[Length2] then SellShort next bar at market;
```

## ENTRY #26 – “CLASSIC KELTNER CHANNEL”
**Concept:** Same as Bollinger Bands but uses Keltner Channels (ATR based).
**Tradestation Code:**
```pascal
if Close crosses over LowerBand and close>close[Length2] then Buy next bar at market;
if Close crosses under UpperBand and close<close[Length2] then SellShort next bar at market;
```

## ENTRY #27 – “THREE AMIGOS”
**Concept:** Composite entry using RSI(14) > 25, RSI thresholds (50), and multi-lookback momentum.
**Tradestation Code:**
```pascal
If ADX(ADXLength)>25 then begin
    If RSI(close,RSILength)<50 and close<close[lookbackBig] and close>close[lookbackshort] then buy next bar at market;
    If RSI(close,RSILength)>50 and close>close[lookbackBig] and close<close[lookbackshort] then sellshort next bar at market;
end;
```

## ENTRY #28 – “TWO AMIGOS”
**Concept:** Simplified version of Entry 27 using only ADX and single lookback momentum.
**Tradestation Code:**
```pascal
If ADX(ADXLength)>20 then begin
    If close>close[lookback] then buy next bar at market;
    If close<close[lookback] then sellshort next bar at market;
end;
```

## ENTRY #29 – “PITTER PATTER PATTERN”
**Concept:** Bi-directional price pattern based on Michael Harris' work.
**Tradestation Code:**
```pascal
If o[1] > h[0] AND o[0] > c[1] AND c[1] > l[1] AND l[1] > c[0] then buy next bar at market;
if o[1] < l[0] AND o[0] < c[1] AND c[1] < h[1] AND h[1] < c[0] then sell short next bar at market;
```

## ENTRY #30 – “PITTER PATTER PATTERN 2”
**Concept:** Similar to Entry 17 but with signals reversed and an added closing condition.
**Tradestation Code:**
```pascal
If l[3]>h[0] and h[0]>l[1] and l[1]>l[2] and c[0] > c[1] then buy next bar at market;
If h[3]<l[0] and l[0]<h[1] and h[1]<h[2] and c[0] < c[1] then sell short next bar at market;
```

## ENTRY #31 – “CLOSING PATTERN ONLY”
**Concept:** Based strictly on the sequence of recent closes.
**Tradestation Code:**
```pascal
if c[1]>c[3] and c>c[2] and c[2]>c[1] then buy next bar at market;
If c[1]<c[3] and c<c[2] and c[2]<c[1] then Sell short next bar at market;
```

## ENTRY #32 – “QUICK PULLBACK PATTERN”
**Concept:** High, followed by a lower high (pullback), followed by a close above the initial high.
**Tradestation Code:**
```pascal
if h[2]>h[1] and l[2]<l[1] and c>h[2] then buy next bar at market;
if l[2]<l[1] and h[2]>h[1] and c<l[2] then sell short next bar at market;
```

## ENTRY #33 – “CLOSING PATTERN ONLY II”
**Concept:** A 5-bar closing price sequence used in the interest rate sector.
**Tradestation Code:**
```pascal
if c[1]<c[2] and c[2]<c[5] and c[5]<c[3] and c[3]<c[4] then buy next bar at market;
If c[1]>c[2] and c[2]>c[5] and c[5]>c[3] and c[3]>c[4] then Sell short next bar at market;
```

## ENTRY #34 – “BREAKDOWN DEAD AHEAD”
**Concept:** Looks for momentum exhaustion where price moves far from previous close.
**Tradestation Code:**
```pascal
If close>close[momen] then sellshort next bar at close - mult*average(myRange,3) stop;
If close<close[momen] then buy next bar at close + mult*average(myRange,3) stop;
```

## ENTRY #35 – “COMMODITY CHANNEL INDEX”
**Concept:** Direct usage of CCI without additional filters.
**Tradestation Code:**
```pascal
CCIValue = CCI( CCILength ) ; CCIAvg = Average( CCIValue, CCIAvgLength );
if CCIAvg>=100 then sell short next bar at open;
if CCIAvg<=-100 then buy next bar at open;
```

## ENTRY #36 – “BIG TAIL BARS”
**Concept:** Counts "bull tails" and "bear tails" over a period. Enters if one dominates.
**Tradestation Code:**
```pascal
If BullBarTail > BearBarTail and BullBarTail > thresh then buy next bar at market;
If BullBarTail < BearBarTail and BearBarTail > thresh then sellshort next bar at market;
```

## ENTRY #37 – “NEW HIGH WITH CONSECUTIVE HIGHS”
**Concept:** Breakout of 10-bar high confirmed by multiple closing momentum checks.
**Tradestation Code:**
```pascal
Condition1= C > Highest(H,xbars)[1] AND C > C[1] AND C>C[3] AND C[1] > C[2];
Condition2= C < Lowest(L,xbars)[1] AND C < C[1] AND C<C[3] AND C[1] < C[2];
If Condition1 then buy next bar at market;
If Condition2 then sell short next bar at market;
```

## ENTRY #38 – “START WITH AN AWESOME OSCILLATOR”
**Concept:** Bill Williams Awesome Oscillator divergence combined with stochastic-style positioning.
**Tradestation Code:**
```pascal
AO = (value1-value2);
if condition1 and condition4 then sellshort next bar at market;
if condition2 and condition3 then buy next bar at market;
```

## ENTRY #39 – “SECOND VERSE, (ALMOST) SAME AS THE FIRST”
**Concept:** Combines Entry 38 with a seasonal month restriction (Jan-Jun long only, Jul-Dec short only).
**Tradestation Code:**
```pascal
If month(date)<=6 and close=highest(close,xbar) and ((c-l)/(h-l)) <thresh then buy next bar at market;
If month(date)>6 and close=lowest(close,xbar) and ((c-l)/(h-l))>(1-thresh) then sellshort next bar at market;
```

## ENTRY #40 – “IT’S ABOUT TIME!”
**Concept:** Uses specific times of day (e.g., 3:00 or 21:30) as triggers combined with lookback momentum.
**Tradestation Code:**
```pascal
if Bullsignaltime and close>close[barsback] then Buy next bar at close limit;
if Bearsignaltime and close<close[barsback] then sellshort next bar at close limit;
```

## ENTRY #41 – “FILTERED ENTRY”
**Concept:** Highest/lowest close filtered by a range contraction (Yesterday's range < 2 days ago range).
**Tradestation Code:**
```pascal
filter = (highd(1)-lowd(1))< (highd(2)-lowd(2));
IF C = lowest(C, barsback) and filter = true then Sellshort next bar at market;
IF C = highest(C, barsback) and filter = true then buy next bar at market;
```

---

# PART 2: EXITS

## EXIT #1 – “NO EXIT CAN STILL BE AN EXIT”
**Concept:** "Stop and Reverse" – entry into a short position automatically closes the long position.

## EXIT #2 – “START SIMPLE”
**Concept:** Dollar-based stops, ATR-based stops, or hybrid limits.
**Tradestation Code:**
```pascal
Setstoploss(stopATR*AvgTrueRange(15)*BigPointValue);
Setprofittarget(targetATR*AvgTrueRange(15)*BigPointValue);
```

## EXIT #3 – “TIMED EXIT”
**Concept:** Exit exactly `bse` bars after entry.
**Tradestation Code:**
```pascal
If BarsSinceEntry >= bse then begin Sell next bar at market; Buy to cover next bar at market; end;
```

## EXIT #4 – “TIMED EXIT, BY DATE/TIME”
**Concept:** Exit at specific dates or months (e.g., start of year or July).
**Tradestation Code:**
```pascal
if year(date)<>year(date[1]) or (month(date)=7 and month(date[1])=6) then begin
    sell next bar at market; buytocover next bar at market;
end;
```

## EXIT #5 – “PERCENTILE EXIT”
**Concept:** Exits based on where the close is relative to recent percentile performance.
**Tradestation Code:**
```pascal
if close<Percentile(.50, Close, barsback) then Sell next bar at market;
```

## EXIT #6 – “GET OUT, WHILE THE GETTING IS GOOD”
**Concept:** Exit after 3 consecutive bars in your favor (reversion to mean).
**Tradestation Code:**
```pascal
if close>close[1] and close[1]>close[2] and close[2]>close[3] then sell next bar at market;
```

## EXIT #7 – “A REAL WORKING END OF DAY EXIT”
**Concept:** Exits just before the market close to avoid `setexitonclose` rejection issues in real-time.
**Tradestation Code:**
```pascal
Var:TimeExit(1605); //4:05 PM
if Time>=TimeExit then begin sell next bar at open; buy to cover next bar at open; end;
```

## EXIT #8 – “DON’T GIVE IT ALL BACK”
**Concept:** Trailing stop that exits if current profit drops more than `X` ATRs from the peak.
**Tradestation Code:**
```pascal
if maxpositionprofit-openpositionprofit > xATR*avgtruerange(15)*BigPointValue then begin
    sell next bar at market; buytocover next bar at market;
end;
```

## EXIT #9 – “PROFIT PROTECTOR”
**Concept:** Locks in a specific percentage of peak profit once a floor is reached.
**Tradestation Code:**
```pascal
If maxpositionprofit>=ppfloor then begin
    If (openpositionprofit/maxpositionprofit)<ppratio then begin
        Sell next bar at market; Buy To Cover Next bar at market;
    end;
End;
```

## EXIT #10 – “EXIT WHERE YOU LIKE”
**Concept:** Exits at specific price points (support/resistance or high/low of last N bars).
**Tradestation Code:**
```pascal
LongProfExit=highest(high,10); LongLossExit=lowest(low,7);
Sell next bar at LongProfExit limit; Sell next bar at LongLossExit stop;
```

## EXIT #11 – “TIERED EXIT”
**Concept:** Increases the percentage of profit protected as the total profit increases.
**Tradestation Code:**
```pascal
If maxpositionprofit>=ppfloor1 then ppratio=ppratio1;
If maxpositionprofit>=ppfloor2 then ppratio=ppratio2;
If maxpositionprofit>=ppfloor3 then ppratio=ppratio3;
// Then check ratio and exit
```

---

# PART 3: BONUS MATERIAL

## BONUS ENTRY #1 – “THE ULTIMATE”
**Concept:** Entry based on the highest/lowest recent value of Larry Williams' Ultimate Oscillator.
**Tradestation Code:**
```pascal
if UltimateOsc(7,14,28)= lowest(UltimateOsc(7,14,28),xbars) then buy next bar at market;
```

## BONUS ENTRY #2 – “DAY OF WEEK STRATEGY, WITH A TWIST”
**Concept:** Friday buy/Monday short strategy that only triggers if the strategy is currently performing well.
**Tradestation Code:**
```pascal
TotEquity = NetProfit + OpenPositionProfit;
If TotEquity-TotEquity[lookback]>-LossAmt then begin
    If dayofweek(date)=4 then buy next bar at open;
    If dayofweek(date)=5 then sellshort next bar at open;
End;
```

---

# PART 4: SOME ODDS AND ENDS
1. **Variables:** Don't optimize just because you can. Sub-optimal parameters often perform better in real-time.
2. **Intraday vs. Overnight:** Review charts before testing. Overnight systems are generally easier to develop.
3. **Entry Symmetry:** Short trades should be mirror images of long trades to limit curvefitting (except for the stock market's upward bias).
4. **Order Types:** Market orders are reliable. Limit orders can miss trades. Stops can have extreme slippage.
5. **Interaction:** Entry/Exit pairs are what make a strategy. Never discard an entry based on only one exit.

---

# PART 5: SUGGESTED PLAN OF ATTACK
- Read the foundation first.
- Test bar sizes (30m, 60m, Daily).
- Use a solid testing process (Strategy Factory®).
- Evaluate 1-2 entries per week.
- Don't get discouraged by failure.
- **TEST THESE YOURSELF!**
