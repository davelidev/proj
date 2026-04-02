import requests
import warnings
from urllib3.exceptions import NotOpenSSLWarning

# Suppress the specific NotOpenSSLWarning from urllib3 v2.
warnings.filterwarnings('ignore', category=NotOpenSSLWarning)

import yfinance as yf
import pandas as pd
import numpy as np
import os
import pickle
import json
import shutil
from datetime import datetime, timedelta
from tabulate import tabulate
import IPython.display as display

# Configuration
num_stocks = 1000
num_years = 10
current_year = datetime.now().year
today_str = datetime.now().strftime("%Y-%m-%d")
start_year = current_year - num_years
exception_tickers = [] # ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'NVDA', 'META', 'TSLA', 'LLY', 'AVGO']

fetch_fundamentals = False # Set to True to enable fundamental data fetching and filtering

# Define test conditions for dynamic emojis (string format)
test_conditions = {
    'RS Rating': '>=80',
    # 'Drawdown': '<-20',
    'Growth Last 1Y': '>=100',
}

# Define filter conditions
filter_conditions = {
    'RS Rating': '>=90',
    'MarketCap Rank': '<=700',
    # 'ATH Years': '>=8',
    # 'Green Years': '>=8',
    # 'Return': '>600',
    'Dollar Volume': '>=1000000000',
    # 'Max Drawdown': '>-60',
    'SEPA': '==1',
    # 'EPS_Growth_Raw': '>=0.25',
    # 'Rev_Growth_Raw': '>=0.25'
    'Growth Last 1Y': '>=150',
}

# Cache Directory Setup
base_cache_dir = "stock_analysis_cache"
if not os.path.exists(base_cache_dir):
    os.makedirs(base_cache_dir)

# Delete old cache from previous days
for item in os.listdir(base_cache_dir):
    item_path = os.path.join(base_cache_dir, item)
    if os.path.isdir(item_path) and item != today_str:
        shutil.rmtree(item_path)

cache_dir = os.path.join(base_cache_dir, today_str)
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

data_cache_path = os.path.join(cache_dir, f"data_{num_stocks}s_{num_years}y.pkl")
meta_cache_path = os.path.join(cache_dir, f"meta_{num_stocks}s.json")
fund_cache_path = os.path.join(cache_dir, f"fund_{num_stocks}s.json")

# 1. Fetch Tickers & Metadata (with Cache)
ticker_metadata = {}
tickers = []

if os.path.exists(meta_cache_path):
    print("--- Loading Ticker Metadata from Cache ---")
    with open(meta_cache_path, 'r') as f:
        ticker_metadata = json.load(f)
    tickers = list(ticker_metadata.keys())
else:
    print(f"Fetching Top {num_stocks} tickers from Nasdaq...")
    headers = {'user-agent': 'Chrome/96.0.4567.58'}
    try:
        data = requests.get('https://api.nasdaq.com/api/screener/stocks?download=true', headers=headers).json()
        syms = data['data']['rows']
        top_n_list = sorted(syms, reverse=True, key=lambda s: float(s.get('marketCap', '-1') or '-1'))[:num_stocks]

        for rank, s in enumerate(top_n_list, 1):
            t_symbol = s['symbol'].replace('.', '-').replace('/', '-')
            ticker_metadata[t_symbol] = {
                'rank': rank,
                'sector': s.get('sector', 'N/A')
            }
        tickers = list(ticker_metadata.keys())

        with open(meta_cache_path, 'w') as f:
            json.dump(ticker_metadata, f)
    except Exception as e:
        print(f"Ticker fetch failed: {e}")

if 'GOOGL' in tickers:
    tickers.remove('GOOGL')

# 2. Fetch Price Data (with Cache)
df = pd.DataFrame()

