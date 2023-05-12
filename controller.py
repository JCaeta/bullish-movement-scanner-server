from packages.backtesting_utils.backtesting_utils import Backtest
import pandas as pd
from packages.strategies.strategies3 import StrategyMovementTracker
from packages.strategies.strategies3 import NormalDistribution
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
        # self.data = pd.read_csv(path_ggal_norm)
        # self.strategy = StrategyMovementTracker()
        # self.backtest = Backtest(self.data, self.strategy)
        pass

    def get_all(self):
        self.backtest.clear()
        self.backtest.run()
        self.all_data = self.set_all_data(self.strategy)
        return self.all_data

    def clear(self):
        self.backtest = None
        self.strategy = None

    def analyze(self, data_json):
        # 1) Get necessary data
        data = self.normalize_data(data_json['file'])
        max_correction_percentage = float(data_json['maxCorrectionPercentage'])

        # self.backtest = None
        self.strategy = StrategyMovementTracker()
        self.strategy.short_percentage = max_correction_percentage/100
        self.backtest = Backtest(data, self.strategy)
        self.backtest.run()
        data = self.set_all_data(self.strategy, data)
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

    # Strategy 3
    def set_all_data(self, strategy, data):
        candlesticks = self.setup_candlesticks(data)
        rects = self.setup_movement_rects(strategy.movements)
        normal_distribution = self.setup_normal_distribution(strategy.movements)
        
        return {
            'candlesticksChart': {'candlesticks': candlesticks, 'rects': rects},
            'normDistChart': normal_distribution
        }
        # return {'candlesticks': candlesticks, 'rects': rects, 'normalDist': normal_distribution}
    
    def setup_candlesticks(self, data):
        candlesticks = []
        for i, row in data.iterrows():
            candlesticks.append({ 'time': row['time'], 'open': row['open'], 'high': row['high'], 'low': row['low'], 'close': row['close'] })
        return candlesticks

    def setup_movement_rects(self, movements):
        rects = []
        for move in movements:
            move_candlesticks = move.candlesticks_until_max
            entry_price = move.entry_price
            close_price = move.max_value_candlestick['value']
            rects.append(create_rect(entry_price, close_price, move_candlesticks))
        return rects

    def setup_normal_distribution(self, movements):
        normal_distribution = NormalDistribution(movements)
        x = normal_distribution.calculate()

        data = {'labels': [], 'data': []}
        for i in x:
            label = str(round(i*100, 4)) + "% - " + str(round((i + (normal_distribution.interval - 0.001))*100, 4)) + "%"
            data['labels'].append(label)
            data['data'].append(x[i])
        return data

