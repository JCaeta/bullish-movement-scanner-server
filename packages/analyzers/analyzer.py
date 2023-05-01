import abc
import pandas as pd
from .operator import Operator

class IAnalyzer(abc.ABC):
    @abc.abstractmethod
    def analyze_data(self, data: pd.DataFrame):
        pass

class Analyzer1(IAnalyzer):
    __data = None

    def analyze_data(self, data: pd.DataFrame):
        self.__data = data

        # 1) Calculate moving average
        self.__data["ma200"] = self.calculate_moving_average(self.__data, 200, "close")
        self.__data = self.calculate_bolliger_bands(self.__data, 100, "close", 2)
        self.__data = self.calculate_average_range(self.__data, 8)

    def calculate_moving_average(self, data, period: int, price: str):
        """
        price variable could be
        - close
        - open
        - high
        - low
        """
        return data[price].rolling(period).mean()
    
    def calculate_bolliger_bands(self, data: pd.DataFrame, period: int, price: str, mult: float):

        # Compute the rolling mean and standard deviation of the prices
        rolling_mean = data[price].rolling(window=period).mean()
        rolling_std = data[price].rolling(window=period).std()

        # Compute the upper and lower Bollinger Bands
        upper_band = rolling_mean + (rolling_std * mult)
        lower_band = rolling_mean - (rolling_std * mult)

        # Add the Bollinger Bands to the DataFrame
        data['bb' + str(period) + '_up_band'] = upper_band
        data['bb' + str(period) + '_low_band'] = lower_band
        data['bb' + str(period) + '_mean'] = rolling_mean
        return data

    def calculate_average_range(self, data: pd.DataFrame, period: int):
        str_period = str(period)
        data['range' + str_period] = abs((data['high'] - data['open'])/data['open']) + abs((data['low'] - data['open'])/data['open'])
        data['avg_range' + str_period] = data['range' + str_period].rolling(window=period).mean()
        return data

    def get_data(self):
        return self.__data

    def open_positions(self, data: pd.DataFrame):
        stop_loss_perc = 0.001
        take_profit_perc = 0.001
        operator = Operator(stop_loss_perc, take_profit_perc)

        for index, row in data.iterrows():
            # input()
            prices = [row['open'], row['low'], row['high'], row['close']]
            up_band = row['bb100_up_band']
            low_band = row['bb100_low_band']

            # print(prices)
            # if there are an open position
            if operator.position_is_open():
            # If the price goes above the upper band
            if any(price > up_band for price in prices):
                # Open sell position
                operator.open_sell_position(row['time'])

            # If the price goes below the lower band
            elif any(price < low_band for price in prices):
                # Open buy position
                # print("buy")
                operator.open_buy_position(row['time'])
            else:

        return operator.get_markers()


















    # def open_positions(self, data: pd.DataFrame):
    #     sell = False
    #     buy = False
    #     perc_stop_loss = 0.001
    #     perc_take_profit = 0.001
    #     stop_loss_price = None
    #     take_profit_price = None
    #     time_bars = []
    #     open_price = None

    #     dict_operation_lines = {
    #         'operation_type': [], # buy or sell
    #         'time': [],
    #         'price': [],
    #     }

    #     dict_markers = {
    #         'operation_type': [],
    #         'time': [],
    #         'price': []
    #     }

    #     def clear_variables():
    #         global sell
    #         global buy
    #         global stop_loss_price
    #         global take_profit_price 
    #         global time_bars
    #         global open_price

    #         sell = False
    #         buy = False
    #         stop_loss_price = None
    #         take_profit_price = None
    #         time_bars = []
    #         open_price = None

    #     def print_variables():
    #         global sell
    #         global buy
    #         global stop_loss_price
    #         global take_profit_price 
    #         global time_bars
    #         global open_price

    #         print("sell: ", sell, " | buy: ", buy, " | stop_loss_price: ", stop_loss_price, " | take_profit_price: ", take_profit_price, " | time_bars: ", time_bars, " | open_price: ", open_price)
    #         sell = False
    #         buy = False
    #         stop_loss_price = None
    #         take_profit_price = None
    #         time_bars = []
    #         open_price = None


    #     for index, row in data.iterrows():
    #         # input()
    #         prices = [row['open'], row['low'], row['high'], row['close']]
    #         up_band = row['bb100_up_band']
    #         low_band = row['bb100_low_band']

    #         print(prices, " | up_band: ", up_band, " | low_band: ", low_band)
    #         # If there aren't open positions
    #         if sell == False and buy == False:
    #             print("there are an open position")
    #             print_variables()
    #             # If the price goes above the upper band
    #             if any(price > up_band for price in prices):
    #                 # Open sell position
    #                 sell = True
    #                 open_price = max(prices)
    #                 stop_loss_price = open_price + (open_price*perc_stop_loss)
    #                 take_profit_price = open_price - (open_price*perc_take_profit)
    #                 time_bars.append(row['time'])

    #                 dict_markers['operation_type'] = 'sell'
    #                 dict_markers['price'] = open_price
    #                 dict_markers['time'] = row['time']
    #                 print("sell | stop_loss_price: ", stop_loss_price, " | dict_markers: ", dict_markers)


    #             # If the price goes below the lower band
    #             elif any(price < low_band for price in prices):
    #                 # Open buy position
    #                 print("buy")
    #                 buy = True
    #                 price_buy = min(prices)
    #                 stop_loss_price = price_buy - (price_buy*perc_stop_loss)
    #                 take_profit_price = price_buy + (price_buy*perc_take_profit)
    #                 time_bars.append(row['time'])

    #                 dict_markers['operation_type'] = 'buy'
    #                 dict_markers['price'] = price_buy
    #                 dict_markers['time'] = row['time']

    #         # If there are a sell open position
    #         elif sell:
    #             input()
    #             time_bars.append(row['time'])
    #             # If price goes to stop loss
    #             if any(price >= stop_loss_price for price in prices):
    #                 # Close sell position
    #                 # 1) Calculate values for line
    #                 slope = (stop_loss_price - open_price) / len(time_bars)
    #                 for i, time in enumerate(time_bars):
    #                     y = slope*i + open_price
    #                     dict_operation_lines['operation_type'] = 'sell'
    #                     dict_operation_lines['price'] = y
    #                     dict_operation_lines['time'] = time
    #                 print("close sell | dict_operation_lines", dict_operation_lines)
    #                 clear_variables()
    #                 print_variables()

    #             # If price goes to take profit
    #             elif any(price <= take_profit_price for price in prices):
    #                 # Close sell position
    #                 # 1) Calculate values for line
    #                 slope = (take_profit_price - open_price) / len(time_bars)
    #                 for i, time in enumerate(time_bars):
    #                     y = slope*i + open_price
    #                     dict_operation_lines['operation_type'] = 'sell'
    #                     dict_operation_lines['price'] = y
    #                     dict_operation_lines['time'] = time
    #                 print("close sell | dict_operation_lines", dict_operation_lines)
    #                 clear_variables()
    #                 print_variables()

    #         elif buy:
    #             time_bars.append(row['time'])
    #             # If price goes to stop loss
    #             if any(price <= stop_loss_price for price in prices):
    #                 # Close buy position
    #                 # 1) Calculate values for line
    #                 slope = (stop_loss_price - price_buy) / len(time_bars)
    #                 for i, time in enumerate(time_bars):
    #                     y = slope*i + price_buy
    #                     dict_operation_lines['operation_type'] = 'buy'
    #                     dict_operation_lines['price'] = y
    #                     dict_operation_lines['time'] = time
    #                 clear_variables()
    #                 print_variables()
                
    #             # If price goes to take profit
    #             elif any(price >= take_profit_price for price in prices):
    #                 # Close buy position
    #                 # 1) Calculate values for line
    #                 slope = (take_profit_price - price_buy) / len(time_bars)
    #                 for i, time in enumerate(time_bars):
    #                     y = slope*i + open_price
    #                     dict_operation_lines['operation_type'] = 'buy'
    #                     dict_operation_lines['price'] = y
    #                     dict_operation_lines['time'] = time
    #                 clear_variables()
    #                 print_variables()
    #     return dict_operation_lines, dict_markers
            

