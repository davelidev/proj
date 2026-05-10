class BaseSubAlgo:
    """Minimal base class for sub-algorithms."""
    def __init__(self):
        self.symbols = []
        self.benchmark = None
        self.name = "BaseSubAlgo"

    def initialize(self):
        raise NotImplementedError

    def update_targets(self, context):
        raise NotImplementedError


class Algo187(BaseSubAlgo):
    """
    Strategy: Information ratio – active return consistency.
    Maintains active return close to a target by adjusting weights
    proportionally to the deviation, aiming for stable, positive
    active returns with low tracking error.
    """
    def initialize(self):
        self.name = "Algo187"
        # Strategy parameters
        self.target_active_return = 0.0005  # 0.05% per period
        self.smoothing_factor = 0.2          # weight adjustment sensitivity
        # Placeholder for per-symbol alpha estimates (could be populated later)
        self.alpha_scores = {sym: 0.0 for sym in self.symbols}
        # Baseline equal weights (must sum to 1.0)
        self.base_weights = {sym: 1.0 / len(self.symbols) for sym in self.symbols}
        # Last active return (for smoothing)
        self.last_active_return = 0.0

    def update_targets(self, context):
        """
        Compute target weights based on active return consistency.
        context must contain:
            'current_active_return': float (most recent period active return)
        Returns a dict of target weights (symbol -> weight).
        """
        if not self.symbols:
            return {}

        # Get current active return from context
        current_active_return = context.get('current_active_return', self.last_active_return)

        # Deviation from target
        deviation = current_active_return - self.target_active_return

        # Adjust weights: underperformers (negative deviation) get increased exposure
        # if they have positive alpha; overperformers get reduced.
        # Here we use a simple proportional rule based on alpha scores.
        adjustment = -self.smoothing_factor * deviation

        # Compute adjustment per symbol proportional to alpha scores
        total_alpha = sum(abs(v) for v in self.alpha_scores.values())
        if total_alpha == 0:
            # Fall back to equal adjustment
            adjustments = {sym: adjustment / len(self.symbols) for sym in self.symbols}
        else:
            adjustments = {sym: adjustment * (self.alpha_scores[sym] / total_alpha)
                           for sym in self.symbols}

        # New weights = base weights + adjustments, then ensure non-negative and sum to 1
        raw_weights = {sym: self.base_weights[sym] + adjustments[sym] for sym in self.symbols}
        # Clamp to [0,1] and renormalize
        min_clamped = {sym: max(0.0, w) for sym, w in raw_weights.items()}
        total = sum(min_clamped.values())
        if total > 0:
            target_weights = {sym: w / total for sym, w in min_clamped.items()}
        else:
            # Fallback to equal weights if all become zero
            target_weights = {sym: 1.0 / len(self.symbols) for sym in self.symbols}

        # Update internal state
        self.last_active_return = current_active_return
        # Optionally update base weights to the new target for next iteration
        self.base_weights = target_weights.copy()

        return target_weights
