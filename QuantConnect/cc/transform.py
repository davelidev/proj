#!/usr/bin/env python3
"""
Replace hardcoded Mega-7 baskets with dynamic top-5 market-cap universe.
Each file gets handled individually since patterns vary.
"""

import os

ALGOS_DIR = "cc/algos2"

# Template universe init + Sel method
UNIVERSE_BLOCK = """
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self._Sel)

    def _Sel(self, fundamental):
        elig = [f for f in fundamental
                if f.HasFundamentalData and f.MarketCap > 0 and f.Price > 5]
        elig.sort(key=lambda f: f.MarketCap, reverse=True)
        self._universe = [f.Symbol for f in elig[:5]]
        return self._universe
"""

# ---- Per-file transformations ----

def transform(fpath, num):
    with open(fpath) as f:
        c = f.read()

    if num == 31:
        c = c.replace(
            '        basket = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA"]\n'
            '        self.basket_symbols = []\n'
            '        for t in basket:\n'
            '            eq = self.AddEquity(t, Resolution.Daily)\n'
            '            self.basket_symbols.append(eq.Symbol)\n',
            ''
        )
        c = c.replace('self.basket_symbols', 'self._universe')

    elif num == 32:
        c = c.replace(
            '        basket = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN"]\n'
            '        self.basket_symbols = []\n'
            '        for t in basket:\n'
            '            eq = self.AddEquity(t, Resolution.Daily)\n'
            '            self.basket_symbols.append(eq.Symbol)\n',
            ''
        )
        c = c.replace('self.basket_symbols', 'self._universe')

    elif num == 33:
        c = c.replace(
            '        basket = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA"]\n'
            '        self.basket_symbols = []\n'
            '        for t in basket:\n'
            '            eq = self.AddEquity(t, Resolution.Daily)\n'
            '            self.basket_symbols.append(eq.Symbol)\n',
            ''
        )
        c = c.replace('self.basket_symbols', 'self._universe')

    elif num == 34:
        c = c.replace(
            '        basket = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA"]\n'
            '        self.basket_symbols = []\n'
            '        for t in basket:\n'
            '            eq = self.AddEquity(t, Resolution.Daily)\n'
            '            self.basket_symbols.append(eq.Symbol)\n',
            ''
        )
        c = c.replace('self.basket_symbols', 'self._universe')

    elif num == 38:
        # Fixed-weight → EW: remove weight_map dict, AddEquity loop, use _universe
        c = c.replace(
            '        weights = {\n'
            '            "AAPL": 0.20,\n'
            '            "MSFT": 0.20,\n'
            '            "NVDA": 0.15,\n'
            '            "GOOGL": 0.15,\n'
            '            "AMZN": 0.15,\n'
            '            "META": 0.10,\n'
            '            "TSLA": 0.05,\n'
            '        }\n'
            '        self.weight_map = {}\n'
            '        for t, w in weights.items():\n'
            '            eq = self.AddEquity(t, Resolution.Daily)\n'
            '            self.weight_map[eq.Symbol] = w\n',
            ''
        )
        c = c.replace('self.weight_map', 'self._universe')
        c = c.replace(
            'for sym, w in self._universe.items():',
            'for sym in self._universe:\n                    w = 1.0 / len(self._universe)'
        )
        c = c.replace(
            'for sym, w in self._universe.items():\n                self.SetHoldings(sym, w)',
            'for sym in self._universe:\n                w = 1.0 / len(self._universe)\n                self.SetHoldings(sym, w)'
        )

    elif num == 40:
        c = c.replace(
            '        basket = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA"]\n'
            '        self.basket_symbols = []\n'
            '        for t in basket:\n'
            '            eq = self.AddEquity(t, Resolution.Daily)\n'
            '            self.basket_symbols.append(eq.Symbol)\n',
            ''
        )
        c = c.replace('self.basket_symbols', 'self._universe')

    elif num == 41:
        c = c.replace(
            '        self.tickers = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA"]\n'
            '        self.symbols = [self.AddEquity(t, Resolution.Daily).Symbol for t in self.tickers]\n',
            ''
        )
        c = c.replace('self.symbols', 'self._universe')

    elif num == 42:
        c = c.replace(
            '        self.tickers = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA"]\n'
            '        self.symbols = [self.AddEquity(t, Resolution.Daily).Symbol for t in self.tickers]\n',
            ''
        )
        c = c.replace('self.symbols', 'self._universe')

    elif num == 43:
        # Fixed-weight → EW
        c = c.replace(
            '        # Fixed cap-style weights (sum=1.0)\n'
            '        self.weights_by_ticker = {\n'
            '            "AAPL": 0.20,\n'
            '            "MSFT": 0.20,\n'
            '            "NVDA": 0.15,\n'
            '            "GOOGL": 0.15,\n'
            '            "AMZN": 0.15,\n'
            '            "META": 0.10,\n'
            '            "TSLA": 0.05,\n'
            '        }\n'
            '        self.symbol_weights = []\n'
            '        for t, w in self.weights_by_ticker.items():\n'
            '            sym = self.AddEquity(t, Resolution.Daily).Symbol\n'
            '            self.symbol_weights.append((sym, w))\n',
            ''
        )
        c = c.replace('self.symbol_weights', 'self._universe')
        c = c.replace(
            'for sym, w in self._universe:',
            'for sym in self._universe:\n                w = 1.0 / len(self._universe)'
        )

    elif num == 44:
        c = c.replace(
            '        self.tickers = [\n'
            '            "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN",\n'
            '            "META", "TSLA", "AVGO", "JPM", "V",\n'
            '        ]\n'
            '        self.symbols = [self.AddEquity(t, Resolution.Daily).Symbol for t in self.tickers]\n',
            ''
        )
        c = c.replace('self.symbols', 'self._universe')

    elif num == 45:
        c = c.replace(
            '        self.tickers = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA"]\n'
            '        self.symbols = [self.AddEquity(t, Resolution.Daily).Symbol for t in self.tickers]\n',
            ''
        )
        c = c.replace('self.symbols', 'self._universe')
        # Schedule uses self._universe[0] → need QQQ anchor
        c = c.replace('self._universe[0]', 'self.qqq')

    elif num == 46:
        c = c.replace(
            '        self.tickers = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA"]\n'
            '        self.symbols = [self.AddEquity(t, Resolution.Daily).Symbol for t in self.tickers]\n',
            ''
        )
        c = c.replace('self.symbols', 'self._universe')
        c = c.replace(
            "self.weights = {s: 1.0 / len(self._universe) for s in self._universe}",
            "self.weights = {}"
        )

    elif num == 47:
        c = c.replace(
            '        self.tickers = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA"]\n'
            '        self.symbols = [self.AddEquity(t, Resolution.Daily).Symbol for t in self.tickers]\n',
            ''
        )
        c = c.replace('self.symbols', 'self._universe')
        c = c.replace(
            "self.weights = {s: 1.0 / len(self._universe) for s in self._universe}",
            "self.weights = {}"
        )

    elif num == 49:
        c = c.replace(
            '        self.tickers = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA"]\n'
            '        self.symbols = [self.AddEquity(t, Resolution.Daily).Symbol for t in self.tickers]\n',
            ''
        )
        c = c.replace('self.symbols', 'self._universe')

    elif num == 50:
        c = c.replace(
            '        self.tickers = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA"]\n'
            '        self.symbols = [self.AddEquity(t, Resolution.Daily).Symbol for t in self.tickers]\n',
            ''
        )
        c = c.replace('self.symbols', 'self._universe')

    elif num in (51, 52, 53, 54, 55, 57, 58, 59, 60):
        c = c.replace('    MEGA = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA"]\n', '')
        c = c.replace('    MEGA = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA", "AVGO"]\n', '')
        c = c.replace(
            '        self.syms = [self.AddEquity(t, Resolution.Daily).Symbol for t in self.MEGA]\n',
            ''
        )

        # Fix schedule ticker before replacing syms → _universe
        c = c.replace('self.syms[0]', 'self.qqq')
        c = c.replace('self.syms', 'self._universe')

        if num in (51, 53, 54, 55, 58, 59, 60):
            # These have TQQQ already - add QQQ anchor after tqqq
            pass
        elif num in (52, 57):
            # These have no anchor - need QQQ schedule anchor
            c = c.replace("self._universe[0]", "self.qqq")

    # ---- Add universe selection where needed ----
    if num == 31:
        # No QQQ, needs QQQ + universe
        c = c.replace(
            '        self.SetCash(100_000)\n\n        self.regime_in',
            '        self.SetCash(100_000)' + UNIVERSE_BLOCK + '\n        self.regime_in'
        )
    elif num == 32:
        # Has QQQ, add universe after the QQQ line
        c = c.replace(
            '        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol\n'
            '        self.rsi',
            '        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol\n'
            '        self.UniverseSettings.Resolution = Resolution.Daily\n'
            '        self.AddUniverse(self._Sel)\n'
            '        self.rsi'
        )
    elif num == 33:
        c = c.replace(
            '        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol\n'
            '        self.sma50',
            '        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol\n'
            '        self.UniverseSettings.Resolution = Resolution.Daily\n'
            '        self.AddUniverse(self._Sel)\n'
            '        self.sma50'
        )
    elif num == 34:
        c = c.replace(
            '        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol\n\n'
            '        self.regime_in',
            '        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol\n'
            '        self.UniverseSettings.Resolution = Resolution.Daily\n'
            '        self.AddUniverse(self._Sel)\n\n'
            '        self.regime_in'
        )
    elif num == 38:
        c = c.replace(
            '        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol\n'
            '        self.atr',
            '        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol\n'
            '        self.UniverseSettings.Resolution = Resolution.Daily\n'
            '        self.AddUniverse(self._Sel)\n'
            '        self.atr'
        )
    elif num == 40:
        c = c.replace(
            '        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol\n'
            '        self.sma50',
            '        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol\n'
            '        self.UniverseSettings.Resolution = Resolution.Daily\n'
            '        self.AddUniverse(self._Sel)\n'
            '        self.sma50'
        )
    elif num in (41, 42, 44, 46, 47, 49, 50):
        c = c.replace(
            '        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol\n\n'
            '        self.vol_threshold',
            '        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol\n'
            '        self.UniverseSettings.Resolution = Resolution.Daily\n'
            '        self.AddUniverse(self._Sel)\n\n'
            '        self.vol_threshold'
        )
    elif num == 43:
        c = c.replace(
            '        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol\n'
            '        self.vol_threshold',
            '        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol\n'
            '        self.UniverseSettings.Resolution = Resolution.Daily\n'
            '        self.AddUniverse(self._Sel)\n'
            '        self.vol_threshold'
        )
    elif num == 45:
        # Needs QQQ + universe
        c = c.replace(
            '        self.vol_threshold = 0.25\n'
            '        self.in_market',
            '        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol\n'
            '        self.UniverseSettings.Resolution = Resolution.Daily\n'
            '        self.AddUniverse(self._Sel)\n'
            '        self.vol_threshold = 0.25\n'
            '        self.in_market'
        )
    elif num in (51, 53, 54, 55, 58, 59, 60):
        # These have TQQQ, need QQQ anchor + universe
        c = c.replace(
            '        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol\n',
            '        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol\n'
            '        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol\n'
            '        self.UniverseSettings.Resolution = Resolution.Daily\n'
            '        self.AddUniverse(self._Sel)\n'
        )
    elif num in (52, 57):
        # No TQQQ, no anchor, need QQQ + universe
        c = c.replace(
            '        self.SetCash(100_000)\n',
            '        self.SetCash(100_000)\n'
            '        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol\n'
            '        self.UniverseSettings.Resolution = Resolution.Daily\n'
            '        self.AddUniverse(self._Sel)\n'
        )

    # ---- Add _Sel method if not present ----
    if "def _Sel(self" not in c:
        # Insert before the last method in the file
        lines = c.split('\n')
        last_def = -1
        for i, line in enumerate(lines):
            if line.strip().startswith('def '):
                last_def = i
        if last_def > 0:
            indent = lines[last_def][:len(lines[last_def]) - len(lines[last_def].lstrip())]
            sel = (
                f'\n{indent}def _Sel(self, fundamental):\n'
                f'{indent}    elig = [f for f in fundamental\n'
                f'{indent}            if f.HasFundamentalData and f.MarketCap > 0 and f.Price > 5]\n'
                f'{indent}    elig.sort(key=lambda f: f.MarketCap, reverse=True)\n'
                f'{indent}    self._universe = [f.Symbol for f in elig[:5]]\n'
                f'{indent}    return self._universe\n'
            )
            lines.insert(last_def, sel)
            c = '\n'.join(lines)

    return c


def main():
    files = sorted(os.listdir(ALGOS_DIR))
    for fname in files:
        if not fname.startswith("algo_") or not fname.endswith(".py"):
            continue
        num_str = fname.replace("algo_", "").replace(".py", "")
        try:
            num = int(num_str)
        except ValueError:
            continue
        if num not in range(31, 61):
            continue

        fpath = os.path.join(ALGOS_DIR, fname)
        orig = open(fpath).read()
        result = transform(fpath, num)
        if result != orig:
            open(fpath, 'w').write(result)
            print(f"  Transformed {fname}")
        else:
            print(f"  SKIP (no change) {fname}")


if __name__ == "__main__":
    # Restore originals first from git
    os.system("cd cc/algos2 && git checkout -- algo_0*.py 2>/dev/null")
    main()
