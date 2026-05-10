from QuantConnect import *
from QuantConnect.Algorithm.Framework import *
from QuantConnect.Algorithm.Framework.Alphas import AlphaModel
from QuantConnect.Algorithm.Framework.Portfolio import PortfolioConstructionModel
from QuantConnect.Algorithm.Framework.Risk import RiskManagementModel
from QuantConnect.Algorithm.Framework.Execution import ExecutionModel

class Algo176(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.AddEquity("TQQQ", Resolution.Daily)
        
        self.window = []
        self.leverage = 1.0
        
    def OnData(self, data):
        if not self.IsWarmingUp:
            if not self.Portfolio.Invested:
                self.SetHoldings("TQQQ", 0.9 * self.leverage)
            else:
                current_price = self.Securities["TQQQ"].Price
                self.window.append(current_price)
                if len(self.window) > 20:
                    self.window.pop(0)
                
                if len(self.window) == 20:
                    avg = sum(self.window) / 20
                    if current_price > avg * 1.01:
                        self.SetHoldings("TQQQ", 1.0 * self.leverage)
                    elif current_price < avg * 0.99:
                        self.SetHoldings("TQQQ", 0.5 * self.leverage)
