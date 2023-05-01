from packages.backtesting_utils.backtesting_utils import Backtest
import pandas as pd
from packages.strategies.strategies2 import StrategyMovementTracker
from packages.charts.tradingview_utils import create_rect
from packages.json_utils.adapters import JsonInvestingAdapter

data_dir = "D:\\documents storage\\repositories\\Reusables\\financials_visualization_reusables\\Data\\"
path_ggal_norm = data_dir + "GGAL_norm.csv"

class ChartsController:
    """
    UI data format
    Data formats that lightweight libary needs on the frontend

    Lines
    - To plot a line over candlesticks must be a time value for 
    each candlestick value, in other words, must not be time gaps

        const line = [
            { time: '2023-02-02', value: 24000 },
            { time: '2022-02-03', value: 25000 },
            ...
        ]

    Candlesticks
        - With timestamps
        const candlesticks = [
                { time: 1643687400, open: 50, high: 60, low: 40, close: 55 },
                { time: 1643687700, open: 55, high: 65, low: 45, close: 60 },
                { time: 1643688000, open: 60, high: 70, low: 50, close: 65 },
                // ...
            ];

        - With date
        const candlesticks = [
                { time: '2021-02-23', open: 50, high: 60, low: 40, close: 55 },
                { time: '2021-02-24', open: 55, high: 65, low: 45, close: 60 },
                { time: '2021-02-25', open: 60, high: 70, low: 50, close: 65 },
                // ...
            ];
    """

    def __init__(self):
        self.data = pd.read_csv(path_ggal_norm)
        self.strategy = StrategyMovementTracker()
        self.backtest = Backtest(self.data, self.strategy)

    # def set_all_data(self, strategy):
    #     candlesticks = []
    #     rects = []
    #     for i, row in self.data.iterrows():
    #         candlesticks.append({ 'time': row['time'], 'open': row['open'], 'high': row['high'], 'low': row['low'], 'close': row['close'] })
        
    #     return {'candlesticks': candlesticks, 'rects': rects}

    def get_all(self):
        self.backtest.clear()
        self.backtest.run()
        self.all_data = self.set_all_data(self.strategy)
        return self.all_data

    def analyze(self, data_json):
        data = self.normalize_data(data_json['file'])
        self.strategy = StrategyMovementTracker()
        self.backtest = Backtest(data, self.strategy)
        self.backtest.clear()
        self.backtest.run()
        data = self.set_all_data(self.strategy)
        return data

    def normalize_data(self, json_data):
        # Create a DataFrame from the CSV data
        column_names = json_data[0]
        data_rows = json_data[1:]
        data = pd.DataFrame(data_rows, columns=column_names)

        adapter = JsonInvestingAdapter()
        adapter.set_data(data)
        adapter.convert_to_base_format()
        return adapter.get_data_base_format()

    def set_all_data(self, strategy):
        candlesticks = []
        rects = []
        for i, row in self.data.iterrows():
            candlesticks.append({ 'time': row['time'], 'open': row['open'], 'high': row['high'], 'low': row['low'], 'close': row['close'] })
        
        for i in strategy.movements:
            rects.append(create_rect(i.entry_price, i.close_price, i.candlesticks))
        
        return {'candlesticks': candlesticks, 'rects': rects}
