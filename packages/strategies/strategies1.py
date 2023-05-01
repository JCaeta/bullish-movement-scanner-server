import pandas as pd

class Strategy1: 
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
        # return { 'time': data['time'], 'open': data['open'], 'high': data['high'], 'low': data['low'], 'close': data['close'] }
        return data

class StrategyPriceTrigger:
    def __init__(self, entry_price: float, upper_price: float, lower_price: float, func_close):
        self.candlesticks = []
        self.upper_price = upper_price
        self.lower_price = lower_price
        self.entry_price = entry_price
        self.close_price = None
        self.func_close = func_close
        self.strategy = Strategy1()
        # self.type_trigger = None
        
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

        self.candlesticks.append(data)

        if((data["open"] or data["high"] or data["low"] or data["close"]) >= self.upper_price):
            self.upper_price_event()
        elif((data["open"] or data["high"] or data["low"] or data["close"]) <= self.lower_price):
            self.lower_price_event()
    
    def upper_price_event(self):
        self.close(self.upper_price)
        # self.type_trigger = 'upper'

    def lower_price_event(self):
        self.close(self.lower_price)
        # self.type_trigger = 'lower'

    def close(self, price):
        # self.type_trigger = price
        self.close_price = price
        if self.func_close != None:
            self.func_close()

class Movement:
    def __init__(self, entry_price, close_price, candlesticks):
        self.candlesticks = candlesticks
        self.entry_price = entry_price
        self.close_price = close_price
    
    def set_candlesticks(self, candlesticks):
        self.candlesticks = candlesticks

class StrategyMovementTracker:
    def __init__(self):
        self.entry_price = None
        self.long_percentage = None
        self.short_percentage = None
        self.upper_price = None
        self.lower_price = None
        self.movements = []

    def clear(self):
        self.entry_price = None
        self.long_percentage = None
        self.short_percentage = None
        self.upper_price = None
        self.lower_price = None
        self.movements = []

    def start_tracking(self, entry_price: float, long_percentage: float, short_percentage: float):
        self.entry_price = entry_price
        self.long_percentage = long_percentage
        self.short_percentage = short_percentage

        upper_price = self.entry_price + (self.entry_price*self.long_percentage)
        lower_price = self.entry_price - (self.entry_price*self.short_percentage)

        self.price_trigger = StrategyPriceTrigger(self.entry_price, upper_price, lower_price, self.func_close)

    def set_current_data(self, data):
        if self.entry_price == None:
            self.start_tracking(data['open'], 0.01, 0.01)
        self.price_trigger.on_price_event(data)
        
    def func_close(self):
        move = Movement(self.entry_price, self.price_trigger.close_price, self.price_trigger.candlesticks)
        self.movements.append(move)

        self.entry_price = None
        self.long_percentage = None
        self.short_percentage = None
        self.upper_price = None
        self.lower_price = None
        
class StrategyBuyOperation:
    candlesticks = []

    def __init__(self, take_profit_price: float, stop_loss_price: float, entry_price: float):
        self.take_profit_price = take_profit_price
        self.stop_loss_price = stop_loss_price
        self.entry_price = entry_price
        
    def current_event(self, data):
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

        self.candlesticks.append(data)
        if((data["open"] or data["high"] or data["low"] or data["close"]) >= self.take_profit_price):
            pass

