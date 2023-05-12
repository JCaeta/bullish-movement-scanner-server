import pandas as pd
import copy

class Movement:
    def __init__(self, entry_price, close_price = None):
        self.candlesticks = []
        self.entry_price = entry_price
        self.close_price = close_price
        self.max_value_candlestick = {'value': None, 'index': None, 'data': None}
        self.candlesticks_until_max = []
        self.min_value_candlestick = {'value': None, 'index': None, 'data': None}
        self.candlesticks_until_min = []

    def set_candlesticks(self, candlesticks):
        self.candlesticks = candlesticks

    def set_close_price(self, close_price):
        self.close_price = close_price
    
    def add_candlestick(self, data):
        self.candlesticks.append(data)
        self.check_max_value(data)
        self.check_min_value(data)
    
    def check_max_value(self, data):
        max_value = max([data['open'], data['high'], data['close']])

        if self.max_value_candlestick['value'] == None or max_value > self.max_value_candlestick['value']:
            self.max_value_candlestick = {
                'value': max_value, 
                'index': len(self.candlesticks) - 1, 
                'data': data}
            self.candlesticks_until_max = self.candlesticks[:self.max_value_candlestick['index'] + 1]
    
    def check_min_value(self, data):
        min_value = min([data['open'], data['low'], data['close']])
        if self.min_value_candlestick['value'] == None or min_value > self.min_value_candlestick['value']:
            self.min_value_candlestick = {
                'value': min_value, 
                'index': len(self.candlesticks) - 1, 
                'data': data}
        
            self.candlesticks_until_min = self.candlesticks[:self.min_value_candlestick['index'] + 1]
        
class StrategyPriceTrigger:
    def __init__(self, entry_price: float, 
                 upper_price = None, 
                 lower_price = None, 
                 func_lower_close = None, 
                 func_upper_close = None):
        self.upper_price = upper_price
        self.lower_price = lower_price
        self.entry_price = entry_price
        self.close_price = None
        self.func_lower_close = func_lower_close
        self.func_upper_close = func_upper_close
        self.movement = Movement(entry_price = self.entry_price)

    def on_price_event(self, data):
        """
        Data is a pandas array
        format:
            time     1.635549e+09
            open     1.155160e+00
            high     1.155310e+00
            low      1.155110e+00
            close    1.155260e+00

        Example of how to get the time
        time = data[time]
        """

        # self.candlesticks.append(data)
        self.movement.add_candlestick(data)
        if self.upper_price_triggered(data):
            self.upper_price_event()
        elif self.lower_price_triggered(data):
            self.lower_price_event()
    
    def upper_price_triggered(self, data) -> bool:
        if(self.upper_price != None):
            max_value = max([data["open"], data["high"], data["low"], data["close"]])
            return max_value >= self.upper_price 

    def lower_price_triggered(self, data) -> bool:
        if(self.lower_price != None):
            min_value = min([data["open"], data["high"], data["low"], data["close"]])
            return min_value <= self.lower_price
                
    def upper_price_event(self):
        self.close(self.upper_price)
        self.func_upper_close()

    def lower_price_event(self):
        self.close(self.lower_price)
        self.func_lower_close()

    def close(self, price):
        self.close_price = price
        self.movement.set_close_price(self.close_price)

    def set_lower_price(self, lower_price):
        self.lower_price = lower_price

class NormalDistribution:
    # This normal distribution calculate percentages

    def __init__(self, movements = [], interval = 0.02):
        self.interval = interval
        self.max_value = None
        self.min_value = None
        self.x = {}
        self.y = {}
        self.max_n_intervals = 100
        self.movements = movements

    def calculate(self):
        percentages = []
        for move in self.movements:
            max_value = move.max_value_candlestick['value']
            entry_price = move.entry_price
            perc = (max_value - entry_price)/entry_price
            percentages.append(perc)
        
        self.setup_intervals(percentages)
        # Set intervals
        # max_perc = max(percentages)
        # i = 0
        # self.x[i] = 0
        # while i <= max_perc:
        #     i += self.interval
        #     self.x[round(i, 4)] = 0

        # for p in percentages:
        #     for i in self.x:
        #         if p <= i:
        #             self.x[round(i - self.interval, 4)] += 1
        #             break
        return self.x
    
    def setup_intervals(self, percentages):
        if(len(percentages) > 0):
            max_perc = max(percentages)
            n_intervals = max_perc/self.interval
            interval_step = 0.02

            while n_intervals > self.max_n_intervals:
                self.interval += interval_step
                n_intervals = max_perc/self.interval

            i = 0
            self.x[i] = 0
            while i <= max_perc:
                i += self.interval
                self.x[round(i, 4)] = 0

            for p in percentages:
                for i in self.x:
                    if p <= i:
                        self.x[round(i - self.interval, 4)] += 1
                        break
        else:
            self.x[0] = 0
            return self.x

class StrategyMovementTracker:
    def __init__(self):
        self.entry_price = None
        self.long_percentage = None
        self.short_percentage = None
        self.upper_price = None
        self.lower_price = None
        self.movements = []
        self.max_price = None

    def clear(self):
        self.entry_price = None
        self.long_percentage = None
        self.upper_price = None
        self.lower_price = None
        self.movements = []
        self.price_trigger = None
    
    def clear_close(self):
        self.price_trigger = None
        self.entry_price = None
        self.long_percentage = None
        self.upper_price = None
        self.lower_price = None

    def start_tracking(self, entry_price: float):
        self.entry_price = entry_price
        self.max_price = self.entry_price

        lower_price = self.entry_price - (self.entry_price*self.short_percentage)
        self.price_trigger = StrategyPriceTrigger(entry_price = self.entry_price, 
                                                  lower_price = lower_price, 
                                                  func_lower_close = self.func_lower_close)

    def set_max_correction(self, max_price):
        self.price_trigger.set_lower_price(max_price - (max_price*self.short_percentage))

    def set_current_data(self, data):
        """
        data: DataFrame.series
        """
        # 1) If there is not open operation, open one
        if self.entry_price == None:
            min_value = min([data["open"], data["high"], data["low"], data["close"]])
            # self.start_tracking(min_value, 0.1, 0.1)
            self.start_tracking(min_value)

        # 2) Check and set max price
        self.check_max_correction(data)

        # 3) Send data to price trigger
        self.price_trigger.on_price_event(data)
    
    def check_max_correction(self, data):
        # Check and set max price
        max_value = max([data["open"], data["high"], data["low"], data["close"]])
        if (max_value > self.max_price):
            self.max_price = max_value
            self.set_max_correction(self.max_price)

    # def func_upper_close(self):
    #     move = self.price_trigger.movement
    #     if len(move.candlesticks_until_max) > 1:
    #         # Check close_price > entry_price in the whole movement
    #         if move.close_price > move.entry_price:
    #             self.movements.append(move)
    #     self.clear_close()

    def func_lower_close(self):
        move = self.price_trigger.movement
        if len(move.candlesticks_until_max) > 1:
            # if move.close_price > move.entry_price:
            #     self.movements.append(move)
            if move.close_price < move.entry_price:
                move.close_price = move.max_value_candlestick['value']
            self.movements.append(move)
                
        self.clear_close()

    def check_open_movements(self):
        if self.price_trigger != None:
            # Close movement
            self.price_trigger.lower_price_event()