if tickers:
    if os.path.exists(data_cache_path):
        print("--- Loading Price Data from Cache ---")
        with open(data_cache_path, 'rb') as f:
            df = pickle.load(f)
    else:
        start_date = f"{start_year}-01-01"
        print(f"Downloading data for {num_years} years for {len(tickers)} stocks...")
        # Fetch both Close and Volume data
        df = yf.download(tickers, start=start_date, auto_adjust=True)[['Close', 'Volume']]

        with open(data_cache_path, 'wb') as f:
            pickle.dump(df, f)

def detect_pivots(prices, volatility_pct):
    """
    Detects significant price pivots (peaks and valleys) using a ZigZag-like algorithm.
    A pivot is identified if the price reverses by more than 3x the 20-day volatility. Returns a list of tuples (pivot_price, reversal_magnitude).
    """
    pivots = []
    prices_3y = prices.iloc[-756:] if len(prices) > 756 else prices
    if prices_3y.empty or pd.isna(volatility_pct) or volatility_pct == 0:
        return []

    threshold = 3 * volatility_pct
    last_extreme = prices_3y.values[0]
    trend = 0 # 0: init, 1: up, -1: down
    
    for p in prices_3y.values:
        if trend == 0:
            if p > last_extreme * (1 + threshold):
                trend = 1
                last_extreme = p
            elif p < last_extreme * (1 - threshold):
                trend = -1
                last_extreme = p
        elif trend == 1: # Uptrend
            if p > last_extreme:
                last_extreme = p
            elif p < last_extreme * (1 - threshold):
                reversal_magnitude = (last_extreme - p) / last_extreme
                pivots.append((last_extreme, reversal_magnitude))
                trend = -1
                last_extreme = p
        elif trend == -1: # Downtrend
            if p < last_extreme:
                last_extreme = p
            elif p > last_extreme * (1 + threshold):
                reversal_magnitude = (p - last_extreme) / last_extreme
                pivots.append((last_extreme, reversal_magnitude))
                trend = 1
                last_extreme = p
    return pivots

