class BaseSubAlgo:
    """
    Base class for sub-algorithms. Provides minimal structure.
    Subclasses should override initialize() and update_targets().
    """
    def __init__(self):
        self.initial_capital = 100000.0   # example default
        self.current_capital = self.initial_capital
        self.position_size = 0.0          # fraction of capital to risk
        self.trades = []                  # list of trade outcomes: {'profit_ratio': float} (e.g., 0.1 for 10% gain, -0.05 for 5% loss)

    def initialize(self):
        """Initialize algorithm state. To be overridden."""
        pass

    def update_targets(self):
        """Update target position size. To be overridden."""
        pass


class Algo143(BaseSubAlgo):
    """
    Kelly Criterion strategy.
    Position size is determined by:
        f* = (p * R - (1-p)) / R
    where p = win rate, R = average win / average loss (reward-to-risk ratio).
    Only trades with positive expectation are taken; otherwise position size is 0.
    """
    def initialize(self):
        """Set up algorithm-specific parameters."""
        self.win_rate = 0.0
        self.avg_win = 0.0
        self.avg_loss = 0.0
        self.kelly_fraction = 0.0
        # Kelly fraction multiplier (e.g., use half-Kelly to be more conservative)
        self.kelly_multiplier = 0.5

    def update_targets(self):
        """
        Recompute Kelly fraction based on recent trades and set position size.
        Assumes self.trades contains a list of dicts with key 'profit_ratio'.
        """
        # Reset statistics
        wins = []
        losses = []
        for trade in self.trades:
            profit = trade['profit_ratio']
            if profit > 0:
                wins.append(profit)
            elif profit < 0:
                losses.append(abs(profit))   # use absolute loss amount
            # zero profit trades are ignored (neither win nor loss)

        total_trades = len(wins) + len(losses)
        if total_trades == 0:
            self.position_size = 0.0
            return

        self.win_rate = len(wins) / total_trades
        self.avg_win = sum(wins) / len(wins) if wins else 0.0
        self.avg_loss = sum(losses) / len(losses) if losses else 0.0

        if self.avg_loss == 0 or self.avg_win == 0:
            # Cannot compute R reliably; no position
            self.kelly_fraction = 0.0
        else:
            R = self.avg_win / self.avg_loss
            p = self.win_rate
            # Kelly fraction for binary outcomes with fixed risk/reward
            f = (p * R - (1 - p)) / R
            self.kelly_fraction = max(0.0, min(1.0, f * self.kelly_multiplier))

        # Update position size as a fraction of current capital
        self.position_size = self.kelly_fraction

    # Optional helper to record a trade
    def record_trade(self, profit_ratio):
        """Add a trade result (profit/loss ratio) to the history."""
        self.trades.append({'profit_ratio': profit_ratio})
