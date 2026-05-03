from datetime import datetime
from unittest.mock import MagicMock

MONDAY  = datetime(2020, 1, 6, 10, 5)
TUESDAY = datetime(2020, 1, 7, 10, 5)


def make_indicator(value=50.0, is_ready=True):
    ind = MagicMock()
    ind.Current = MagicMock()
    ind.Current.Value = value
    ind.IsReady = is_ready
    return ind


def make_security(price=100.0, invested=False, avg_price=100.0, holdings_value=0.0):
    sec = MagicMock()
    sec.Price = price
    sec.Invested = invested
    sec.Holdings = MagicMock()
    sec.Holdings.AveragePrice = avg_price
    sec.Holdings.HoldingsValue = holdings_value
    return sec


def make_algo(time=None, is_warming_up=False, portfolio_value=100_000.0):
    algo = MagicMock()
    algo.IsWarmingUp = is_warming_up
    algo.Time = time or MONDAY
    algo.Portfolio = MagicMock()
    algo.Portfolio.TotalPortfolioValue = portfolio_value
    algo.Portfolio.Cash = portfolio_value
    algo.Securities = {}

    def add_equity(ticker, *args, **kwargs):
        result = MagicMock()
        result.Symbol = ticker
        algo.Securities[ticker] = make_security()
        return result

    algo.AddEquity.side_effect = add_equity
    algo.RSI.return_value = make_indicator(50.0)
    algo.SMA.return_value = make_indicator(100.0)
    algo.MAX.return_value = make_indicator(120.0)
    algo.ATR.return_value = make_indicator(2.0)
    algo.ADX.return_value = make_indicator(30.0)
    return algo


def make_fundamental(symbol, sector, market_cap, has_data=True):
    f = MagicMock()
    f.Symbol = symbol
    f.HasFundamentalData = has_data
    f.AssetClassification.MorningstarSectorCode = sector
    f.MarketCap = market_cap
    return f


def make_changes(added=None, removed=None):
    changes = MagicMock()
    changes.AddedSecurities = added or []
    changes.RemovedSecurities = removed or []
    return changes


class MockBar:
    def __init__(self, high, low):
        self.high = high
        self.low = low


class MockHistory:
    def __init__(self, bars):
        self._bars = bars

    def __len__(self):
        return len(self._bars)

    @property
    def iloc(self):
        return self._bars


def make_history(*bar_tuples):
    return MockHistory([MockBar(h, l) for h, l in bar_tuples])
