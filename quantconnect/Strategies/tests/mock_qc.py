import sys
import types


class _CurrentValue:
    def __init__(self, value=0.0):
        self.Value = value


class PythonIndicator:
    def __init__(self):
        self.Current = _CurrentValue(0.0)
        self.IsReady = False

    def Update(self, *args):
        return False


class SimpleMovingAverage:
    def __init__(self, period):
        self.period = period
        self.Current = _CurrentValue(0.0)
        self.IsReady = False

    def Update(self, time, value):
        self.Current.Value = value
        self.IsReady = True


class Resolution:
    Daily = "Daily"
    Minute = "Minute"


class MovingAverageType:
    Wilders = "Wilders"


class MorningstarSectorCode:
    Technology = 311


class QCAlgorithm:
    pass


def install_mock():
    module = types.ModuleType("AlgorithmImports")
    module.Resolution = Resolution
    module.MovingAverageType = MovingAverageType
    module.MorningstarSectorCode = MorningstarSectorCode
    module.PythonIndicator = PythonIndicator
    module.SimpleMovingAverage = SimpleMovingAverage
    module.QCAlgorithm = QCAlgorithm
    sys.modules["AlgorithmImports"] = module
