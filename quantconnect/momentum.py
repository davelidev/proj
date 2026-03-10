from AlgorithmImports import *


class ConditionalSectorRotation(QCAlgorithm):

    def Initialize(self):
        # 1. Set Strategy Settings
        self.SetStartDate(2015, 1, 1)  # Set your start date
        self.SetCash(100000)  # Set your starting capital
        self.rsi_period = int(self.GetParameter("rsi_period") or 10)
        self.spy_sma_period = int(self.GetParameter("spy_sma_period") or 200)
        self.qqq_sma_period = int(self.GetParameter("qqq_sma_period") or 20)
        self.tqqq_sma_period = int(self.GetParameter("tqqq_sma_period") or 20)

        # 2. Define the Universe of Tickers
        self.tickers = [
            "SPY", "QQQ", "TQQQ", "UVXY",
            "TECL", "SPXL", "SQQQ", "TECS", "BSV", "QID"
        ]

        self.symbols = {}
        self.rsis = {}

        # 3. Initialize Assets and Indicators
        for ticker in self.tickers:
            # Add Equity with Daily resolution for standard MA/RSI calculation
            symbol = self.AddEquity(ticker, Resolution.Daily).Symbol
            self.symbols[ticker] = symbol
            # Initialize RSI for all assets (Standard 14 period)
            self.rsis[ticker] = self.RSI(symbol, self.rsi_period, MovingAverageType.Wilders, Resolution.Daily)

        # 4. Initialize Specific Moving Averages required by logic
        self.spy_sma = self.SMA(self.symbols["SPY"], self.spy_sma_period, Resolution.Daily)
        self.qqq_sma = self.SMA(self.symbols["QQQ"], self.qqq_sma_period, Resolution.Daily)
        self.tqqq_sma = self.SMA(self.symbols["TQQQ"], self.tqqq_sma_period, Resolution.Daily)

        # 5. Warm Up Period
        self.SetWarmUp(200)
        
        # 6. State Tracking
        self.current_ticker = None

    def OnData(self, data):
        # Ensure data is ready before running logic
        if self.IsWarmingUp or not self.spy_sma.IsReady: return

        # -------------------------------------------------------------
        # RETRIEVE CURRENT VALUES
        # -------------------------------------------------------------

        # Prices
        price_spy = self.Securities[self.symbols["SPY"]].Price
        price_tqqq = self.Securities[self.symbols["TQQQ"]].Price

        # Indicators (Values)
        rsi_qqq = self.rsis["QQQ"].Current.Value
        rsi_tqqq = self.rsis["TQQQ"].Current.Value

        sma_spy = self.spy_sma.Current.Value
        sma_tqqq = self.tqqq_sma.Current.Value

        target_ticker = None

        # -------------------------------------------------------------
        # EXECUTE LOGIC TREE
        # -------------------------------------------------------------

        if price_spy > sma_spy:
            if rsi_qqq > 80:
                target_ticker = "UVXY"
            else:
                target_ticker = "TQQQ"
        else:
            if rsi_qqq < 30: # Over-sold on tqqq
                target_ticker = "TQQQ"
            else:
                if price_tqqq > sma_tqqq:
                    target_ticker = "TQQQ" if rsi_tqqq < 70 else "TECS"
                else:
                    target_ticker = self.GetMaxRsiAsset(["TECS", "BSV"])

        # -------------------------------------------------------------
        # EXECUTE TRADE
        # -------------------------------------------------------------
        if target_ticker != self.current_ticker:
            self.SetHoldings(self.symbols[target_ticker], 1, liquidateExistingHoldings=True)
            self.current_ticker = target_ticker

    def GetMaxRsiAsset(self, ticker_list):
        """Helper to compare RSIs and return the ticker with the highest value"""
        return max(ticker_list, key=lambda t: self.rsis[t].Current.Value)