# 3. Process Results
results = []
if not df.empty:
    for ticker in tickers:
        try:
            # Ensure both 'Close' and 'Volume' data exist for the ticker
            if ('Close', ticker) not in df.columns or ('Volume', ticker) not in df.columns: continue

            prices = df['Close'][ticker].dropna()
            volumes = df['Volume'][ticker].dropna()

            # If no price data or volume data, skip
            if len(prices) < 252 or len(volumes) < 252: continue

            curr = prices.iloc[-1]

            # --- Max Growth in last year check ---
            # Calculates the maximum possible gain between any two points in the last year,
            # where the purchase date is before the sell date.
            growth_last_1y_pct = np.nan
            prices_1y = prices.iloc[-252:]
            if len(prices_1y) > 1:
                max_gain = 0.0
                max_price_so_far = 0.0
                for price in reversed(prices_1y.values):
                    max_price_so_far = max(max_price_so_far, price)
                    if price > 0:
                        potential_gain = (max_price_so_far - price) / price
                        max_gain = max(max_gain, potential_gain)
                growth_last_1y_pct = max_gain * 100

            # Volatility Calculation
            daily_returns = prices.pct_change(fill_method=None).dropna()
            volatility_pct = daily_returns.std()

            # --- SMA Calculations with Emoji indicators ---
            sma20 = prices.rolling(window=20).mean().iloc[-1]
            
            sma50_series = prices.rolling(window=50).mean()
            sma50 = sma50_series.iloc[-1]
            sma50_up = "🟢" if sma50 > sma50_series.iloc[-2] else "🔴"

            sma150 = prices.rolling(window=150).mean().iloc[-1]

            sma200_series = prices.rolling(window=200).mean()
            sma200 = sma200_series.iloc[-1]
            sma200_up = "🟢" if sma200 > sma200_series.iloc[-2] else "🔴"

            above_20 = "🟢" if curr > sma20 else "🔴"
            above_50 = "🟢" if curr > sma50 else "🔴"
            above_200 = "🟢" if curr > sma200 else "🔴"

            sma20_gt_sma50 = "🟢" if sma20 > sma50 else "🔴"
            sma50_gt_sma200 = "🟢" if sma50 > sma200 else "🔴"

            # Check for Support (MA, Pivots) using Volatility for tolerance
            supports = []
            if sma50 * (1 - volatility_pct) <= curr <= sma50 * (1 + volatility_pct): supports.append("50")
            if sma200 * (1 - volatility_pct) <= curr <= sma200 * (1 + volatility_pct): supports.append("200")
            
            # Check if near any pivot
            pivots = detect_pivots(prices, volatility_pct)
            near_pivots_count = 0
            has_strong_pivot = False
            for p, reversal in pivots:
                if p * (1 - volatility_pct) <= curr <= p * (1 + volatility_pct):
                    near_pivots_count += 1
                    if reversal >= 6 * volatility_pct:
                        has_strong_pivot = True
            if near_pivots_count >= 2 or has_strong_pivot:
                supports.append("Piv")
            
            near_support_val = ", ".join(supports) if supports else "-"

            # --- SEPA Analysis ---
            is_sepa = False
            # Ensure we have at least a year of data and a month of 200-day MA data
            if len(prices) >= 252 and len(sma200_series) > 30:
                prices_52w = prices.iloc[-252:]
                low_52w = prices_52w.min()
                high_52w = prices_52w.max()
                
                # Minervini SEPA Trend Template
                # 1. Price > 150 and > 200
                # 2. 150 > 200
                # 3. 200 trending up (at least 1 month)
                # 4. 50 > 150 > 200
                # 5. Price > 50
                # 6. Price > 1.3 * Low 52w
                # 7. Price within 25% of High 52w
                s1 = curr > sma150 and curr > sma200
                s2 = sma150 > sma200
                s3 = sma200 > sma200_series.iloc[-22]
                s4 = sma50 > sma150
                s5 = curr > sma50
                s6 = curr >= low_52w * 1.30
                s7 = curr >= high_52w * 0.75

                if all([s1, s2, s3, s4, s5, s6, s7]):
                    is_sepa = True

            sepa_val = "✅" if is_sepa else "❌"

            # Weighted RS Calculation
            q1, q2, q3, q4 = prices.iloc[-63], prices.iloc[-126], prices.iloc[-189], prices.iloc[-252]
            weighted_rs = ((curr/q1)*0.4) + ((curr/q2)*0.2) + ((curr/q3)*0.2) + ((curr/q4)*0.2)

            # ATH Years Logic
            yearly_max = prices.resample('YE').max()
            if yearly_max.index[-1].year == current_year:
                yearly_max = yearly_max.iloc[:-1]

            ath_years_count = 0
            running_ath = 0
            for val in yearly_max:
                if val > running_ath:
                    ath_years_count += 1
                    running_ath = val
            
            # Check if ATH (max of current data) was in last 6 months
            ath_date = prices[prices == prices.max()].index[-1]
            six_months_ago = datetime.strptime(today_str, "%Y-%m-%d") - timedelta(days=180)
            ath_6m_val = "✅" if ath_date >= six_months_ago else "❌"

            drawdown = ((curr - prices.max()) / prices.max()) * 100

            # Maximum drawdown over the period
            cumulative_max = prices.cummax()
            max_drawdown_series = (prices - cumulative_max) / cumulative_max
            max_drawdown = max_drawdown_series.min() * 100 if not max_drawdown_series.empty else 0

            # Use .values[0] to get the first element to avoid any indexing ambiguity
            total_return = ((curr - prices.values[0]) / prices.values[0]) * 100 if prices.values[0] != 0 else 0

            yearly_closes = prices.resample('YE').last()
            if yearly_closes.index[-1].year == current_year:
                yearly_closes = yearly_closes.iloc[:-1]

            # Explicitly create the first price point with its correct DatetimeIndex
            # to ensure proper concatenation and calculation.
            price_series = pd.concat([pd.Series([prices.values[0]], index=[prices.index[0]]), yearly_closes])
            annual_returns = price_series.pct_change(fill_method=None).dropna()
            green_years = f"{(annual_returns > 0).sum()}/{len(annual_returns)}"

            # Calculate Dollar Volume for the last month
            today_date = datetime.strptime(today_str, "%Y-%m-%d")
            one_month_ago = today_date - timedelta(days=30)

            # Combine prices and volumes for dollar volume calculation
            combined_data = pd.DataFrame({'Close': prices, 'Volume': volumes}).dropna()
            if combined_data.empty: continue # Skip if no combined data

            # Filter for the last month
            last_month_data = combined_data[combined_data.index >= one_month_ago]
            last_month_dollar_volume = (last_month_data['Close'] * last_month_data['Volume']).sum()


            results.append({
                'Ticker': ticker,
                'MarketCap Rank': ticker_metadata[ticker]['rank'],
                'Raw_RS': weighted_rs,
                'Drawdown': drawdown,
                'Max Drawdown': max_drawdown,
                'Return': total_return,
                'ATH Years': f"{ath_years_count}/{len(yearly_max)}",
                'Green Years': green_years,
                'Dollar Volume': last_month_dollar_volume,
                'SEPA': 1 if is_sepa else 0,
                'Growth Last 1Y': growth_last_1y_pct,
                'SEPA, ATH <6m | >50, 200\n20>50>200 | ↗50 ↗200': f"{sepa_val} {ath_6m_val} | {above_50} {above_200} | {sma20_gt_sma50} {sma50_gt_sma200} | {sma50_up} {sma200_up}",
                'Support': near_support_val,
                'SMA20_raw': sma20,
                'SMA50_raw': sma50,
                'SMA200_raw': sma200, # Add raw SMA200 value
                'Sector': ticker_metadata[ticker]['sector']
            })
        except Exception: continue

    # Helper function to parse condition strings into lambda functions
    def create_condition_func(col_name, condition_str):
        import operator
        ops = {
            '>=': operator.ge,
            '>': operator.gt,
            '<=': operator.le,
            '<': operator.lt,
            '==': operator.eq
        }

        # Find the operator and split the string
        found_op = None
        value_str = None
        for op_symbol in sorted(ops.keys(), key=len, reverse=True): # Check multi-char ops first
            if op_symbol in condition_str:
                op_parts = condition_str.split(op_symbol, 1)
                value_str = op_parts[1].strip().replace('%', '')
                found_op = ops[op_symbol]
                break
        if found_op is None:
            raise ValueError(f"Unsupported operator in condition string: {condition_str}")

        # Convert value string to float
        try:
            val = float(value_str)
        except ValueError:
            raise ValueError(f"Invalid numeric value in condition: {value_str}")

        # Return appropriate lambda function based on column type
        if 'Years' in col_name: # Specific handling for 'ATH Years' and 'Green Years'
            return lambda x: found_op(int(x.split('/')[0]), val)
        else: # General numeric comparison
            return lambda x: found_op(x, val)

    # Helper function to format dollar volume with M, B suffix and 3 digits
    def format_dollar_volume(value):
        if value >= 1_000_000_000:
            return f"{value / 1_000_000_000:.0f}B"
        elif value >= 1_000_000:
            return f"{value / 1_000_000:.0f}M"
        else:
            return f"{value:,.0f}"

    # 4. Display Logic
    res_df = pd.DataFrame(results)
    if not res_df.empty:
        res_df['RS Rating'] = (res_df['Raw_RS'].rank(pct=True) * 99).astype(int)
        res_df = res_df.sort_values(by='MarketCap Rank', ascending=True)

        # --- Split filters and apply technical filters first ---
        fundamental_filter_keys = ['EPS_Growth_Raw', 'Rev_Growth_Raw', 'Profit_Margin_Raw']
        technical_filters = {k: v for k, v in filter_conditions.items() if k not in fundamental_filter_keys}
        fundamental_filters = {k: v for k, v in filter_conditions.items() if k in fundamental_filter_keys}

        tech_mask = pd.Series(True, index=res_df.index)
        for col_name, cond_str in technical_filters.items():
            if col_name in res_df.columns:
                filter_func = create_condition_func(col_name, cond_str)
                tech_mask &= res_df[col_name].apply(filter_func)
        res_df = res_df[tech_mask | res_df['Ticker'].isin(exception_tickers)]

        # --- Fetch Fundamentals and apply fundamental filters ---
        if fetch_fundamentals and not res_df.empty:
            print(f"Fetching fundamentals for {len(res_df)} technically qualified stocks...")
            
            fundamental_cache = {}
            if os.path.exists(fund_cache_path):
                with open(fund_cache_path, 'r') as f:
                    fundamental_cache = json.load(f)

            eps_growth_raw, rev_growth_raw, profit_margin_raw = [], [], []
            cache_updated = False
            
            for t in res_df['Ticker']:
                if t in fundamental_cache:
                    try:
                        eg, rg, pm = fundamental_cache[t]
                    except (ValueError, TypeError):
                        try:
                            info = yf.Ticker(t).info
                            eg, rg, pm = info.get('earningsQuarterlyGrowth'), info.get('revenueGrowth'), info.get('profitMargins')
                        except:
                            eg, rg, pm = None, None, None
                        fundamental_cache[t] = [eg, rg, pm]
                        cache_updated = True
                else:
                    try:
                        info = yf.Ticker(t).info
                        eg, rg, pm = info.get('earningsQuarterlyGrowth'), info.get('revenueGrowth'), info.get('profitMargins')
                    except:
                        eg, rg, pm = None, None, None
                    fundamental_cache[t] = [eg, rg, pm]
                    cache_updated = True

                eps_growth_raw.append(eg if eg is not None else np.nan)
                rev_growth_raw.append(rg if rg is not None else np.nan)
                profit_margin_raw.append(pm if pm is not None else np.nan)
            
            if cache_updated:
                with open(fund_cache_path, 'w') as f:
                    json.dump(fundamental_cache, f)

            res_df['EPS_Growth_Raw'] = eps_growth_raw
            res_df['Rev_Growth_Raw'] = rev_growth_raw
            res_df['Profit_Margin_Raw'] = profit_margin_raw

            fund_mask = pd.Series(True, index=res_df.index)
            for col_name, cond_str in fundamental_filters.items():
                if col_name in res_df.columns:
                    filter_func = create_condition_func(col_name, cond_str)
                    fund_mask &= res_df[col_name].apply(filter_func).fillna(False)
            res_df = res_df[fund_mask | res_df['Ticker'].isin(exception_tickers)]

        # Check if res_df is empty after filtering
        if res_df.empty:
            display.display(display.HTML(f"<h2>TOP {num_stocks} STOCKS PERFORMANCE (Complete Years: {start_year}-{current_year-1} | As of: {today_str})</h2>"))
            display.display(display.HTML("<p>No stocks match the current filter criteria.</p>"))
        else:
            # Conditionally format fundamental columns
            if fetch_fundamentals:
                res_df['EPS Q/Q'] = res_df['EPS_Growth_Raw'].apply(lambda x: f"{x*100:.0f}%" if pd.notna(x) else "-")
                res_df['Rev Q/Q'] = res_df['Rev_Growth_Raw'].apply(lambda x: f"{x*100:.0f}%" if pd.notna(x) else "-")
                res_df['Profit Margin'] = res_df['Profit_Margin_Raw'].apply(lambda x: f"{x*100:.1f}%" if pd.notna(x) else "-")
            else:
                # If fundamentals weren't fetched, these columns won't be displayed.
                pass
            # Convert string conditions to lambda functions for dynamic testers
            parsed_test_conditions = {}
            for col, cond_str in test_conditions.items():
                parsed_test_conditions[col] = create_condition_func(col, cond_str)

            # --- Apply dynamic testers with explicit optionality and consistent formatting ---
            columns_to_process = {
                'MarketCap Rank': {'raw_col': 'MarketCap Rank', 'display_col': 'Mkt\nCap', 'format_func': lambda x: str(x)},
                'RS Rating': {'raw_col': 'RS Rating', 'display_col': 'RS#', 'format_func': lambda x: str(x)},
                'Growth Last 1Y': {'raw_col': 'Growth Last 1Y', 'display_col': '1Y\nGrowth', 'format_func': lambda x: f"{x:.0f}%" if pd.notna(x) else "-"},
                'ATH Years': {'raw_col': 'ATH Years', 'display_col': 'ATH\nYear', 'format_func': lambda x: x}, # Already formatted as string "X/Y"
                'Green Years': {'raw_col': 'Green Years', 'display_col': 'Green\nYears', 'format_func': lambda x: x}, # Already formatted as string "X/Y"
                'Drawdown': {'raw_col': 'Drawdown', 'display_col': 'Drawdown', 'format_func': lambda x: f"{x:.2f}%"},
                'Max Drawdown': {'raw_col': 'Max Drawdown', 'display_col': 'Max DD', 'format_func': lambda x: f"{x:.2f}%"},
                'Return': {'raw_col': 'Return', 'display_col': f'{num_years}Y Return', 'format_func': lambda x: f"{x:,.2f}%"},
                'Dollar Volume': {'raw_col': 'Dollar Volume', 'display_col': '$Vol', 'format_func': format_dollar_volume}
            }

            for col_key, config in columns_to_process.items():
                raw_col = config['raw_col']
                display_col = config['display_col']
                format_func = config['format_func']

                # Get the formatted base value (without emoji)
                display_values = res_df[raw_col].apply(format_func)

                if col_key in parsed_test_conditions:
                    condition_func = parsed_test_conditions[col_key]
                    # Apply emoji based on the raw value for the condition check
                    emoji_prefix = res_df[raw_col].apply(
                        lambda x: "🟢 " if condition_func(x) else "🔴 "
                    )
                    res_df[display_col] = emoji_prefix + display_values
                else:
                    res_df[display_col] = display_values

            # Define emojis for sectors
            sector_emojis = {
                'Technology': '💻',
                'Health Care': '🏥',
                'Financial Services': '🏦',
                'Finance': '🏦',
                'Consumer Discretionary': '🛒',
                'Communication Services': '📡',
                'Telecommunications': '📡',
                'Industrials': '🏭',
                'Basic Materials': '🧱',
                'Energy': '⚡️',
                'Utilities': '💡',
                'Consumer Staples': '🍎',
                'Real Estate': '🏘️',
                'N/A': '❓'
            }
            res_df['Sector Emoji'] = res_df['Sector'].map(sector_emojis).fillna('❓')
            res_df['Sector'] = res_df['Sector Emoji'] + ' ' + res_df['Sector']

            # Select and Order Columns
            display_cols = ['Ticker', 'Mkt\nCap', '$Vol', 'RS#', '1Y\nGrowth']
            if fetch_fundamentals:
                display_cols.extend(['EPS Q/Q', 'Rev Q/Q', 'Profit Margin'])
            display_cols.extend(['SEPA, ATH <6m | >50, 200\n20>50>200 | ↗50 ↗200', 'Support', 'Drawdown', 'Max DD', f'{num_years}Y Return', 'ATH\nYear', 'Green\nYears', 'Sector'])
            final_df = res_df[display_cols]

            # Print as a formatted table to console
            print(f"\nTOP {num_stocks} STOCKS PERFORMANCE (Complete Years: {start_year}-{current_year-1} | As of: {today_str})\n")
            # Ensure tabulate is imported if it was removed in a previous step.
            # It's already in the context, so no need to add an import line here.
            from tabulate import tabulate # Re-add import if it was removed
            print(tabulate(final_df, headers='keys', tablefmt='fancy_grid', showindex=False, colalign=("left",)*len(final_df.columns)))
            print(','.join(final_df['Ticker'].tolist()))